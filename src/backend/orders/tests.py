from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient

from orders.models import Order
from users.models import Address


class OrderShippingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="buyer", password="pwd123456")
        self.staff = User.objects.create_user(
            username="staff_user",
            password="pwd123456",
            is_staff=True,
        )
        self.address = Address.objects.create(
            user=self.customer,
            name="Buyer",
            address="Shanghai Road 1",
            phone_number="13800000000",
            is_default=True,
        )
        self.order = Order.objects.create(
            user=self.customer,
            address=self.address,
            status="pending_shipment",
        )

    def test_staff_can_ship_paid_order(self):
        self.client.force_authenticate(self.staff)

        response = self.client.post(
            f"/api/orders/{self.order.id}/ship/",
            {
                "express_company": "SF Express",
                "express_no": "SF1234567890",
                "shipping_remark": "Leave at service desk",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "pending_receipt")
        self.assertEqual(self.order.express_company, "SF Express")
        self.assertEqual(self.order.express_no, "SF1234567890")
        self.assertEqual(self.order.shipping_remark, "Leave at service desk")
        self.assertIsNotNone(self.order.shipped_at)

    def test_non_staff_cannot_ship_order(self):
        self.client.force_authenticate(self.customer)

        response = self.client.post(f"/api/orders/{self.order.id}/ship/", {}, format="json")

        self.assertEqual(response.status_code, 403)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "pending_shipment")

    def test_ship_requires_company_tracking_and_remark(self):
        self.client.force_authenticate(self.staff)

        response = self.client.post(
            f"/api/orders/{self.order.id}/ship/",
            {"express_company": "SF Express"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "express_company/express_no/shipping_remark are required")

    def test_customer_logistics_uses_real_shipping_data(self):
        self.order.status = "pending_receipt"
        self.order.express_company = "SF Express"
        self.order.express_no = "SF1234567890"
        self.order.shipped_at = self.order.created_at
        self.order.save(update_fields=["status", "express_company", "express_no", "shipped_at", "updated_at"])

        self.client.force_authenticate(self.customer)
        response = self.client.get(f"/api/orders/{self.order.id}/logistics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["company"], "SF Express")
        self.assertEqual(response.data["data"]["tracking_no"], "SF1234567890")
        self.assertEqual(len(response.data["data"]["timeline"]), 2)

    def test_order_cannot_start_refund_twice(self):
        self.order.status = "completed"
        self.order.aftersale_used = True
        self.order.save(update_fields=["status", "aftersale_used", "updated_at"])

        self.client.force_authenticate(self.customer)
        response = self.client.post(f"/api/orders/{self.order.id}/refund/", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "refund already used")

    def test_customer_logistics_compatibility_fields_are_present(self):
        self.order.status = "pending_receipt"
        self.order.express_company = "SF Express"
        self.order.express_no = "SF1234567890"
        self.order.shipped_at = self.order.created_at
        self.order.save(update_fields=["status", "express_company", "express_no", "shipped_at", "updated_at"])

        self.client.force_authenticate(self.customer)
        response = self.client.get(f"/api/orders/{self.order.id}/logistics/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["company"], "SF Express")
        self.assertEqual(response.data["data"]["tracking_no"], "SF1234567890")
        self.assertEqual(response.data["data"]["express_company"], "SF Express")
        self.assertEqual(response.data["data"]["express_no"], "SF1234567890")
        self.assertEqual(response.data["data"]["timeline"], response.data["data"]["traces"])


class OrderAdminShippingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            password="pwd123456",
            email="admin@example.com",
        )
        self.customer = User.objects.create_user(username="buyer", password="pwd123456")
        self.address = Address.objects.create(
            user=self.customer,
            name="Buyer",
            address="Shanghai Road 1",
            phone_number="13800000000",
            is_default=True,
        )
        self.order = Order.objects.create(
            user=self.customer,
            address=self.address,
            status="pending_shipment",
        )
        self.client.force_login(self.admin_user)

    def test_admin_ship_form_page_renders(self):
        response = self.client.get(reverse("admin:orders_order_ship", args=[self.order.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "express_company")
        self.assertContains(response, "express_no")
        self.assertContains(response, "shipping_remark")

    def test_admin_can_submit_ship_form(self):
        response = self.client.post(
            reverse("admin:orders_order_ship", args=[self.order.id]),
            {
                "express_company": "SF Express",
                "express_no": "SF1234567890",
                "shipping_remark": "Leave at service desk",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("admin:orders_order_changelist"))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "pending_receipt")
        self.assertEqual(self.order.express_company, "SF Express")
        self.assertEqual(self.order.express_no, "SF1234567890")
        self.assertEqual(self.order.shipping_remark, "Leave at service desk")
        self.assertIsNotNone(self.order.shipped_at)

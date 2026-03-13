from django.db import models
from django.contrib.auth.models import User

from users.models import Address
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending_payment", "待支付"),
        ("pending_shipment", "待发货"),
        ("pending_receipt", "待收货"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
        ("refund_processing", "售后中")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending_payment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_TRANSITIONS = {
        "pending_payment": ["pending_shipment", "cancelled"],
        "pending_shipment": ["pending_receipt", "cancelled"],
        "pending_receipt": ["completed", "cancelled", "refund_processing"],
        "completed": ["refund_processing"],
        "refund_processing": ["completed", "cancelled"],
        "cancelled": [],
    }

    def __str__(self):
        return f"订单 {self.id} - {self.status}"

    def change_status(self, new_status):
        if self.status == "cancelled":
            raise ValueError(f"Cannot change status from {self.status}")

        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")

        if new_status not in self.STATUS_TRANSITIONS[self.status]:
            raise ValueError(f"Invalid transition: {self.status} -> {new_status}")

        self.status = new_status
        self.save(update_fields=["status", "updated_at"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

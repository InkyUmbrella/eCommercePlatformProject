from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from products.models import Category, Product, ProductImage, ProductSpecification


class ProductApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Skincare", sort_order=1)
        self.product = Product.objects.create(
            category=self.category,
            name="Essence",
            brand="Lancome",
            sku="LAN-ESS-001",
            short_description="Repair essence",
            price="299.00",
            stock=50,
            is_active=True,
            description="Deep repair",
        )

    def test_product_detail_returns_images_and_specifications(self):
        image_file = SimpleUploadedFile("detail.jpg", b"filecontent", content_type="image/jpeg")
        ProductImage.objects.create(product=self.product, image=image_file, sort_order=1)
        ProductSpecification.objects.create(product=self.product, name="容量", value="30ml", sort_order=1)

        response = self.client.get(f"/api/products/{self.product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["sku"], "LAN-ESS-001")
        self.assertEqual(response.data["data"]["brand"], "Lancome")
        self.assertEqual(len(response.data["data"]["images"]), 1)
        self.assertEqual(len(response.data["data"]["specifications"]), 1)

    def test_product_list_supports_brand_filter(self):
        response = self.client.get("/api/products/", {"brand": "Lancome"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["count"], 1)

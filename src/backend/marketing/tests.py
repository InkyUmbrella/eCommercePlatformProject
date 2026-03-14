from django.test import TestCase
from rest_framework.test import APIClient

from marketing.models import Banner, HotRecommend
from products.models import Category, Product


class MarketingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Makeup", sort_order=1)
        self.product = Product.objects.create(
            category=self.category,
            name="Lipstick",
            price="199.00",
            stock=20,
            is_active=True,
            description="Best seller",
        )

    def test_banners_endpoint_returns_configured_banners(self):
        Banner.objects.create(
            title="Spring Sale",
            subtitle="Limited offer",
            link="/product-detail/1",
            sort_order=1,
            is_active=True,
        )

        response = self.client.get("/api/home/banners/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["title"], "Spring Sale")

    def test_banner_prefers_product_link_when_product_selected(self):
        banner = Banner.objects.create(
            title="Spring Sale",
            subtitle="Limited offer",
            link="/legacy-link",
            product=self.product,
            sort_order=1,
            is_active=True,
        )

        response = self.client.get("/api/home/banners/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"][0]["id"], banner.id)
        self.assertEqual(response.data["data"][0]["link"], f"/product-detail/{self.product.id}")
        self.assertEqual(response.data["data"][0]["product_id"], self.product.id)

    def test_banner_auto_matches_product_by_same_title(self):
        banner = Banner.objects.create(
            title="Lipstick",
            subtitle="Limited offer",
            sort_order=1,
            is_active=True,
        )

        banner.refresh_from_db()
        self.assertEqual(banner.product_id, self.product.id)

    def test_hot_recommends_endpoint_returns_curated_products(self):
        HotRecommend.objects.create(product=self.product, title="Home Pick", sort_order=1, is_active=True)

        response = self.client.get("/api/home/hot-recommends/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["id"], self.product.id)
        self.assertEqual(response.data["data"][0]["recommend_title"], "Home Pick")

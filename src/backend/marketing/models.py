from django.db import models
from django.db.models import Case, IntegerField, Value, When


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    subtitle = models.CharField(max_length=200, blank=True, default="", verbose_name="副标题")
    image = models.ImageField(upload_to="marketing/banners/", blank=True, null=True, verbose_name="图片")
    link = models.CharField(max_length=255, blank=True, default="", verbose_name="跳转链接")
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="banners",
        verbose_name="对应商品",
    )
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["sort_order", "-id"]
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.product_id and self.title:
            from products.models import Product

            matched_product = (
                Product.objects.filter(name=self.title)
                .annotate(
                    active_priority=Case(
                        When(is_active=True, then=Value(0)),
                        default=Value(1),
                        output_field=IntegerField(),
                    )
                )
                .order_by("active_priority", "id")
                .first()
            )
            if matched_product:
                self.product = matched_product
        super().save(*args, **kwargs)


class HotRecommend(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="hot_recommends", verbose_name="商品")
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="推荐标题")
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ["sort_order", "-id"]
        unique_together = ("product", "title")
        verbose_name = "热门推荐"
        verbose_name_plural = "热门推荐"

    def __str__(self):
        return self.title or self.product.name

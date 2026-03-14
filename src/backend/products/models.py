from django.db import models


class Category(models.Model):
    name = models.CharField("分类名称", max_length=50)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="父级分类",
    )
    sort_order = models.IntegerField("排序", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="所属分类",
    )
    name = models.CharField("商品名称", max_length=200)
    brand = models.CharField("品牌", max_length=100, blank=True, default="")
    sku = models.CharField("SKU编码", max_length=50, blank=True, default="")
    short_description = models.CharField("短描述", max_length=200, blank=True, default="")
    price = models.DecimalField("价格", max_digits=10, decimal_places=2)
    stock = models.IntegerField("库存", default=0)
    is_active = models.BooleanField("上架", default=True)
    cover_image = models.ImageField(
        "封面图",
        upload_to="products/covers/",
        blank=True,
        null=True,
    )
    description = models.TextField("商品描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="商品",
    )
    image = models.ImageField("图片", upload_to="products/detail/")
    sort_order = models.IntegerField("排序", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.product.name} 的图片"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
        verbose_name="商品",
    )
    name = models.CharField("规格名称", max_length=50)
    value = models.CharField("规格值", max_length=100)
    sort_order = models.IntegerField("排序", default=0)

    class Meta:
        verbose_name = "商品规格"
        verbose_name_plural = "商品规格"
        ordering = ["sort_order", "id"]
        unique_together = ("product", "name", "value")

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

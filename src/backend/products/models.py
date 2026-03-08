from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """商品分类"""
    name = models.CharField('分类名称', max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父级分类'
    )
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品"""
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='所属分类'
    )
    name = models.CharField('商品名称', max_length=200)
    
    # SKU相关字段
    sku = models.CharField('SKU编码', max_length=50, unique=True, blank=True, null=True, 
                          help_text='商品库存单位编码，如IPHONE15-BLACK-256')
    brand = models.CharField('品牌', max_length=100, blank=True)
    model = models.CharField('型号', max_length=100, blank=True, help_text='如 iPhone 15')
    
    # 价格和库存
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    market_price = models.DecimalField('市场价', max_digits=10, decimal_places=2, 
                                       blank=True, null=True, help_text='划线价')
    cost_price = models.DecimalField('成本价', max_digits=10, decimal_places=2, 
                                     blank=True, null=True, help_text='用于计算利润')
    stock = models.IntegerField('库存', default=0, validators=[MinValueValidator(0)])
    stock_warning = models.IntegerField('库存预警', default=0, 
                                        help_text='低于此值显示库存紧张')
    
    # 商品属性
    is_active = models.BooleanField('上架', default=True)
    is_new = models.BooleanField('新品', default=False)
    is_hot = models.BooleanField('热卖', default=False)
    is_recommend = models.BooleanField('推荐', default=False)
    
    # 媒体文件
    cover_image = models.ImageField(
        '封面图',
        upload_to='products/covers/',
        blank=True,
        null=True
    )
    video_url = models.URLField('视频地址', blank=True, help_text='商品介绍视频链接')
    
    # 详细描述
    description = models.TextField('商品描述', blank=True)
    short_description = models.CharField('短描述', max_length=200, blank=True, 
                                        help_text='用于列表页显示的简短描述')
    specifications = models.JSONField('规格参数', blank=True, null=True, 
                                     help_text='JSON格式存储规格参数')
    
    # 销售信息
    sales_count = models.IntegerField('销量', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    rating = models.FloatField('评分', default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField('评论数', default=0)
    
    # 时间信息
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('上架时间', blank=True, null=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # 自动生成SKU（如果没有提供）
        if not self.sku:
            import uuid
            # 生成格式：SKU-8位随机字符
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        # 上架时自动记录上架时间
        if self.is_active and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def is_out_of_stock(self):
        """是否缺货"""
        return self.stock <= 0
    
    @property
    def is_low_stock(self):
        """是否库存紧张"""
        return 0 < self.stock <= self.stock_warning


class ProductImage(models.Model):
    """商品图片"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='商品'
    )
    image = models.ImageField('图片', upload_to='products/detail/')
    sort_order = models.IntegerField('排序', default=0)
    is_main = models.BooleanField('是否主图', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        ordering = ['-is_main', 'sort_order']

    def __str__(self):
        return f"{self.product.name} 的图片"
    
    def save(self, *args, **kwargs):
        # 如果设置为主图，则将该商品的其他图片的主图标记取消
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)


class ProductSpecification(models.Model):
    """商品规格（简化SKU，如颜色、尺寸）"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specs',
        verbose_name='商品'
    )
    name = models.CharField('规格名称', max_length=50, help_text='如颜色、尺寸')
    value = models.CharField('规格值', max_length=100, help_text='如红色、XL')
    price_adjust = models.DecimalField('价格调整', max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField('库存', default=0)
    image = models.ImageField('规格图片', upload_to='products/specs/', blank=True, null=True)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '商品规格'
        verbose_name_plural = '商品规格'
        ordering = ['sort_order']
        unique_together = ['product', 'name', 'value']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}:{self.value}"
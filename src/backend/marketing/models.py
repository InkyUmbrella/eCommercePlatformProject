from django.db import models
from products.models import Product

class Banner(models.Model):
    """轮播图"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banners/', help_text='建议尺寸：1920x600像素')
    link = models.URLField('链接', blank=True, help_text='点击轮播图跳转的链接，可以是商品详情页或活动页')
    sort_order = models.IntegerField('排序', default=0, help_text='数字越小越靠前')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title

class HotRecommend(models.Model):
    """热门推荐"""
    RECOMMEND_TYPES = (
        ('home', '首页推荐'),
        ('category', '分类页推荐'),
        ('detail', '详情页推荐'),
    )
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='recommends',
        verbose_name='推荐商品'
    )
    recommend_type = models.CharField('推荐类型', max_length=20, choices=RECOMMEND_TYPES, default='home')
    sort_order = models.IntegerField('排序', default=0, help_text='数字越小越靠前')
    is_active = models.BooleanField('是否启用', default=True)
    start_date = models.DateTimeField('开始时间', null=True, blank=True)
    end_date = models.DateTimeField('结束时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '热门推荐'
        verbose_name_plural = '热门推荐'
        ordering = ['recommend_type', 'sort_order']
        unique_together = ['product', 'recommend_type']  # 同一类型下不重复推荐同一商品

    def __str__(self):
        return f"{self.get_recommend_type_display()} - {self.product.name}"

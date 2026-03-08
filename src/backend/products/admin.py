from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Product, ProductImage, ProductSpecification

class ProductImageInline(admin.TabularInline):
    """商品图片内联"""
    model = ProductImage
    extra = 3
    fields = ('image', 'sort_order', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "暂无图片"
    image_preview.short_description = '预览'

class ProductSpecInline(admin.TabularInline):
    """商品规格内联"""
    model = ProductSpecification
    extra = 2
    fields = ('name', 'value', 'price_adjust', 'stock', 'image', 'sort_order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'sort_order', 'product_count', 'created_at')
    list_editable = ('sort_order',)
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} if hasattr(Category, 'slug') else {}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = '商品数量'
    product_count.admin_order_field = 'products_count'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = (
        'id', 'name', 'category', 'sku', 'price', 'stock', 
        'sales_count', 'view_count', 'cover_image_preview',
        'is_active', 'is_new', 'is_hot', 'created_at'
    )
    list_editable = ('price', 'stock', 'is_active', 'is_new', 'is_hot')
    list_filter = ('category', 'is_active', 'is_new', 'is_hot', 'created_at')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('created_at', 'updated_at', 'view_count', 'sales_count', 'cover_image_preview')
    
    # 字段分组
    fieldsets = (
        ('基本信息', {
            'fields': (
                'category', 'name', 'sku', 'brand', 'model',
                ('is_active', 'is_new', 'is_hot', 'is_recommend')
            )
        }),
        ('价格库存', {
            'fields': (
                ('price', 'market_price', 'cost_price'),
                ('stock', 'stock_warning'),
                ('sales_count', 'view_count')
            )
        }),
        ('媒体文件', {
            'fields': ('cover_image', 'cover_image_preview', 'video_url')
        }),
        ('描述信息', {
            'fields': ('short_description', 'description', 'specifications')
        }),
        ('评分统计', {
            'fields': ('rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    # 内联
    inlines = [ProductImageInline, ProductSpecInline]
    
    # 列表页操作
    actions = ['make_active', 'make_inactive', 'make_new', 'make_hot', 'clone_product']
    
    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.cover_image.url)
        return "暂无图片"
    cover_image_preview.short_description = '封面预览'
    
    def make_active(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_active=True, published_at=timezone.now())
        self.message_user(request, f'{updated} 个商品已上架')
    make_active.short_description = '批量上架'
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} 个商品已下架')
    make_inactive.short_description = '批量下架'
    
    def make_new(self, request, queryset):
        updated = queryset.update(is_new=True)
        self.message_user(request, f'{updated} 个商品标记为新品')
    make_new.short_description = '标记为新品'
    
    def make_hot(self, request, queryset):
        updated = queryset.update(is_hot=True)
        self.message_user(request, f'{updated} 个商品标记为热卖')
    make_hot.short_description = '标记为热卖'
    
    def clone_product(self, request, queryset):
        """复制商品"""
        for product in queryset:
            product.pk = None
            product.name = f"{product.name} (复制)"
            product.sku = None
            product.sales_count = 0
            product.view_count = 0
            product.save()
        self.message_user(request, f'{queryset.count()} 个商品已复制')
    clone_product.short_description = '复制商品'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_preview', 'is_main', 'sort_order')
    list_editable = ('is_main', 'sort_order')
    list_filter = ('product', 'is_main')
    search_fields = ('product__name',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "暂无图片"
    image_preview.short_description = '预览'

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'value', 'price_adjust', 'stock', 'sort_order')
    list_editable = ('price_adjust', 'stock', 'sort_order')
    list_filter = ('product', 'name')
    search_fields = ('product__name', 'value')
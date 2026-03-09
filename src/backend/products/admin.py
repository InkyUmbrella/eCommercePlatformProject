﻿from django.contrib import admin
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
    # 列表显示字段 - 添加 status_badge
    list_display = (
        'id', 'name', 'category', 'sku', 'price', 'stock', 
        'sales_count', 'view_count', 'cover_image_preview',
        'status_badge',  # 状态标签
        'is_active', 'is_new', 'is_hot', 'created_at'
    )
    list_editable = ('price', 'stock', 'is_active', 'is_new', 'is_hot')
    list_filter = ('category', 'is_active', 'is_new', 'is_hot', 'created_at')
    search_fields = ('name', 'sku', 'description', 'brand')
    readonly_fields = ('created_at', 'updated_at', 'view_count', 'sales_count', 'cover_image_preview', 'status_display')
    
    # 字段分组
    fieldsets = (
        ('基本信息', {
            'fields': (
                'category', 'name', 'sku', 'brand', 'model',
                ('is_active', 'status_display'),
                ('is_new', 'is_hot', 'is_recommend')
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
    
    # ===== 状态标签相关方法 =====
    def status_badge(self, obj):
        """显示上下架状态标签"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #4caf50; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 12px; font-weight: bold;">✓ 已上架</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #9e9e9e; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 12px; font-weight: bold;">✗ 已下架</span>'
            )
    status_badge.short_description = '状态'
    status_badge.admin_order_field = 'is_active'
    
    def status_display(self, obj):
        """详情页状态显示"""
        if obj.is_active:
            return format_html(
                '<span style="color: #4caf50; font-size: 14px;">✓ 已上架</span><br>'
                '<small>上架时间: {}</small>',
                obj.published_at or '-'
            )
        else:
            return format_html(
                '<span style="color: #9e9e9e; font-size: 14px;">✗ 已下架</span>'
            )
    status_display.short_description = '当前状态'
    
    # ===== 库存过滤器 =====
    class StockFilter(admin.SimpleListFilter):
        """库存状态过滤器"""
        title = '库存状态'
        parameter_name = 'stock_status'
        
        def lookups(self, request, model_admin):
            return (
                ('low', '库存紧张 (≤10)'),
                ('out', '缺货 (=0)'),
                ('normal', '库存充足 (>10)'),
            )
        
        def queryset(self, request, queryset):
            if self.value() == 'low':
                return queryset.filter(stock__gt=0, stock__lte=10)
            if self.value() == 'out':
                return queryset.filter(stock=0)
            if self.value() == 'normal':
                return queryset.filter(stock__gt=10)
            return queryset
    
    # ===== 重写 get_list_filter =====
    def get_list_filter(self, request):
        """动态添加过滤器"""
        return [
            'category',
            'is_active',
            'is_new',
            'is_hot',
            self.StockFilter,
            'brand',
            ('created_at', admin.DateFieldListFilter),
        ]
    
    # ===== 批量操作 =====
    actions = [
        'make_active', 
        'make_inactive', 
        'make_new', 
        'make_hot', 
        'clone_product',
        'export_products',
        'bulk_mark_as_recommend',
    ]
    
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
            old_images = list(product.images.all())
            old_specs = list(product.specs.all())
            
            product.pk = None
            product.name = f"{product.name} (复制)"
            product.sku = None
            product.sales_count = 0
            product.view_count = 0
            product.save()
            
            # 复制图片
            for image in old_images:
                image.pk = None
                image.product = product
                image.save()
            
            # 复制规格
            for spec in old_specs:
                spec.pk = None
                spec.product = product
                spec.save()
                
        self.message_user(request, f'{queryset.count()} 个商品已复制')
    clone_product.short_description = '复制商品'
    
    def export_products(self, request, queryset):
        """导出商品数据为CSV"""
        import csv
        from django.http import HttpResponse
        from django.utils import timezone
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="products_{timezone.now().date()}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', '名称', 'SKU', '品牌', '分类', '价格', '库存', '状态', '销量', '创建时间'])
        
        for product in queryset:
            writer.writerow([
                product.id,
                product.name,
                product.sku,
                product.brand,
                product.category.name,
                str(product.price),
                product.stock,
                '已上架' if product.is_active else '已下架',
                product.sales_count,
                product.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    export_products.short_description = '📊 导出商品数据'
    
    def bulk_mark_as_recommend(self, request, queryset):
        """批量标记为推荐"""
        count = queryset.update(is_recommend=True)
        self.message_user(request, f'成功标记 {count} 个商品为推荐')
    bulk_mark_as_recommend.short_description = '⭐ 批量标记推荐'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('images', 'specs')

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
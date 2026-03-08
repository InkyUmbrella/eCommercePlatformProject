from django.contrib import admin
from .models import Banner, HotRecommend

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """轮播图管理"""
    list_display = ('title', 'image_preview', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'image', 'image_preview', 'link')
        }),
        ('展示设置', {
            'fields': ('sort_order', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """图片预览"""
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px;"/>'
        return '暂无图片'
    image_preview.short_description = '图片预览'
    image_preview.allow_tags = True

@admin.register(HotRecommend)
class HotRecommendAdmin(admin.ModelAdmin):
    """热门推荐管理"""
    list_display = ('product', 'recommend_type', 'sort_order', 'is_active', 'start_date', 'end_date')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('recommend_type', 'is_active', 'created_at')
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)  # 需要 ProductAdmin 支持 autocomplete
    
    fieldsets = (
        ('推荐信息', {
            'fields': ('product', 'recommend_type', 'sort_order')
        }),
        ('状态设置', {
            'fields': ('is_active', 'start_date', 'end_date')
        }),
    )

from django.contrib import admin
from .models import Banner, HotRecommend

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """轮播图管理"""
    list_display = ('title', 'image_preview', 'sort_order', 'status_badge', 'created_at')
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
   
    # 添加状态标签
    def status_badge(self, obj):
        """状态标签"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #4caf50; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✓ 启用</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #9e9e9e; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✗ 禁用</span>'
            )
    status_badge.short_description = '状态'
    
    # 添加批量操作
    actions = ['enable_banners', 'disable_banners']
    
    def enable_banners(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'已启用 {count} 个轮播图')
    enable_banners.short_description = '启用所选轮播图'
    
    def disable_banners(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'已禁用 {count} 个轮播图')
    disable_banners.short_description = '禁用所选轮播图'

@admin.register(HotRecommend)
class HotRecommendAdmin(admin.ModelAdmin):
    """热门推荐管理"""
    list_display = ('product', 'recommend_type', 'sort_order', 'status_badge', 'start_date', 'end_date')
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

# 添加状态标签
    def status_badge(self, obj):
        """状态标签"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #4caf50; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✓ 启用</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #9e9e9e; color: white; padding: 3px 8px; '
                'border-radius: 3px;">✗ 禁用</span>'
            )
    status_badge.short_description = '状态'

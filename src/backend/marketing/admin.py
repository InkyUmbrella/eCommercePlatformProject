from django.contrib import admin

from .models import Banner, HotRecommend


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sort_order", "is_active", "created_at")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "subtitle", "link")
    list_filter = ("is_active",)


@admin.register(HotRecommend)
class HotRecommendAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "title", "sort_order", "is_active", "created_at")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "product__name")
    list_filter = ("is_active",)
    autocomplete_fields = ("product",)

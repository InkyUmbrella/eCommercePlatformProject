from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, ProductSpecification

admin.site.site_header = "电商后台管理"
admin.site.site_title = "电商后台"
admin.site.index_title = "管理面板"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("created_at",)
    fields = ("image", "sort_order", "created_at")


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ("name", "value", "sort_order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "sort_order", "created_at")
    list_filter = ("parent",)
    search_fields = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("parent")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline, ProductSpecificationInline)
    list_display = ("id", "name", "brand", "sku", "category", "price", "stock", "is_active", "created_at")
    list_display_links = ("name",)
    list_editable = ("stock", "is_active")
    list_filter = ("category", "brand", "is_active")
    search_fields = ("name", "brand", "sku", "description", "short_description")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    list_select_related = ("category",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image_tag", "sort_order", "created_at")
    list_filter = ("product",)
    readonly_fields = ("image_tag", "created_at")

    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.image.url)
        return "-"

    image_tag.short_description = "预览"


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "name", "value", "sort_order")
    list_filter = ("name",)
    search_fields = ("product__name", "name", "value")

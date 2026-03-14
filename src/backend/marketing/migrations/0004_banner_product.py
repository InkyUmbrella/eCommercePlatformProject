from django.db import migrations, models
import django.db.models.deletion


def fill_banner_product(apps, schema_editor):
    Banner = apps.get_model("marketing", "Banner")
    Product = apps.get_model("products", "Product")

    for banner in Banner.objects.filter(product__isnull=True).exclude(title=""):
        matched_product = (
            Product.objects.filter(name=banner.title)
            .order_by("-is_active", "id")
            .first()
        )
        if matched_product:
            banner.product_id = matched_product.id
            banner.save(update_fields=["product"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0009_product_catalog_fields"),
        ("marketing", "0003_banner_hotrecommend"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="banners",
                to="products.product",
                verbose_name="对应商品",
            ),
        ),
        migrations.RunPython(fill_banner_product, migrations.RunPython.noop),
    ]

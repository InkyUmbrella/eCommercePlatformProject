from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_alter_productspecification_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, default="", max_length=100, verbose_name="品牌"),
        ),
        migrations.AddField(
            model_name="product",
            name="short_description",
            field=models.CharField(blank=True, default="", max_length=200, verbose_name="短描述"),
        ),
        migrations.AddField(
            model_name="product",
            name="sku",
            field=models.CharField(blank=True, default="", max_length=50, verbose_name="SKU"),
        ),
        migrations.CreateModel(
            name="ProductSpecification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="规格名称")),
                ("value", models.CharField(max_length=100, verbose_name="规格值")),
                ("sort_order", models.IntegerField(default=0, verbose_name="排序")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="products.product",
                        verbose_name="商品",
                    ),
                ),
            ],
            options={
                "verbose_name": "商品规格",
                "verbose_name_plural": "商品规格",
                "ordering": ["sort_order", "id"],
                "unique_together": {("product", "name", "value")},
            },
        ),
    ]

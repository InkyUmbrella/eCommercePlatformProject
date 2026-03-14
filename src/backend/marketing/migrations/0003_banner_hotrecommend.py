from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_alter_productspecification_unique_together_and_more"),
        ("marketing", "0002_delete_banner_delete_hotrecommend"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("subtitle", models.CharField(blank=True, default="", max_length=200)),
                ("image", models.ImageField(blank=True, null=True, upload_to="marketing/banners/")),
                ("link", models.CharField(blank=True, default="", max_length=255)),
                ("sort_order", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["sort_order", "-id"]},
        ),
        migrations.CreateModel(
            name="HotRecommend",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, default="", max_length=100)),
                ("sort_order", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hot_recommends",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order", "-id"],
                "unique_together": {("product", "title")},
            },
        ),
    ]

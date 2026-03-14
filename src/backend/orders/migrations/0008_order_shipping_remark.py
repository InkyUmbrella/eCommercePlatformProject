from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0007_order_aftersale_used"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="shipping_remark",
            field=models.CharField(blank=True, default="", max_length=255, verbose_name="发货备注"),
        ),
    ]

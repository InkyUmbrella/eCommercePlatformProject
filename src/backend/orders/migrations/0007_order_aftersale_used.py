from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_order_shipping_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="aftersale_used",
            field=models.BooleanField(default=False, verbose_name="是否已申请过售后"),
        ),
    ]

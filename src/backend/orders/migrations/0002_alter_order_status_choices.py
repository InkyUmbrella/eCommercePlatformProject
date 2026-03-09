# Generated manually for status choices update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending_payment", "Pending Payment"),
                    ("pending_shipment", "Pending Shipment"),
                    ("pending_receipt", "Pending Receipt"),
                    ("refund_processing", "Refund Processing"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending_payment",
                max_length=20,
            ),
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    # slug already exists in 0001_initial, so this migration is intentionally a no-op.
    operations = []

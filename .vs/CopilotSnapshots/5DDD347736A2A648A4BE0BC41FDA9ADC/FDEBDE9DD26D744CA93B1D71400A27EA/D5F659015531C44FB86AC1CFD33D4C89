from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        base = slugify(product.name)[:195]
        slug = base
        counter = 1
        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f"{base}-{counter}"
            counter += 1
        product.slug = slug
        product.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_add_slug_nullable'),
    ]

    operations = [
        migrations.RunPython(generate_slugs),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    selected = models.BooleanField(default=True, verbose_name='是否选中')

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = '购物车项'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

# Create your models here.

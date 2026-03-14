from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='收货人')
    address = models.TextField(verbose_name='详细地址')
    phone_number = models.TextField(max_length=20, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='默认地址')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址'

    def __str__(self):
        return f'{self.name} - {self.address} - {self.phone_number}'

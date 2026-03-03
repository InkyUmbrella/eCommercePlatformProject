from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='addresses')
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.TextField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.address} - {self.phone_number}'
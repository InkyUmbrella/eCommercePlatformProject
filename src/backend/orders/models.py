from django.db import models
from django.contrib.auth.models import User

from users.models import Address


class Order(models.Model):
    STATUS_CHOICES = (
    ('pending_payment', '待支付'),
    ('pending_shipment','待发货'),
    ('pending_receipt','待收货'),
    ('completed','已完成'),
    ('cancelled','已取消'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'订单 {self.id} - {self.status}'

    # 定义状态转换规则
    STATUS_TRANSITIONS = {
        'pending_payment': ['pending_shipment', 'cancelled'],      # 待支付 -> 待发货 或 已取消
        'pending_shipment': ['pending_receipt', 'cancelled'],     # 待发货 -> 待收货 或 已取消
        'pending_receipt': ['completed', 'cancelled'],   # 待收货 -> 已完成 或 已取消
        'completed': [],                          # 已完成不能再转其他状态
        'cancelled': [],                          # 已取消不能再转其他状态
    }

    def change_status(self, new_status):
        # 校验当前状态是否能改变
        if self.status == 'cancelled':
            raise ValueError(f"Cannot change status from {self.status}")

        # 校验新状态是否有效
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")

        # 校验是否符合当前状态的流转规则
        if new_status not in self.STATUS_TRANSITIONS[self.status]:
            raise ValueError(f"Invalid transition: {self.status} -> {new_status}")

        # 如果校验通过，更新状态
        self.status = new_status
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
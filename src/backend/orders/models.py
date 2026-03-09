from django.db import models
from django.contrib.auth.models import User

from users.models import Address
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
    ('pending_payment', '待支付'),
    ('pending_shipment','待发货'),
    ('pending_receipt','待收货'),
    ('completed','已完成'),
    ('cancelled','已取消'),
    ('refund_processing','售后中')
    )

# 新增：物流公司选项
    SHIPPING_COMPANIES = (
        ('SF', '顺丰速运'),
        ('EMS', 'EMS'),
        ('STO', '申通快递'),
        ('YTO', '圆通速递'),
        ('ZTO', '中通快递'),
        ('YUNDA', '韵达快递'),
        ('JD', '京东物流'),
        ('OTHER', '其他物流'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')

# ===== 新增：发货相关字段 =====
    shipping_company = models.CharField('物流公司', max_length=20, choices=SHIPPING_COMPANIES, blank=True, null=True)
    shipping_code = models.CharField('物流单号', max_length=50, blank=True)
    shipping_time = models.DateTimeField('发货时间', blank=True, null=True)
    shipping_remark = models.CharField('发货备注', max_length=200, blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'订单 {self.id} - {self.status}'

    # 定义状态转换规则
    STATUS_TRANSITIONS = {
        'pending_payment': ['pending_shipment', 'cancelled'],    # 待支付 -> 待发货 或 已取消
        'pending_shipment': ['pending_receipt', 'cancelled'],    # 待发货 -> 待收货 或 已取消
        'pending_receipt': ['completed', 'refund_processing'],   # 待收货 -> 已完成 或 售后中
        'completed': ['refund_processing'],                      # 已完成 -> 售后中
        'cancelled': [],                                         # 已取消不能再转其他状态
        'refund_processing': ['completed', 'cancelled']          # 售后中 -> 已完成 或 已取消
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

    # ===== 新增：发货方法 =====
    def ship(self, shipping_company, shipping_code, shipping_remark=''):
        """发货操作"""
        from django.utils import timezone
        
        # 检查状态是否为待发货（注意字段名是 pending_shipment）
        if self.status != 'pending_shipment':
            raise ValueError(f"订单状态错误，当前状态：{self.get_status_display()}，不能发货")
        
        self.status = 'pending_receipt'
        self.shipping_company = shipping_company
        self.shipping_code = shipping_code
        self.shipping_remark = shipping_remark
        self.shipping_time = timezone.now()
        self.save()
        
        return True
    
    # ===== 新增：属性方法 =====
    @property
    def is_shipped(self):
        """是否已发货"""
        return self.shipping_time is not None
    
    @property
    def shipping_info(self):
        """发货信息"""
        if self.shipping_time:
            return {
                'company': self.get_shipping_company_display(),
                'code': self.shipping_code,
                'time': self.shipping_time,
                'remark': self.shipping_remark,
            }
        return None

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

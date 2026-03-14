from django.db import models
from django.contrib.auth.models import User

from users.models import Address
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending_payment", "待支付"),
        ("pending_shipment", "待发货"),
        ("pending_receipt", "待收货"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
        ("refund_processing", "售后中")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending_payment")
    aftersale_used = models.BooleanField("是否已申请过售后", default=False)
    express_company = models.CharField("物流公司", max_length=50, blank=True, default="")
    express_no = models.CharField("物流单号", max_length=64, blank=True, default="")
    shipping_remark = models.CharField("发货备注", max_length=255, blank=True, default="")
    shipped_at = models.DateTimeField("发货时间", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    STATUS_TRANSITIONS = {
        "pending_payment": ["pending_shipment", "cancelled"],
        "pending_shipment": ["pending_receipt", "cancelled"],
        "pending_receipt": ["completed", "cancelled", "refund_processing"],
        "completed": ["refund_processing"],
        "refund_processing": ["completed", "cancelled"],
        "cancelled": [],
    }

    def __str__(self):
        return f"订单 {self.id} - {self.status}"

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def change_status(self, new_status):
        if self.status == "cancelled":
            raise ValueError(f"Cannot change status from {self.status}")

        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")

        if new_status not in self.STATUS_TRANSITIONS[self.status]:
            raise ValueError(f"Invalid transition: {self.status} -> {new_status}")

        self.status = new_status
        self.save(update_fields=["status", "updated_at"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="成交价")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

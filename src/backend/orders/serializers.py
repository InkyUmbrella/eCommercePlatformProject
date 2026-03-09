from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.cover_image', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'price', 'quantity', 'total']

class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    shipping_company_display = serializers.CharField(source='get_shipping_company_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'status', 'status_display',
            'total_amount', 'pay_amount', 'shipping_amount',
            'payment_method', 'payment_method_display',
            'shipping_company', 'shipping_company_display', 'shipping_code',
            'shipping_time', 'shipping_remark',
            'receiver_name', 'receiver_phone',
            'receiver_province', 'receiver_city', 'receiver_district', 'receiver_address',
            'buyer_message', 'seller_message',
            'items', 'created_at', 'paid_at', 'shipping_time', 'completed_at'
        ]

class ShipOrderSerializer(serializers.Serializer):
    """发货序列化器"""
    shipping_company = serializers.ChoiceField(choices=Order.SHIPPING_COMPANIES, required=True)
    shipping_code = serializers.CharField(max_length=50, required=True)
    shipping_remark = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    def validate(self, data):
        """验证订单是否可以发货"""
        order = self.context.get('order')
        if not order:
            raise serializers.ValidationError("订单不存在")
        
        if order.status != 'PENDING_SHIP':
            raise serializers.ValidationError(f"订单状态错误，当前状态：{order.get_status_display()}，不能发货")
        
        return data
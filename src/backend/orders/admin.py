from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """订单商品内联"""
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'total', 'product_info')
    fields = ('product_info', 'price', 'quantity', 'total')
    can_delete = False
    
    def product_info(self, obj):
        if obj.product:
            return format_html(
                '<strong>{}</strong><br>'
                '<small>SKU: {}</small>',
                obj.product.name,
                getattr(obj.product, 'sku', '无')
            )
        return "商品已删除"
    product_info.short_description = '商品信息'
    
    def total(self, obj):
        return obj.price * obj.quantity
    total.short_description = '小计'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_no', 'user', 'total_amount', 'pay_amount',
        'status_colored', 'payment_method_display', 'shipping_status',
        'item_count_display',
        'created_at'
    )
    list_filter = (
        'status', 
        'payment_method', 
        'shipping_company', 
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = (
        'order_no', 
        'user__username', 
        'receiver_name', 
        'receiver_phone',
        'shipping_code',
    )
    readonly_fields = (
        'order_no', 'total_amount', 'pay_amount', 'paid_at',
        'created_at', 'updated_at', 'shipping_time'
    )
    inlines = [OrderItemInline]
    
    # 字段分组
    fieldsets = (
        ('订单基本信息', {
            'fields': (
                'order_no', 'user', 'status', 'payment_method',
                ('total_amount', 'pay_amount', 'discount_amount', 'shipping_amount')
            )
        }),
        ('收货信息', {
            'fields': (
                'receiver_name', 'receiver_phone',
                'receiver_province', 'receiver_city', 'receiver_district',
                'receiver_address', 'receiver_zip'
            )
        }),
        ('发货信息', {
            'fields': (
                ('shipping_company', 'shipping_code'),
                'shipping_remark',
                'shipping_time',
            ),
            'classes': ('wide',)
        }),
        ('备注信息', {
            'fields': ('buyer_message', 'seller_message')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'cancelled_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """优化查询性能"""
        return super().get_queryset(request).select_related(
            'user'
        ).prefetch_related(
            'order_items__product'
        ).annotate(
            item_count=Count('order_items')
        )
    
    def order_no(self, obj):
        """订单号"""
        return f"ORD{obj.id:08d}"
    order_no.short_description = '订单号'

    def status_colored(self, obj):
        """带颜色的状态显示"""
        colors = {
            'pending_payment': 'orange',
            'pending_shipment': 'blue',
            'pending_receipt': 'purple',
            'completed': 'green',
            'cancelled': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = '订单状态'
    status_colored.admin_order_field = 'status'
    
    def payment_method_display(self, obj):
        """支付方式显示"""
        if obj.payment_method:
            return obj.get_payment_method_display()
        return '-'
    payment_method_display.short_description = '支付方式'
    
    def shipping_status(self, obj):
        """发货状态显示"""
        if obj.shipping_time:
            return format_html(
                '<span style="color: green;">✓ 已发货</span><br>'
                '<small>{} {}</small>',
                obj.get_shipping_company_display() or '',
                obj.shipping_code or ''
            )
        elif obj.status == 'pending_shipment':
            return format_html(
                '<span style="color: orange; font-weight: bold;">⏳ 待发货</span>'
            )
        else:
            return '-'
    shipping_status.short_description = '发货状态'
    
    def item_count_display(self, obj):
        """商品数量显示"""
        count = getattr(obj, 'item_count', obj.order_items.count())
        return format_html(
            '<span title="商品数量">{}</span>',
            count
        )
    item_count_display.short_description = '商品数'
    item_count_display.admin_order_field = 'item_count'
    
    # 批量操作
    actions = ['ship_selected_orders', 'export_orders']
    
    def ship_selected_orders(self, request, queryset):
        """批量发货"""
        pending_orders = queryset.filter(status='pending_shipment')
        count = pending_orders.count()
        
        if count == 0:
            self.message_user(request, '没有选中的待发货订单', level='WARNING')
            return
        
        if count == 1:
            order = pending_orders.first()
            return HttpResponseRedirect(
                reverse('admin:ship-order', args=[order.id])
            )
        
        return HttpResponseRedirect(
            f"{reverse('admin:bulk-ship-orders')}?ids={','.join([str(o.id) for o in pending_orders])}"
        )
    ship_selected_orders.short_description = '发货所选订单'
    
    def export_orders(self, request, queryset):
        """导出订单数据"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="orders.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['订单号', '用户', '金额', '状态', '收货人', '电话', '地址', '物流公司', '物流单号'])
        
        for order in queryset:
            writer.writerow([
                f"ORD{order.id:08d}",
                order.user.username,
                order.pay_amount,
                order.get_status_display(),
                order.receiver_name,
                order.receiver_phone,
                f"{order.receiver_province} {order.receiver_city} {order.receiver_district} {order.receiver_address}",
                order.get_shipping_company_display() or '',
                order.shipping_code or ''
            ])
        
        return response
    export_orders.short_description = '导出订单CSV'
    
    # 自定义URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'ship-order/<int:order_id>/',
                self.admin_site.admin_view(self.ship_order_view),
                name='ship-order',
            ),
            path(
                'bulk-ship-orders/',
                self.admin_site.admin_view(self.bulk_ship_orders_view),
                name='bulk-ship-orders',
            ),
        ]
        return custom_urls + urls
    
    def ship_order_view(self, request, order_id):
        """单个订单发货页面"""
        from django import forms
        
        class ShipForm(forms.Form):
            shipping_company = forms.ChoiceField(
                label='物流公司',
                choices=Order.SHIPPING_COMPANIES,
                required=True
            )
            shipping_code = forms.CharField(
                label='物流单号',
                max_length=50,
                required=True
            )
            shipping_remark = forms.CharField(
                label='发货备注',
                max_length=200,
                required=False,
                widget=forms.Textarea(attrs={'rows': 2})
            )
        
        order = Order.objects.get(id=order_id)
        
        if request.method == 'POST':
            form = ShipForm(request.POST)
            if form.is_valid():
                try:
                    order.ship(
                        shipping_company=form.cleaned_data['shipping_company'],
                        shipping_code=form.cleaned_data['shipping_code'],
                        shipping_remark=form.cleaned_data['shipping_remark']
                    )
                    self.message_user(request, f'订单 ORD{order.id:08d} 发货成功')
                    return HttpResponseRedirect(reverse('admin:orders_order_changelist'))
                except ValueError as e:
                    self.message_user(request, str(e), level='ERROR')
        else:
            form = ShipForm()
        
        context = {
            'title': f'订单发货 - ORD{order.id:08d}',
            'order': order,
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/orders/ship_order.html', context)
    
    def bulk_ship_orders_view(self, request):
        """批量发货页面"""
        from django import forms
        
        class BulkShipForm(forms.Form):
            shipping_company = forms.ChoiceField(
                label='物流公司',
                choices=Order.SHIPPING_COMPANIES,
                required=True
            )
            shipping_remark = forms.CharField(
                label='发货备注',
                max_length=200,
                required=False,
                widget=forms.Textarea(attrs={'rows': 2})
            )
            order_ids = forms.CharField(widget=forms.HiddenInput())
        
        order_ids = request.GET.get('ids', '').split(',')
        orders = Order.objects.filter(id__in=order_ids, status='pending_shipment')
        
        if request.method == 'POST':
            form = BulkShipForm(request.POST)
            if form.is_valid():
                shipping_company = form.cleaned_data['shipping_company']
                shipping_remark = form.cleaned_data['shipping_remark']
                order_ids = form.cleaned_data['order_ids'].split(',')
                
                success_count = 0
                for order_id in order_ids:
                    try:
                        order = Order.objects.get(id=order_id, status='pending_shipment')
                        import uuid
                        shipping_code = f"SF{str(uuid.uuid4()).replace('-', '')[:12].upper()}"
                        order.ship(shipping_company, shipping_code, shipping_remark)
                        success_count += 1
                    except:
                        pass
                
                self.message_user(request, f'成功发货 {success_count} 个订单')
                return HttpResponseRedirect(reverse('admin:orders_order_changelist'))
        else:
            form = BulkShipForm(initial={'order_ids': ','.join([str(o.id) for o in orders])})
        
        context = {
            'title': '批量发货',
            'orders': orders,
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/orders/bulk_ship.html', context)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price', 'quantity', 'total')
    list_filter = ('order__status',)
    search_fields = ('order__order_no', 'product__name')
    
    def total(self, obj):
        return obj.price * obj.quantity
    total.short_description = '小计'
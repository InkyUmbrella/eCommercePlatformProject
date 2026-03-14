from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = (
        "id",
        "user",
        "status",
        "next_actions_preview",
        "action_buttons",
        "express_company",
        "express_no",
        "shipped_at",
        "created_at",
    )
    list_filter = ("status", "created_at", "shipped_at")
    search_fields = ("id", "user__username", "express_no")
    readonly_fields = ("created_at", "updated_at", "shipped_at", "next_actions_preview")
    actions = (
        "mark_as_paid",
        "mark_as_shipped",
        "mark_as_received",
        "approve_refund",
        "cancel_selected_orders",
    )

    class Media:
        css = {"all": ("orders/admin.css",)}

    @admin.display(description="下一步可操作")
    def next_actions_preview(self, obj):
        action_map = {
            "pending_payment": "标记已支付、取消订单",
            "pending_shipment": "一键发货、取消订单",
            "pending_receipt": "确认完成",
            "completed": "无可用操作",
            "refund_processing": "同意退款、取消订单",
            "cancelled": "无可用操作",
        }
        return action_map.get(obj.status, "无可用操作")

    @admin.display(description="快捷操作")
    def action_buttons(self, obj):
        buttons = []
        if obj.status == "pending_payment":
            buttons.append(self._action_link(obj, "pay", "标记已支付"))
            buttons.append(self._action_link(obj, "cancel", "取消订单"))
        elif obj.status == "pending_shipment":
            buttons.append(self._action_link(obj, "ship", "一键发货"))
            buttons.append(self._action_link(obj, "cancel", "取消订单"))
        elif obj.status == "pending_receipt":
            buttons.append(self._action_link(obj, "receive", "确认完成"))
        elif obj.status == "refund_processing":
            buttons.append(self._action_link(obj, "approve-refund", "同意退款"))
            buttons.append(self._action_link(obj, "cancel", "取消订单"))

        if not buttons:
            return "无"
        return mark_safe(" ".join(buttons))

    def _action_link(self, obj, action, label):
        url = reverse(f"admin:orders_order_{action}", args=[obj.pk])
        return (
            f'<a class="button" href="{url}" '
            'style="margin-right:6px;padding:4px 8px;border-radius:6px;'
            'background:#417690;color:#fff;text-decoration:none;">'
            f"{label}</a>"
        )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj and "status" in form.base_fields:
            status_field = form.base_fields["status"]
            status_label_map = dict(Order.STATUS_CHOICES)
            allowed_statuses = [obj.status, *Order.STATUS_TRANSITIONS.get(obj.status, [])]
            status_field.choices = [
                (status_code, status_label_map[status_code])
                for status_code in allowed_statuses
                if status_code in status_label_map
            ]
            status_field.help_text = "这里只显示当前状态允许流转到的下一步状态。"
        return form

    def get_urls(self):
        custom_urls = [
            path("<int:order_id>/pay/", self.admin_site.admin_view(self.process_pay), name="orders_order_pay"),
            path("<int:order_id>/ship/", self.admin_site.admin_view(self.process_ship), name="orders_order_ship"),
            path("<int:order_id>/receive/", self.admin_site.admin_view(self.process_receive), name="orders_order_receive"),
            path(
                "<int:order_id>/approve-refund/",
                self.admin_site.admin_view(self.process_approve_refund),
                name="orders_order_approve-refund",
            ),
            path("<int:order_id>/cancel/", self.admin_site.admin_view(self.process_cancel), name="orders_order_cancel"),
        ]
        return custom_urls + super().get_urls()

    def _redirect_to_changelist(self):
        return HttpResponseRedirect(reverse("admin:orders_order_changelist"))

    def _transition_one(self, request, order_id, *, from_statuses, to_status, success_message, before_save=None):
        order = Order.objects.get(pk=order_id)
        if order.status not in from_statuses:
            self.message_user(request, "当前订单状态不允许执行这个操作。", level=messages.WARNING)
            return self._redirect_to_changelist()

        try:
            if before_save:
                before_save(order)
            order.change_status(to_status)
            if before_save:
                order.save(update_fields=["status", "express_company", "express_no", "shipped_at", "updated_at"])
            self.message_user(request, success_message, level=messages.SUCCESS)
        except ValueError as exc:
            self.message_user(request, str(exc), level=messages.ERROR)
        return self._redirect_to_changelist()

    def process_pay(self, request, order_id):
        return self._transition_one(
            request,
            order_id,
            from_statuses={"pending_payment"},
            to_status="pending_shipment",
            success_message="订单已标记为已支付，进入待发货。",
        )

    def process_ship(self, request, order_id):
        def fill_shipping(order):
            order.express_company = order.express_company or "默认物流"
            order.express_no = order.express_no or f"AUTO{order.id:010d}"
            order.shipped_at = order.shipped_at or timezone.now()

        return self._transition_one(
            request,
            order_id,
            from_statuses={"pending_shipment"},
            to_status="pending_receipt",
            success_message="订单已发货，进入待收货。",
            before_save=fill_shipping,
        )

    def process_receive(self, request, order_id):
        return self._transition_one(
            request,
            order_id,
            from_statuses={"pending_receipt"},
            to_status="completed",
            success_message="订单已标记为完成。",
        )

    def process_approve_refund(self, request, order_id):
        return self._transition_one(
            request,
            order_id,
            from_statuses={"refund_processing"},
            to_status="completed",
            success_message="已同意退款，售后流程完成。",
        )

    def process_cancel(self, request, order_id):
        return self._transition_one(
            request,
            order_id,
            from_statuses={"pending_payment", "pending_shipment", "refund_processing"},
            to_status="cancelled",
            success_message="订单已取消。",
        )

    def _transition_orders(
        self,
        request,
        queryset,
        *,
        from_statuses,
        to_status,
        success_message,
        before_save=None,
    ):
        updated_count = 0
        skipped_count = 0

        for order in queryset:
            if order.status not in from_statuses:
                skipped_count += 1
                continue

            try:
                if before_save:
                    before_save(order)
                order.change_status(to_status)
                if before_save:
                    order.save(update_fields=["status", "express_company", "express_no", "shipped_at", "updated_at"])
                updated_count += 1
            except ValueError:
                skipped_count += 1

        if updated_count:
            self.message_user(
                request,
                success_message.format(count=updated_count),
                level=messages.SUCCESS,
            )
        if skipped_count:
            self.message_user(
                request,
                f"已跳过 {skipped_count} 个当前状态不匹配的订单。",
                level=messages.WARNING,
            )

    @admin.action(description="将选中的待支付订单标记为已支付")
    def mark_as_paid(self, request, queryset):
        self._transition_orders(
            request,
            queryset,
            from_statuses={"pending_payment"},
            to_status="pending_shipment",
            success_message="已标记 {count} 个订单为待发货。",
        )

    @admin.action(description="将选中的待发货订单标记为已发货")
    def mark_as_shipped(self, request, queryset):
        def fill_shipping(order):
            order.express_company = order.express_company or "默认物流"
            order.express_no = order.express_no or f"AUTO{order.id:010d}"
            order.shipped_at = order.shipped_at or timezone.now()

        self._transition_orders(
            request,
            queryset,
            from_statuses={"pending_shipment"},
            to_status="pending_receipt",
            success_message="已标记 {count} 个订单为已发货。",
            before_save=fill_shipping,
        )

    @admin.action(description="将选中的待收货订单标记为已完成")
    def mark_as_received(self, request, queryset):
        self._transition_orders(
            request,
            queryset,
            from_statuses={"pending_receipt"},
            to_status="completed",
            success_message="已标记 {count} 个订单为已完成。",
        )

    @admin.action(description="同意退款并完成售后")
    def approve_refund(self, request, queryset):
        self._transition_orders(
            request,
            queryset,
            from_statuses={"refund_processing"},
            to_status="completed",
            success_message="已同意 {count} 个订单的退款申请。",
        )

    @admin.action(description="取消选中的可取消订单")
    def cancel_selected_orders(self, request, queryset):
        self._transition_orders(
            request,
            queryset,
            from_statuses={"pending_payment", "pending_shipment", "refund_processing"},
            to_status="cancelled",
            success_message="已取消 {count} 个订单。",
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    list_filter = ("order",)
    search_fields = ("order__id", "product__name")

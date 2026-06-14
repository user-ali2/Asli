from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, DeliveryStaff, DeliveryZone, Payment, Refund, RefundRequest



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "total_price", "total_items"]
    inlines = [CartItemInline]
admin.site.register(CartItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order_type",
        "status",
        
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        
    )

    list_editable = (
        "status",
    )

    inlines = [OrderItemInline]

    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "method",
        "status",
        "amount",
        "transaction_id",
        "created_at"
    )

    list_filter = (
        "method",
        "status"
    )

    list_editable = (
        "status",
    )

    search_fields = ("transaction_id",)

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "get_payment",
        "amount",
        "refunded_by",
        "refunded_at",
    )

    def get_payment(sef, obj):
        return obj.payment.order.id
    

@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "user",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

    list_editable = (
        "status",
    )

admin.site.register(DeliveryZone)

admin.site.register(DeliveryStaff)
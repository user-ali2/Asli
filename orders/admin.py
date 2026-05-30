from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


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
        "status",
        "payment_method",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
    )

    list_editable = (
        "status",
    )

    inlines = [OrderItemInline]
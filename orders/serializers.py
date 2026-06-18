from rest_framework import serializers
from .models import (Order, Payment, Cart, CartItem)
from menu.models import Food


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"

class PaymentRequestSerializer(serializers.Serializer):

    phone = serializers.CharField(max_length=20)

class CartItemSerializer(serializers.ModelSerializer):

    food_name = serializers.CharField(source="food.name", read_only = True)

    food_price = serializers.DecimalField(
        source="food.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    total_price = serializers.SerializerMethodField()

    class Meta:

        model = CartItem

        fields = [
            "id",
            "food",
            "food_name",
            "food_price",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):

        return obj.total_price()
        
class CartSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    total_price = serializers.SerializerMethodField()

    total_items = serializers.SerializerMethodField()

    class Meta:

        model = Cart

        fields = [
            "id",
            "items",
            "total_price",
            "total_items",
            
        ]

    def get_items(self, obj):

        return CartItemSerializer(obj.items.all(), many=True).data
    
    def get_total_price(self, obj):
        return obj.total_price
    
    def get_total_items(self, obj):
        return obj.total_items

class AddToCartSerializer(serializers.Serializer):

    food_id = serializers.IntegerField()


class CheckoutSerializer(serializers.Serializer):

    order_type = serializers.ChoiceField(
        choices=[
            "dine_in",
            "takeout",
            "delivery"
        ]
    )

    full_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    phone = serializers.CharField(
        required = False,
        allow_blank=True
    )

    area = serializers.CharField(
        required=False,
        allow_blank=True
    )

    house_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    plot_number = serializers.CharField(
        required=False,
        allow_blank=True
    )

    delivery_notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

    

    payment_method = serializers.ChoiceField(
        choices = [
            "cash",
            "mpesa",
            "card"
        ]
    )

    zone_id = serializers.IntegerField(required=False)

    def validate(self, data):

        if data["order_type"] == "delivery":

            required_fields = [
                "full_name",
                "phone",
                "area",
            ]

            for field in  required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(
                        f"{field} is required for delivery orders."
                    )
        return data


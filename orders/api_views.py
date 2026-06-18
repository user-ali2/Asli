from rest_framework import viewsets, status
from django.db import transaction
from .models import (Order, Payment, PaymentAttempt,Cart, CartItem,OrderItem, DeliveryZone)
from .serializers import (OrderSerializer, PaymentSerializer, PaymentRequestSerializer, CartItemSerializer,CartSerializer,AddToCartSerializer, CheckoutSerializer)
from menu.models import Food
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .mpesa import stk_push
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        ).order_by("-created_at")
    
    @action(
        detail=True,
        methods=["post"]
    )

    def pay(self, request, pk=None):

        order = self.get_object()

        serializer = PaymentRequestSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        phone = serializer.validated_data["phone"]


        try:
            payment = order.payment

        except Payment.DoesNotExist:
            return Response({
                "error": "Payment record missing"
            }, status=400)

        if payment.status == "paid":
            return Response(
                {"error": "Order already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = stk_push(
            phone_number=phone,
            amount=order.total_price,
            account_reference=str(order.id)
        )

        if response.get("ResponseCode") == "0":

            PaymentAttempt.objects.create(
                payment=payment,
                status="pending",
                mpesa_checkout_id=response.get("CheckoutRequestID"),
                merchant_request_id=response.get("MerchantRequestID"),
            )

        return Response(response)

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            order__user=self.request.user
        )
    

class CartViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])

    def add(self, request):

        serializer = AddToCartSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        food_id = serializer.validated_data["food_id"]

        food = get_object_or_404(Food, id=food_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, food=food)

        if not created:
            item.quantity += 1
            item.save()

        return Response({"message": "Added to cart"})
    
    @action(detail=False, methods=["post"])

    def remove(self,request):

        item_id = request.data.get("item_id")

        cart = get_object_or_404(Cart, user=request.user)

        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        item.delete()

        return Response({"message": "Item removed"})
    
    @action(detail=False, methods=["post"])

    def increase(self, request):

        item_id = request.data.get("item_id")

        cart = get_object_or_404(Cart, user=request.user)

        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        item.quantity += 1
        item.save()

        return Response({"message": "Qauntity increased"})
    
    @action(detail=False, methods=["post"])

    def decrease(self, request):

        item_id = request.data.get("item_id")

        cart = get_object_or_404(Cart, user=request.user)

        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if item.quantity > 1 :
            item.quantity -= 1
            item.save()

        else:
            item.delete()

        return Response({"message": "Quantity updated"})
    
    @action(detail=False, methods=["post"])
    def checkout(self, request):

        serializer = CheckoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        cart = get_object_or_404(Cart, user=request.user)

        



        if not cart.items.exists():

            return Response(
                {
                    "error": "Cart is empty"
                },
                status=400
            )
        
        for item in cart.items.all():

            if not item.food.available:
                return Response({
                    "error": f"{item.food.name} is unavailable."
                }, status=400)
        
        data = serializer.validated_data

        delivery_fee = 0
        zone = None

        if data["order_type"] == "delivery":

            zone = get_object_or_404(
                DeliveryZone,
                id=data["zone_id"],
                active=True
            )

            delivery_fee = zone.delivery_fee

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,

                order_type=data["order_type"],
                zone=zone,
                full_name=data.get("full_name"),
                phone=data.get("phone"),
                area=data.get("area"),
                house_name=data.get("house_name"),
                plot_number=data.get("plot_number"),
                delivery_notes=data.get("delivery_notes"),
            )

            subtotal = 0

            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    food_name=item.food.name,
                    quantity=item.quantity,
                    price=item.food.price,
                )   


                subtotal += (item.food.price * item.quantity)

            order.subtotal = subtotal
            order.delivery_fee = delivery_fee
            order.total_price = subtotal + delivery_fee

            order.save()

            Payment.objects.create(
                order=order,
                method=data["payment_method"],
                amount=order.total_price,
                status="pending",
            )

            cart.items.all().delete()

        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "payment_status": "pending"
        })


         
    

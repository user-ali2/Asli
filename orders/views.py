from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from menu.models import Food
from .services import assign_rider
from .models import ( Cart, CartItem, Order, OrderItem, DeliveryStaff, DeliveryZone, Payment, Refund, RefundRequest, PaymentAttempt)
from .forms import CheckoutForm
from decimal import Decimal
import json

from django.http import JsonResponse
from .mpesa import stk_push
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.utils import timezone

@never_cache
@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    context = {
        "cart": cart
    }

    return render(request, "orders/cart.html", context)

@login_required
def add_to_cart(request, food_id):

    food = get_object_or_404(Food, id=food_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    item.delete()

    return redirect("cart")

@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    item.quantity += 1
    item.save()

    return redirect("cart")

@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    else:
        item.delete()
        

    return redirect("cart")

@login_required
def checkout(request):

    order_type = request.session.get("order_type", "takeout")

    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return redirect("cart")
    
    if request.method == "POST":

        form = CheckoutForm(request.POST)

       
        if form.is_valid():

            order = form.save(commit=False)

            payment_method = form.cleaned_data["payment_method"]


            order.user = request.user
            order.order_type = order_type
            order.subtotal = cart.total_price
           # order.save()

            if (
                order.order_type == "delivery" 
                and order.zone
                and order.zone.delivery_type == "external_rider"
            ):
                order.delivery_fee = (
                    order.zone.external_delivery_fee
                )

            else:
                order.delivery_fee = 0
            
            order.total_price = order.subtotal + Decimal(order.delivery_fee)

            order.status = "pending"

            order.save()

            Payment.objects.create(
                order=order,
                method=payment_method,
                amount=order.total_price,
                status="pending",
            )

            

            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=item.quantity,
                    price=item.food.price


                )

            cart.items.all().delete()

            return redirect("order_success")
        
    else:

        form = CheckoutForm()

    context = {
        "form": form,
        "cart": cart,
        "order_type": order_type,
    }

    return render(request, "orders/checkout.html", context)
    

@login_required
def order_success(request):

    return render(request, "orders/order_success.html")


@login_required
def rider_orders(request):

    rider = get_object_or_404(DeliveryStaff, user=request.user)

    orders = Order.objects.filter(
        assigned_staff=rider
    ).order_by("-created_at")

    return render (request, "orders/rider_dashboard.html", {"orders": orders})

@login_required
def mark_picked_up(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        assigned_staff__user=request.user
    )

    order.status = "picked_up"
    order.save()

    return redirect("rider_dashboard")


@login_required
def mark_on_the_way(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        assigned_staff__user=request.user
    )

    order.status = "on_the_way"
    order.save()

    return redirect("rider_dashboard")

@login_required
def mark_delivered(request, order_id):

    order = get_object_or_404(Order, id=order_id, assigned_staff__user=request.user)

    order.status = "delivered"

    if order.assigned_staff:
        order.assigned_staff.is_available = True
        order.assigned_staff.save()
    order.save()

    return redirect ("rider_dashboard")

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/my_orders.html", {
        "orders":orders
    })

@login_required
def cancel_order(request, order_id):

    if request.method == "POST":

        order = get_object_or_404(
            Order, 
            id=order_id,
            user=request.user
        )

        if order.status == "pending":
            order.status = "cancelled"
            order.save()

        if hasattr(order, "payment"):
            order.payment.status = "failed"
            order.payment.save()

    return redirect("my_orders")


@login_required
def request_refund(request, order_id):

    order = get_object_or_404(
        Order, 
        id=order_id,
        user=request.user
    )

    if request.method == "POST":

        reason = request.POST.get("reason", )

        RefundRequest.objects.create(
            order=order,
            user=request.user,
            reason=reason,
        )

        return redirect("my_orders")
    
    return render(request, "orders/request_refund.html", {
        "order": order
    })

@staff_member_required
def approve_refund(request, request_id):

    refund_request = get_object_or_404(
        RefundRequest,
        id=request_id
    )

    payment = refund_request.order.payment

    Refund.objects.create(
        payment=payment,
        amount=payment.amount,
        reason=refund_request.reason,
        refunded_by=request.user
    )

    payment.status = "refunded"
    payment.save()

    refund_request.status = "approved"
    refund_request.save()

    return redirect("/admin/")

@staff_member_required
def reject_refund(request, request_id):

    refund_request = get_object_or_404(
        RefundRequest,
        id=request_id
    )

    refund_request.status = "rejected"
    refund_request.save()

    return redirect("/admin/")


@staff_member_required
def mark_payment_paid(request, payment_id):

    if request.method != "POST":
        return redirect("cashier_dashboard")
    
    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    payment.status = "paid"
    payment.save()
    return redirect("cashier_dashboard")

@login_required
def initiate_payment(request, order_id):

    payment = order.payment

    if payment.status == "paid":
        return JsonResponse(
            {"error": "Order already paid"},
            status=400
        )

    order = get_object_or_404(Order, id=order_id, user=request.user)

    phone = request.POST.get("phone")
    amount = order.total_price

    response = stk_push(
        phone_number=phone,
        amount=amount,
        account_reference=str(order.id),
    )

    payment = order.payment




    if response.get("ResponseCode") == "0":
        attempt = PaymentAttempt.objects.create(
            payment=payment,
            status = "pending"
        )
        attempt.mpesa_checkout_id = response.get("CheckoutRequestID")
        attempt.merchant_request_id = response.get("MerchantRequestID")
        attempt.save()

    return JsonResponse(response)


def mpesa_callback(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST Required"},
            status=405
        )
    data = json.loads(request.body)

    result = data["Body"]["stkCallback"]

    checkout_id = result["CheckoutRequestID"]

    result_code = result["ResultCode"]

    if result_code == 0:

        print("Payment Successfull")

        metadata = result["CallbackMetadata"]["Item"]
        
        receipt = None

        for item in metadata:
            if item["Name"] == "MpesaReceiptNumber":
                receipt = item["Value"]

        try:
            attempt = PaymentAttempt.objects.get(mpesa_checkout_id=checkout_id)
            payment = attempt.payment

        except PaymentAttempt.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)
        
        if attempt.status == "paid":
            return JsonResponse({"status": "Already processed"})
        
        with transaction.atomic():
            attempt.status = "paid"
            attempt.mpesa_receipt_number = receipt
            payment.paid_at = timezone.now()
            attempt.save()

            
            payment.status = "paid"
            payment.save()

    else:
        try:
            attempt = PaymentAttempt.objects.get(mpesa_checkout_id=checkout_id)
            attempt.status = "failed"
            attempt.save()

        except PaymentAttempt.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})

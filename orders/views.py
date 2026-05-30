from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from menu.models import Food
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm

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

    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return redirect("cart")
    
    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user

            order.total_price = cart.total_price
            order.save()

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
        }

        return render(request, "orders/checkout.html", context)
    

@login_required
def order_success(request):

    return render(request, "orders/order_success.html")


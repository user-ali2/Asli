from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/" , views.remove_from_cart, name="remove_from_cart"),
    path("increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),
    
    path('my-orders/', views.my_orders, name="my_orders"),
    path('cancel/<int:order_id>/', views.cancel_order, name="cancel_order"),
    path("refund-request/<int:order_id>/", views.request_refund, name="request_refund"),
    path("refund-approve/<int:request_id>/", views.approve_refund, name="approve_refund"),
    path("refund-reject/<int:request_id>/" , views.reject_refund, name="reject_refund"),
    path("payment-paid/<int:payment_id>/", views.mark_payment_paid, name="mark_payment_paid"),
    path("payment/<int:order_id>/", views.initiate_payment , name="initiate_payment"),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
]
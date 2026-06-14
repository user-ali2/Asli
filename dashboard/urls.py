from django.urls import path
from . import views

urlpatterns = [
    path("router/", views.dashboard_router, name="dashboard_router"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
    path("manager/", views.manager_dashboard,name="manager_dashboard"),
    path("chef/", views.chef_dashboard, name="chef_dashboard"),
    path("cashier/", views.cashier_dashboard, name="cashier_dashboard"),
    path("waiter/", views.waiter_dashboard, name="waiter_dashboard"),
    path("rider/", views.rider_dashboard, name="rider_dashboard"),
    path("chef/order/<int:order_id>/accept/", views.accept_orders, name="accept_order"),
    path("chef/order/<int:order_id>/prepare/", views.start_preparing, name="start_preparing"),
    path("chef/order/<int:order_id>/ready/", views.mark_ready, name="mark_ready"),
    path("manager/order/<int:order_id>/assign-rider/",views.assign_rider, name="assign_rider"),
    path("waiter/order/<int:order_id>/serve/", views.serve_order, name="serve_order"),
    path("cashier/order/<int:order_id>/conplete/", views.complete_takeout_order, name="complete_takeout_order",),
    path("rider/order/<int:order_id>/pickup/", views.pickup_order, name="pickup_order"),
    path("rider/order/<int:order_id>/start/", views.start_delivery, name="start_delivery"),
    path("rider/order/<int:order_id>/delivered/", views.mark_delivered, name="mark_delivered"),

]
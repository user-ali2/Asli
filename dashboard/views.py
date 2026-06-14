from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from accounts.decorators import (
    owner_required,
    manager_required,
    chef_required,
    cashier_required,
    rider_required,
    waiter_required,

)
from menu.models import Food
from orders.models import Order, DeliveryStaff
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from accounts.utils import in_group


def dashboard_router(request):

    user = request.user

    if not user.is_authenticated:
        return redirect("staff_login")

    if user.is_superuser:
        return redirect("owner_dashboard")
    
    if in_group(user, "Manager"):
        return redirect("manager_dashboard")

    if in_group(user, "Chef"):
        return redirect("chef_dashboard")
    
    if in_group(user, "Rider"):
        return redirect("rider_dashboard")
    
    if in_group(user, "Cashier"):
        return redirect("cashier_dashboard")

    if in_group(user, "Waiter"):
        return redirect("waiter_dashboard")
    
    return redirect("staff_login")


@owner_required
def owner_dashboard(request):

    if not request.user.is_superuser and not in_group(request.user, "Owner"):
        return redirect("dashboard_router")

    orders = Order.objects.all()

    total_orders = orders.count()
    total_revenue = (orders.aggregate(Sum("total_price"))["total_price__sum"] or 0 )

    pending_orders = orders.filter(status="pending").count()
    completed_orders = orders.filter(status="completed").count()

    total_foods = Food.objects.count() 

    return render(request, "dashboard/owner_dashboard.html", {
        "total_orders": total_orders,
        "total_revenue":total_revenue,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_foods": total_foods,

    })


@manager_required
def manager_dashboard(request):

    if not in_group(request.user, "Manager"):
        return redirect("dashboard_router")

    orders = Order.objects.all()

    total_orders = orders.count()

    total_revenue = (orders.aggregate(Sum("total_price"))["total_price__sum"] or 0 )

    pending_orders = orders.filter(status="pending").count()
    completed_orders = orders.filter(status="completed").count()

    total_foods = Food.objects.count()

    delayed_orders = orders.filter(status = "pending", created_at__lt=timezone.now() - timedelta(minutes=20)).order_by("-created_at")    

    cancelled_orders = orders.filter(status__in=["cancelled", "unable_to_proceed"]).order_by("-created_at")

    failed_orders = orders.filter(status = "unable_to_proceed").order_by("-created_at")

    ready_delivery_orders = Order.objects.filter(order_type="delivery", status="ready", assigned_staff__isnull=True).order_by("-created_at")

    available_riders = DeliveryStaff.objects.filter(active=True, is_available=True)

    assigned_delivery_orders = Order.objects.filter(
        order_type="delivery",
        assigned_staff__isnull=False

    ).exclude(
        status__in=[
            "delivered",
            "completed",
            "cancelled",
            "unable_to_proceed",
        ]
    )

    undelivered_orders = orders.filter(order_type="delivery", status="ready", assigned_staff__isnull=True).order_by("-created_at")


    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_foods": total_foods,
        "delayed_orders": delayed_orders,
        "cancelled_orders": cancelled_orders,
        "failed_orders": failed_orders,
        "undelivered_orders": undelivered_orders,
        "ready_delivery_orders": ready_delivery_orders,
        "assigned_delivery_orders": assigned_delivery_orders,
        "available_riders": available_riders,
    }

    return render(request, "dashboard/manager_dashboard.html",context,)



@chef_required
def chef_dashboard(request):

    if not in_group(request.user, "Chef"):
        return redirect("dashboard_router")

    incoming_orders = Order.objects.filter(status="pending", ).order_by("-created_at")

    accepted_orders = Order.objects.filter(status="accepted").order_by(
        "-created_at"
    )

    preparing_orders = Order.objects.filter(
        status="preparing").order_by("-created_at")
    
    ready_orders = Order.objects.filter(
        status="ready"
    ).order_by("-created_at")

    context = {
        "incoming_orders": incoming_orders,
        "accepted_orders": accepted_orders,
        "preparing_orders": preparing_orders,
        "ready_orders": ready_orders,
    }

    return render(request, "dashboard/chef_dashboard.html", context)



@cashier_required
def cashier_dashboard(request):

    if not in_group(request.user, "Cashier"):
        return redirect("dashboard_router")

    orders = Order.objects.exclude(status__in=["cancelled", "unable_to_proceeds"]
                                   ).order_by("-created_at")
    
    context = {
        "orders": orders,
    }

    return render(request, "dashboard/cashier_dashboard.html", context)


@waiter_required
def waiter_dashboard(request):

    if not in_group(request.user, "Waiter"):
        return redirect("dashboard_router")

    dine_in_orders = Order.objects.filter(
        order_type='dine_in'
    ).order_by("-created_at")

    ready_orders = dine_in_orders.filter(status="ready")

    context = {"dine_in_orders": dine_in_orders, "ready_orders": ready_orders}

    return render(request, "dashboard/waiter_dashboard.html", context)


@rider_required
def rider_dashboard(request):

    if not in_group(request.user, "Rider"):
        return redirect("dashboard_router")

    assigned_orders = Order.objects.filter(
        assigned_staff__user=request.user,
        order_type="delivery",
        
    ).order_by("-created_at")

    

    active_orders = assigned_orders.exclude(
        status__in=[
            "delivered", 
            "completed",
            "cancelled",
            "unable_to_proceed",
        ]
    )

    delivered_orders = assigned_orders.filter(status="delivered")

    context = {
        "assigned_orders": assigned_orders,
        "active_orders": active_orders,
        "delivered_orders": delivered_orders,
        "total_assigned": assigned_orders.count(),
        "total_active": active_orders.count(),
        "total_delivered":delivered_orders.count(),
    }

    return render(request, "dashboard/rider_dashboard.html", context,)



@chef_required
def accept_orders(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":
        order.status = "accepted"
        order.save()
    
    return redirect("chef_dashboard")


@chef_required
def start_preparing(request , order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "accepted":
        order.status = "preparing"
        order.save()

    return redirect("chef_dashboard")


@chef_required
def mark_ready(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status == "preparing":
        order.status = "ready"
        order.save()

    return redirect("chef_dashboard")


@waiter_required
def serve_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, order_type="dine_in")

    if order.status == "ready":
        order.status = "completed"
        order.save()
    return redirect("waiter_dashboard")


@cashier_required
def complete_takeout_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, order_type="takeout")

    if order.status == "ready":
        order.status = "completed"
        order.save()

    return redirect("cashier_dashboard")


@rider_required
def pickup_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, order_type="delivery")

    if order.status == "ready":
        order.status = "picked_up"
        order.save()
    
    return redirect("rider_dashboard")


@rider_required
def start_delivery(request, order_id ):

    order = get_object_or_404(Order, id=order_id, order_type="delivery")

    if order.status == "picked_up":
        order.status = "on_the_way"
        order.save()

    return redirect("rider_dashboard")


@rider_required
def mark_delivered(request,order_id):

    order = get_object_or_404(Order, id=order_id, order_type="delivery")

    if order.status == "on_the_way":
        order.status = "delivered"
        order.save()

    if order.assigned_staff:
        order.assigned_staff.is_available = True
        order.assigned_staff.save()

    return redirect("rider_dashboard")



@manager_required
def assign_rider(request, order_id):

    order = get_object_or_404(Order, id=order_id, order_type="delivery", status="ready", assigned_staff__isnull=True)

    if request.method == "POST":
        rider_id = request.POST.get("rider_id")

        rider = get_object_or_404(
            DeliveryStaff,
            id=rider_id,
            active=True,
            is_available=True
        )

        order.assigned_staff = rider
        order.save()

        rider.is_available = False
        rider.save()

    return redirect("manager_dashboard")
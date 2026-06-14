from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from .utils import in_group
from django.contrib.auth import authenticate, login



def role_required(role_name):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                #raise PermissionDenied
                return redirect("staff_login")
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if not in_group(request.user, role_name):
                #raise PermissionDenied
                return redirect ("staff_login")

            return view_func(request, *args, **kwargs)
        return wrapper
    
    return decorator

owner_required = role_required("Owner")
manager_required = role_required("Manager")
chef_required = role_required("Chef")
cashier_required = role_required("Cashier")
rider_required = role_required("Rider")
waiter_required = role_required("Waiter")
customer_required = role_required("Customer")
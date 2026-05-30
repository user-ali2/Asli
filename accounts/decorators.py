from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from .utils import in_group
#from django.contrib.auth.decorators import login_required


def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if not in_group(request.user, 'Owner'):
            #return redirect('home')
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    
    return wrapper


def management_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if not in_group(request.user, 'Management'):
            #return redirect ('home')
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    
    return wrapper

def staff_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if not in_group(request.user, 'Staff'):
            #return redirect('home')
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper 
    
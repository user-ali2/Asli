from django.shortcuts import (render,redirect)
from menu.models import Food
from django.contrib.auth.decorators import login_required
from accounts.decorators import (
    owner_required,
    management_required,
    staff_required,
)

def home(request):

    featured_foods = Food.objects.filter(
        featured = True,
        available = True,
    )[:3]

    context = {
        'featured_foods': featured_foods
    }

    return render(request, 'home.html', context)



#def home(request):
 #   return render(request, 'home.html')

def food(request):
    return render(request, 'menu.html')

def takeout(request):
    return render(request, 'takeout.html')

def delivery(request):
    return render(request, 'delivery.html')
@login_required
@owner_required
def owner_dashboard(request):
    return render(request, 'accounts/owner_dashboard.html')
@login_required
@management_required
def management_dashboard(request):
    return render(request, 'accounts/management_dashboard.html')
@login_required
@staff_required
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')

@login_required
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')
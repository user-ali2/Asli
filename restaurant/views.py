from django.shortcuts import (render,redirect)
from menu.models import Food
from django.contrib.auth.decorators import login_required
from accounts.decorators import (
    owner_required,
    manager_required,
    chef_required,
    cashier_required,
    rider_required,
    
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

from django.shortcuts import render
from .models import Food

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
    return render(request, 'food.html')

def takeout(request):
    return render(request, 'takeout.html')

def delivery(request):
    return render(request, 'delivery.html')

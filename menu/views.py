from django.shortcuts import render
from .models import Category, Food

def menu_page(request):

    foods = Food.objects.filter(
        available = True
    )

    categories = Category.objects.all()

    featured_foods = Food.objects.filter(
        featured=True,
        available=True
        
    )[:6]

    context = {
        'foods': foods,
        'categories': categories,
        'featured_foods': featured_foods,

    }

    return render (request, 'menu/menu.html', context)



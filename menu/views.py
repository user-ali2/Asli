from django.shortcuts import render
from .models import Category, Food

def menu_page(request):

    order_type = request.GET.get('type')

    if order_type:
        request.session['order_type'] = order_type

    print(
    request.session.get("order_type")
    )

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
        'order_type': request.session.get("order_type", 'takeout')

    }

    return render (request, 'menu/menu.html', context)



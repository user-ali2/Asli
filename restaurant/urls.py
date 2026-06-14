from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('food/' , views.food, name='food'),
    path('takeout/', views.takeout, name='takeout'),
    path('delivery/', views.delivery, name='delivery'),
    
]


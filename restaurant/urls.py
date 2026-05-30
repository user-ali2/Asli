from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('food/' , views.food, name='food'),
    path('takeout/', views.takeout, name='takeout'),
    path('delivery/', views.delivery, name='delivery'),
    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('management_dashboard/', views.management_dashboard, name='management_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name = 'customer_dashboard'),
]


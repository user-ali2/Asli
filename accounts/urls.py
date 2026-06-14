from django.urls import path

from .views import (
    register_view,
    CustomLoginView,
    
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
   # path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('staff-logout/', views.staff_logout, name='staff_logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout')
]
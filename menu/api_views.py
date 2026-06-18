from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Food, Category
from .serializers import FoodSerializer, CategorySerializer

class FoodViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = FoodSerializer

    permission_classes = [AllowAny]

    queryset = Food.objects.filter(available=True).order_by("name")\
    

class CategoryViewSite(viewsets.ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    permission_classes = [AllowAny]

    queryset = Category.objects.all().order_by("name")


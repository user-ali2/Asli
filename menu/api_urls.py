from rest_framework.routers import DefaultRouter
from .api_views import FoodViewSet, CategoryViewSite

router = DefaultRouter()

router.register(r"foods", FoodViewSet, basename="foods")

router.register(r"categories", CategoryViewSite, basename="category")

urlpatterns = router.urls

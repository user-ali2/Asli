from rest_framework.routers import DefaultRouter
from .api_views import OrderViewSet,PaymentViewSet, CartViewSet

router = DefaultRouter()

router.register(
    r"orders",OrderViewSet,basename="orders"
)

router.register(
    r"payments", PaymentViewSet, basename="payments"
)

router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = router.urls
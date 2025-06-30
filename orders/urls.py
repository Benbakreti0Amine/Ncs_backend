from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'admin/orders', OrderViewSet, basename='admin-orders')

urlpatterns = router.urls 
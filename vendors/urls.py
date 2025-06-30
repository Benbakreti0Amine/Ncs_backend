from django.urls import path
from users.views import LoginView
from .views import VendorRegisterView, VendorOrderViewSet, VendorStatsView, VendorListView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', VendorRegisterView.as_view(), name='vendor-register'),
    path('login/', LoginView.as_view(), name='vendor-login'),
    path('stats/', VendorStatsView.as_view(), name='vendor-stats'),
    path('list/', VendorListView.as_view(), name='vendor-list'),
]

router = DefaultRouter()
router.register(r'orders', VendorOrderViewSet, basename='vendor-orders')

urlpatterns += router.urls 
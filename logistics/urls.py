from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PackageViewSet, DeliveryRouteViewSet, DeliveryStatusViewSet,
    PackageHistoryViewSet, DeliveryNotificationViewSet, LogisticsDashboardView
)

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')
router.register(r'routes', DeliveryRouteViewSet, basename='delivery-routes')
router.register(r'statuses', DeliveryStatusViewSet, basename='delivery-statuses')
router.register(r'history', PackageHistoryViewSet, basename='package-history')
router.register(r'notifications', DeliveryNotificationViewSet, basename='delivery-notifications')

urlpatterns = [
    path('dashboard/', LogisticsDashboardView.as_view(), name='logistics-dashboard'),
] + router.urls 
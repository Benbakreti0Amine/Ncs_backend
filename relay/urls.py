from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RelayPointViewSet, RelayOperatorRegisterView, RelayParcelViewSet, RelayProfileView, RelayEarningsView
from users.views import LoginView

router = DefaultRouter()
router.register(r'admin/relay-points', RelayPointViewSet, basename='admin-relay-points')
router.register(r'parcels', RelayParcelViewSet, basename='relay-parcels')

urlpatterns = router.urls
urlpatterns += [
    path('register/', RelayOperatorRegisterView.as_view(), name='relay-register'),
    path('login/', LoginView.as_view(), name='relay-login'),
    path('profile/', RelayProfileView.as_view(), name='relay-profile'),
    path('earnings/', RelayEarningsView.as_view(), name='relay-earnings'),
] 
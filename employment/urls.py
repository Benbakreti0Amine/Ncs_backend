from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmploymentPostViewSet, RelayApplicationViewSet

router = DefaultRouter()
router.register(r'posts', EmploymentPostViewSet, basename='employment-posts')
router.register(r'applications', RelayApplicationViewSet, basename='relay-applications')

urlpatterns = router.urls 
from django.urls import path
from .views import TrackOrderView

urlpatterns = [
    path('track/<str:tracking_id>/', TrackOrderView.as_view(), name='track-order'),
] 
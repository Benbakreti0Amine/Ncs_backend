from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('createuser/', views.ListCreateUser.as_view(), name='createuser'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('list/<int:pk>/', views.RetrieveUser.as_view(), name='retrieveuser'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

router = DefaultRouter()
router.register(r'admin/users', views.UserViewSet, basename='admin-users')

urlpatterns += router.urls
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import EmploymentPost, RelayApplication
from .serializers import EmploymentPostSerializer, RelayApplicationSerializer
from users.views import IsAdminOrStaff

# Create your views here.

class EmploymentPostViewSet(viewsets.ModelViewSet):
    queryset = EmploymentPost.objects.all()
    serializer_class = EmploymentPostSerializer
    permission_classes = [IsAdminOrStaff]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class RelayApplicationViewSet(viewsets.ModelViewSet):
    queryset = RelayApplication.objects.all()
    serializer_class = RelayApplicationSerializer
    permission_classes = [IsAdminOrStaff]

    def perform_update(self, serializer):
        serializer.save(reviewed_by=self.request.user)

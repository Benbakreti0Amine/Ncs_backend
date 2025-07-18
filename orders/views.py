from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAdminUser]

from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import VendorRegisterSerializer
from rest_framework import viewsets, permissions
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserSerializer

# Create your views here.

class VendorRegisterView(CreateAPIView):
    serializer_class = VendorRegisterSerializer

class VendorOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer


    def get_queryset(self):
        return Order.objects.filter(vendor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

class VendorStatsView(APIView):


    def get(self, request):
        vendor = request.user
        orders = Order.objects.filter(vendor=vendor)
        total = orders.count()
        delivered = orders.filter(status='PICKED_UP').count()
        returned = orders.filter(status='RETURNED').count()
        pending = orders.filter(status='PENDING').count()
        success_rate = (delivered / total) * 100 if total else 0
        return Response({
            'total_orders': total,
            'delivered': delivered,
            'returned': returned,
            'pending': pending,
            'success_rate': success_rate,
        })

class VendorListView(ListAPIView):
    queryset = User.objects.filter(role='VENDOR')
    serializer_class = UserSerializer

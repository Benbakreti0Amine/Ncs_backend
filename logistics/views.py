from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Package, DeliveryRoute, DeliveryStatus, PackageHistory, DeliveryNotification
from .serializers import (
    PackageSerializer, DeliveryRouteSerializer, DeliveryStatusSerializer,
    PackageHistorySerializer, DeliveryNotificationSerializer, PackageDetailSerializer
)
from users.views import IsAdminOrStaff
from orders.models import Order
import uuid

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_staff:
            return Package.objects.all()
        elif user.role == 'VENDOR':
            return Package.objects.filter(order__vendor=user)
        elif user.role == 'RELAY_OPERATOR':
            return Package.objects.filter(order__relay_point__operator=user)
        return Package.objects.none()

    def perform_create(self, serializer):
        # Generate unique tracking number
        tracking_number = f"CP{str(uuid.uuid4())[:8].upper()}"
        package = serializer.save(tracking_number=tracking_number)
        
        # Create initial history entry
        PackageHistory.objects.create(
            package=package,
            action='CREATED',
            description=f'Package created for order {package.order.tracking_id}',
            location=package.order.relay_point.address,
            performed_by=self.request.user
        )

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        package = self.get_object()
        new_status = request.data.get('status')
        location = request.data.get('location', '')
        description = request.data.get('description', '')
        
        if new_status:
            package.status = new_status
            package.save()
            
            # Create history entry
            PackageHistory.objects.create(
                package=package,
                action='STATUS_UPDATED',
                description=description or f'Status updated to {new_status}',
                location=location,
                performed_by=request.user
            )
            
            # Create delivery status entry
            DeliveryStatus.objects.create(
                package=package,
                status='COMPLETED' if new_status in ['DELIVERED', 'PICKED_UP_BY_CONSUMER'] else 'IN_PROGRESS',
                location=location,
                description=description or f'Package {new_status.lower()}',
                handled_by=request.user,
                is_milestone=True
            )
            
            return Response({'message': 'Status updated successfully'})
        return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def tracking_details(self, request, pk=None):
        package = self.get_object()
        serializer = PackageDetailSerializer(package)
        return Response(serializer.data)

class DeliveryRouteViewSet(viewsets.ModelViewSet):
    queryset = DeliveryRoute.objects.all()
    serializer_class = DeliveryRouteSerializer

class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_staff:
            return DeliveryStatus.objects.all()
        elif user.role == 'VENDOR':
            return DeliveryStatus.objects.filter(package__order__vendor=user)
        elif user.role == 'RELAY_OPERATOR':
            return DeliveryStatus.objects.filter(package__order__relay_point__operator=user)
        return DeliveryStatus.objects.none()

class PackageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackageHistory.objects.all()
    serializer_class = PackageHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_staff:
            return PackageHistory.objects.all()
        elif user.role == 'VENDOR':
            return PackageHistory.objects.filter(package__order__vendor=user)
        elif user.role == 'RELAY_OPERATOR':
            return PackageHistory.objects.filter(package__order__relay_point__operator=user)
        return PackageHistory.objects.none()

class DeliveryNotificationViewSet(viewsets.ModelViewSet):
    queryset = DeliveryNotification.objects.all()
    serializer_class = DeliveryNotificationSerializer

class LogisticsDashboardView(APIView):

    def get(self, request):
        user = request.user
        if user.role == 'ADMIN' or user.is_staff:
            packages = Package.objects.all()
        elif user.role == 'VENDOR':
            packages = Package.objects.filter(order__vendor=user)
        elif user.role == 'RELAY_OPERATOR':
            packages = Package.objects.filter(order__relay_point__operator=user)
        else:
            packages = Package.objects.none()

        total_packages = packages.count()
        in_transit = packages.filter(status='IN_TRANSIT').count()
        delivered = packages.filter(status='DELIVERED').count()
        pending = packages.filter(status='CREATED').count()
        
        return Response({
            'total_packages': total_packages,
            'in_transit': in_transit,
            'delivered': delivered,
            'pending': pending,
            'delivery_rate': (delivered / total_packages * 100) if total_packages > 0 else 0
        })

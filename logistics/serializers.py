from rest_framework import serializers
from .models import Package, DeliveryRoute, DeliveryStatus, PackageHistory, DeliveryNotification
from orders.serializers import OrderSerializer

class PackageSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__'

class DeliveryRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRoute
        fields = '__all__'

class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = '__all__'

class PackageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageHistory
        fields = '__all__'

class DeliveryNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryNotification
        fields = '__all__'

class PackageDetailSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    routes = DeliveryRouteSerializer(many=True, read_only=True)
    delivery_statuses = DeliveryStatusSerializer(many=True, read_only=True)
    history = PackageHistorySerializer(many=True, read_only=True)
    notifications = DeliveryNotificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__' 
from django.db import models
from users.models import User
from orders.models import Order
from relay.models import RelayPoint
from core.models import Wilaya

class Package(models.Model):
    PACKAGE_STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PICKED_UP_FROM_SELLER', 'Picked Up from Seller'),
        ('IN_TRANSIT', 'In Transit'),
        ('ARRIVED_AT_RELAY', 'Arrived at Relay Point'),
        ('READY_FOR_PICKUP', 'Ready for Pickup'),
        ('PICKED_UP_BY_CONSUMER', 'Picked Up by Consumer'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=20, unique=True)
    package_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    package_dimensions = models.CharField(max_length=100, null=True, blank=True)
    package_type = models.CharField(max_length=50, default='Standard')
    fragile = models.BooleanField(default=False)
    requires_signature = models.BooleanField(default=False)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=PACKAGE_STATUS_CHOICES, default='CREATED')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Package {self.tracking_number} - {self.order.product}"

class DeliveryRoute(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='routes')
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    from_wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT, related_name='routes_from')
    to_wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT, related_name='routes_to')
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estimated_time_hours = models.IntegerField(null=True, blank=True)
    route_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route: {self.from_location} → {self.to_location}"

class DeliveryStatus(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='delivery_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    location = models.CharField(max_length=255)
    description = models.TextField()
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_milestone = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.package.tracking_number} - {self.status} at {self.location}"

class PackageHistory(models.Model):
    ACTION_CHOICES = [
        ('CREATED', 'Package Created'),
        ('PICKED_UP', 'Picked Up'),
        ('SCANNED', 'Scanned'),
        ('IN_TRANSIT', 'In Transit'),
        ('ARRIVED', 'Arrived'),
        ('READY', 'Ready for Pickup'),
        ('PICKED_UP_BY_CONSUMER', 'Picked Up by Consumer'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
        ('NOTIFICATION_SENT', 'Notification Sent'),
        ('STATUS_UPDATED', 'Status Updated'),
    ]
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.package.tracking_number} - {self.action} at {self.timestamp}"

class DeliveryNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('SMS', 'SMS'),
        ('EMAIL', 'Email'),
        ('PUSH', 'Push Notification'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    delivery_confirmation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.package.tracking_number} - {self.notification_type} to {self.recipient}"

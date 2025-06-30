from django.db import models
from users.models import User
from relay.models import RelayPoint

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ASSIGNED', 'Assigned'),
        ('DELIVERED_TO_POINT', 'Delivered to Point'),
        ('PICKED_UP', 'Picked Up'),
        ('NOT_COLLECTED', 'Not Collected'),
        ('RETURNED', 'Returned'),
    ]
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'VENDOR'})
    relay_point = models.ForeignKey(RelayPoint, on_delete=models.PROTECT)
    product = models.CharField(max_length=255)
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    client_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    tracking_id = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_id} - {self.product} ({self.get_status_display()})"

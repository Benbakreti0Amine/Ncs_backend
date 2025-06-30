from django.db import models
from users.models import User
from core.models import Wilaya

class RelayPoint(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('BLOCKED', 'Blocked'),
    ]
    operator = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'RELAY_OPERATOR'})
    wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    opening_hours = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.address} ({self.get_status_display()})"

from django.db import models
from users.models import User
from core.models import Wilaya

class EmploymentPost(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('CLOSED', 'Closed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    place = models.CharField(max_length=255)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT)
    space_required = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'ADMIN'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.place}"

class RelayApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('BLOCKED', 'Blocked'),
    ]
    employment_post = models.ForeignKey(EmploymentPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'RELAY_OPERATOR'}, related_name='applications')
    address = models.CharField(max_length=255)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.PROTECT)
    opening_hours = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    store_image = models.ImageField(upload_to='store_images/', null=True, blank=True)
    commerce_register = models.ImageField(upload_to='commerce_registers/', null=True, blank=True)
    id_card = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.employment_post.title}"

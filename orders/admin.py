from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracking_id', 'product', 'vendor', 'relay_point', 'status', 'created_at')
    search_fields = ('tracking_id', 'product', 'client_name', 'client_phone')
    list_filter = ('status', 'relay_point', 'vendor')

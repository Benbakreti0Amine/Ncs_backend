from django.contrib import admin
from .models import Package, DeliveryRoute, DeliveryStatus, PackageHistory, DeliveryNotification

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'order', 'status', 'package_type', 'created_at', 'estimated_delivery')
    search_fields = ('tracking_number', 'order__product', 'order__client_name')
    list_filter = ('status', 'package_type', 'fragile', 'requires_signature', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DeliveryRoute)
class DeliveryRouteAdmin(admin.ModelAdmin):
    list_display = ('package', 'from_location', 'to_location', 'distance_km', 'estimated_time_hours')
    search_fields = ('package__tracking_number', 'from_location', 'to_location')
    list_filter = ('from_wilaya', 'to_wilaya', 'created_at')

@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('package', 'status', 'location', 'handled_by', 'timestamp', 'is_milestone')
    search_fields = ('package__tracking_number', 'location', 'description')
    list_filter = ('status', 'is_milestone', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(PackageHistory)
class PackageHistoryAdmin(admin.ModelAdmin):
    list_display = ('package', 'action', 'location', 'performed_by', 'timestamp')
    search_fields = ('package__tracking_number', 'description', 'location')
    list_filter = ('action', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(DeliveryNotification)
class DeliveryNotificationAdmin(admin.ModelAdmin):
    list_display = ('package', 'notification_type', 'recipient', 'sent_at', 'delivered')
    search_fields = ('package__tracking_number', 'recipient', 'message')
    list_filter = ('notification_type', 'delivered', 'sent_at')
    readonly_fields = ('sent_at',)

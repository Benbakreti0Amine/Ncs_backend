from django.contrib import admin
from .models import RelayPoint

@admin.register(RelayPoint)
class RelayPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'operator', 'wilaya', 'status', 'earnings')
    search_fields = ('address', 'operator__nom', 'operator__prenom')
    list_filter = ('status', 'wilaya')

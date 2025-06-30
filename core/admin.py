from django.contrib import admin
from .models import Wilaya

@admin.register(Wilaya)
class WilayaAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name', 'code')

from django.contrib import admin
from .models import EmploymentPost, RelayApplication

@admin.register(EmploymentPost)
class EmploymentPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'place', 'wilaya', 'status', 'created_by', 'created_at')
    search_fields = ('title', 'place', 'description')
    list_filter = ('status', 'wilaya', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RelayApplication)
class RelayApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'employment_post', 'wilaya', 'status', 'applied_at')
    search_fields = ('applicant__nom', 'applicant__prenom', 'employment_post__title')
    list_filter = ('status', 'wilaya', 'applied_at')
    readonly_fields = ('applied_at',)

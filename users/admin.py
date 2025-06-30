from django.contrib import admin

from users.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'numero_de_telephone', 'role', 'is_active', 'is_staff')
    search_fields = ('nom', 'prenom', 'numero_de_telephone', 'role')
    list_filter = ('role', 'is_active', 'is_staff')

admin.site.register(User, UserAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo', 'franquia', 'is_staff', 'is_superuser')
    list_filter = ('tipo', 'franquia', 'is_staff', 'is_superuser')

    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Sistema', {
            'fields': ('tipo', 'franquia')
        }),
    )
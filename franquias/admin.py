from django.contrib import admin
from .models import Franquia


@admin.register(Franquia)
class FranquiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj')
    search_fields = ('nome', 'cnpj')
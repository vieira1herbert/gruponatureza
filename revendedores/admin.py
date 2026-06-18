from django.contrib import admin
from .models import Revendedor


@admin.register(Revendedor)
class RevendedorAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nome',
        'cpf',
        'telefone',
        'email',
        'franquia'
    )

    search_fields = (
        'nome',
        'cpf',
        'codigo'
    )

    list_filter = ('franquia',)

    readonly_fields = ('codigo',)
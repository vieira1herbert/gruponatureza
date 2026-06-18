from django.contrib import admin
from .models import Estoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'produto',
        'franquia',
        'quantidade',
        'estoque_minimo'
    )

    list_filter = ('franquia',)
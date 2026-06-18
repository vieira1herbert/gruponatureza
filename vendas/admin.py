from django.contrib import admin
from .models import Venda, ItemVenda


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'franquia',
        'data',
        'valor_total'
    )

    inlines = [ItemVendaInline]
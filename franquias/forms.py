from django import forms
from .models import Franquia


class FranquiaForm(forms.ModelForm):
    class Meta:
        model = Franquia

        fields = [
            'nome',
            'cnpj',
            'endereco',
            'telefone',
            'ativa'
        ]
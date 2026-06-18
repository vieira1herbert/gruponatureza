from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto

        fields = [
            'nome',
            'preco',
            'codigo_barras'
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Nome do produto'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'input',
                'placeholder': 'Preço',
                'step': '0.01'
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Código de barras'
            }),
        }
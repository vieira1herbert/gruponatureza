from django import forms
from .models import Estoque


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['quantidade', 'estoque_minimo']

        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'input'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'input'}),
        }
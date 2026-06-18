from django import forms
from franquias.models import Franquia
from .models import Revendedor


class RevendedorForm(forms.ModelForm):
    class Meta:
        model = Revendedor

        fields = [
            'franquia',
            'nome',
            'cpf',
            'telefone',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        self.usuario_logado = kwargs.pop('usuario_logado', None)

        super().__init__(*args, **kwargs)

        if self.usuario_logado.tipo in ['administrador', 'operador']:
            self.fields['franquia'].queryset = Franquia.objects.all()

        elif self.usuario_logado.tipo == 'gerente':
            self.fields['franquia'].queryset = Franquia.objects.filter(
                id=self.usuario_logado.franquia_id
            )

            self.fields['franquia'].initial = self.usuario_logado.franquia
            self.fields['franquia'].disabled = True
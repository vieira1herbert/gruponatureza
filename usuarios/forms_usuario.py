from django.contrib.auth.forms import UserCreationForm

from franquias.models import Franquia
from .models import Usuario


class UsuarioCadastroForm(UserCreationForm):

    class Meta:
        model = Usuario

        fields = [
            'first_name',
            'username',
            'email',
            'tipo',
            'franquia',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        self.usuario_logado = kwargs.pop('usuario_logado', None)

        super().__init__(*args, **kwargs)

        if self.usuario_logado.tipo == 'administrador':
            self.fields['tipo'].choices = [
                ('administrador', 'Administrador'),
                ('operador', 'Operador'),
                ('gerente', 'Gerente'),
                ('colaborador', 'Colaborador'),
            ]

            self.fields['franquia'].queryset = Franquia.objects.all()

        elif self.usuario_logado.tipo == 'operador':
            self.fields['tipo'].choices = [
                ('operador', 'Operador'),
                ('gerente', 'Gerente'),
                ('colaborador', 'Colaborador'),
            ]

            self.fields['franquia'].queryset = Franquia.objects.all()

        elif self.usuario_logado.tipo == 'gerente':
            self.fields['tipo'].choices = [
                ('colaborador', 'Colaborador'),
            ]

            self.fields['franquia'].queryset = Franquia.objects.filter(
                id=self.usuario_logado.franquia_id
            )

            self.fields['franquia'].initial = self.usuario_logado.franquia
            self.fields['franquia'].disabled = True
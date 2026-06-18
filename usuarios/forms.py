from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Usuario
from franquias.models import Franquia


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'input'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        })
    )


class UsuarioForm(forms.ModelForm):

    password = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'input'
        })
    )

    class Meta:

        model = Usuario

        fields = [
            'first_name',
            'username',
            'email',
            'password',
            'tipo',
            'franquia'
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'input'
            }),

            'username': forms.TextInput(attrs={
                'class': 'input'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'input'
            }),

            'tipo': forms.Select(attrs={
                'class': 'input'
            }),

            'franquia': forms.Select(attrs={
                'class': 'input'
            }),

        }

    def __init__(self, *args, **kwargs):

        self.usuario_logado = kwargs.pop(
            'usuario_logado',
            None
        )

        super().__init__(*args, **kwargs)

        if self.usuario_logado:

            if self.usuario_logado.tipo == 'administrador':

                self.fields['tipo'].choices = [
                    ('administrador', 'Administrador'),
                    ('operador', 'Operador'),
                    ('gerente', 'Gerente'),
                    ('colaborador', 'Colaborador'),
                ]

                self.fields['franquia'].queryset = (
                    Franquia.objects.all()
                )

            elif self.usuario_logado.tipo == 'operador':

                self.fields['tipo'].choices = [
                    ('operador', 'Operador'),
                    ('gerente', 'Gerente'),
                    ('colaborador', 'Colaborador'),
                ]

                self.fields['franquia'].queryset = (
                    Franquia.objects.all()
                )

            elif self.usuario_logado.tipo == 'gerente':

                self.fields['tipo'].choices = [
                    ('colaborador', 'Colaborador')
                ]

                self.fields['franquia'].queryset = (
                    Franquia.objects.filter(
                        id=self.usuario_logado.franquia_id
                    )
                )

                self.fields['franquia'].initial = (
                    self.usuario_logado.franquia
                )

                self.fields['franquia'].disabled = True
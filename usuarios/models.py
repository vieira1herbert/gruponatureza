from django.db import models
from django.contrib.auth.models import AbstractUser
from franquias.models import Franquia


class Usuario(AbstractUser):

    TIPOS_USUARIO = (
        ('administrador', 'Administrador'),
        ('operador', 'Operador'),
        ('gerente', 'Gerente'),
        ('colaborador', 'Colaborador'),
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default='colaborador'
    )

    franquia = models.ForeignKey(
        Franquia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return f'{self.username} - {self.get_tipo_display()}'

    def is_administrador(self):
        return self.tipo == 'administrador'

    def is_operador(self):
        return self.tipo == 'operador'

    def is_gerente(self):
        return self.tipo == 'gerente'

    def is_colaborador(self):
        return self.tipo == 'colaborador'
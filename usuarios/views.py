from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import LoginForm, UsuarioForm
from .forms_usuario import UsuarioCadastroForm
from .models import Usuario


class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm


def sair(request):
    logout(request)
    return redirect('login')


@login_required
def listar_usuarios(request):

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('inicio')

    if request.user.tipo in ['administrador', 'operador']:
        usuarios = Usuario.objects.all().order_by('first_name')

    elif request.user.tipo == 'gerente':
        usuarios = Usuario.objects.filter(
            franquia=request.user.franquia
        ).order_by('first_name')

    else:
        usuarios = Usuario.objects.none()

    return render(request, 'usuarios/listar.html', {
        'usuarios': usuarios
    })


@login_required
def cadastrar_usuario(request):

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('inicio')

    if request.method == 'POST':

        form = UsuarioCadastroForm(
            request.POST,
            usuario_logado=request.user
        )

        if form.is_valid():

            usuario = form.save(commit=False)

            if request.user.tipo == 'gerente':
                usuario.franquia = request.user.franquia
                usuario.tipo = 'colaborador'

            if request.user.tipo == 'operador' and usuario.tipo == 'administrador':
                messages.error(
                    request,
                    'Operador não pode cadastrar Administrador.'
                )
                return redirect('listar_usuarios')

            usuario.save()

            messages.success(
                request,
                'Usuário cadastrado com sucesso.'
            )

            return redirect('listar_usuarios')

    else:

        form = UsuarioCadastroForm(
            usuario_logado=request.user
        )

    return render(request, 'usuarios/cadastrar.html', {
        'form': form
    })


@login_required
def editar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('listar_usuarios')

    if request.user.tipo == 'gerente':

        if usuario.franquia != request.user.franquia:
            messages.error(
                request,
                'Você só pode editar usuários da sua própria franquia.'
            )
            return redirect('listar_usuarios')

        if usuario.tipo != 'colaborador':
            messages.error(
                request,
                'Gerentes só podem editar colaboradores.'
            )
            return redirect('listar_usuarios')

    form = UsuarioForm(
        request.POST or None,
        instance=usuario,
        usuario_logado=request.user
    )

    if form.is_valid():

        usuario_editado = form.save(commit=False)

        senha = request.POST.get('password')

        if senha:
            usuario_editado.set_password(senha)

        if request.user.tipo == 'gerente':
            usuario_editado.tipo = 'colaborador'
            usuario_editado.franquia = request.user.franquia

        if request.user.tipo == 'operador' and usuario_editado.tipo == 'administrador':
            messages.error(
                request,
                'Operador não pode definir usuário como Administrador.'
            )
            return redirect('listar_usuarios')

        usuario_editado.save()

        messages.success(
            request,
            'Usuário atualizado com sucesso.'
        )

        return redirect('listar_usuarios')

    return render(
        request,
        'usuarios/editar.html',
        {
            'form': form,
            'usuario_editado': usuario
        }
    )
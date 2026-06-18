from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RevendedorForm
from .models import Revendedor


@login_required
def listar_revendedores(request):

    if request.user.tipo in ['administrador', 'operador']:
        revendedores = Revendedor.objects.select_related(
            'franquia'
        ).all().order_by('nome')

    elif request.user.tipo == 'gerente':
        revendedores = Revendedor.objects.select_related(
            'franquia'
        ).filter(
            franquia=request.user.franquia
        ).order_by('nome')

    else:
        messages.error(request, 'Você não possui permissão.')
        return redirect('home')

    return render(request, 'revendedores/listar.html', {
        'revendedores': revendedores
    })


@login_required
def cadastrar_revendedor(request):

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('home')

    if request.method == 'POST':
        form = RevendedorForm(
            request.POST,
            usuario_logado=request.user
        )

        if form.is_valid():
            revendedor = form.save(commit=False)

            if request.user.tipo == 'gerente':
                revendedor.franquia = request.user.franquia

            revendedor.save()

            messages.success(request, 'Revendedor cadastrado com sucesso.')
            return redirect('listar_revendedores')

    else:
        form = RevendedorForm(usuario_logado=request.user)

    return render(request, 'revendedores/cadastrar.html', {
        'form': form
    })

@login_required
def editar_revendedor(request, revendedor_id):

    revendedor = get_object_or_404(
        Revendedor,
        id=revendedor_id
    )

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('listar_revendedores')

    if request.user.tipo == 'gerente' and revendedor.franquia != request.user.franquia:
        messages.error(request, 'Você só pode editar revendedores da sua franquia.')
        return redirect('listar_revendedores')

    form = RevendedorForm(
        request.POST or None,
        instance=revendedor,
        usuario_logado=request.user
    )

    if form.is_valid():
        revendedor = form.save(commit=False)

        if request.user.tipo == 'gerente':
            revendedor.franquia = request.user.franquia

        revendedor.save()

        messages.success(request, 'Revendedor atualizado com sucesso.')
        return redirect('listar_revendedores')

    return render(request, 'revendedores/editar.html', {
        'form': form,
        'revendedor': revendedor
    })
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FranquiaForm
from .models import Franquia


@login_required
def listar_franquias(request):

    if request.user.tipo != 'administrador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('/')

    busca = request.GET.get('busca', '').strip()

    franquias = Franquia.objects.all()

    if busca:
        franquias = franquias.filter(
            nome__icontains=busca
        )

    franquias = franquias.order_by('nome')

    return render(request, 'franquias/listar.html', {
        'franquias': franquias,
        'busca': busca
    })


@login_required
def cadastrar_franquia(request):

    if request.user.tipo != 'administrador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('/')

    form = FranquiaForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Franquia cadastrada com sucesso.')
        return redirect('listar_franquias')

    return render(request, 'franquias/cadastrar.html', {
        'form': form
    })


@login_required
def editar_franquia(request, franquia_id):

    if request.user.tipo != 'administrador':
        messages.error(request, 'Você não possui permissão.')
        return redirect('/')

    franquia = get_object_or_404(
        Franquia,
        id=franquia_id
    )

    form = FranquiaForm(
        request.POST or None,
        instance=franquia
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Franquia atualizada com sucesso.')
        return redirect('listar_franquias')

    return render(request, 'franquias/editar.html', {
        'form': form,
        'franquia': franquia
    })
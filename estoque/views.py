from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Estoque
from .forms import EstoqueForm


@login_required
def listar_estoque(request):

    codigo = request.GET.get('codigo', '').strip()

    estoques = Estoque.objects.select_related(
        'produto',
        'franquia'
    )

    if request.user.tipo in ['administrador', 'operador']:
        estoques = estoques.all()

    elif request.user.tipo in ['gerente', 'colaborador']:
        estoques = estoques.filter(
            franquia=request.user.franquia
        )

    else:
        messages.error(request, 'Você não possui permissão.')
        return redirect('home')

    if codigo:
        estoques = estoques.filter(
            produto__codigo_barras__icontains=codigo
        )

    estoques = estoques.order_by('produto__nome')

    return render(request, 'estoque/listar.html', {
        'estoques': estoques,
        'codigo': codigo
    })


@login_required
def editar_estoque(request, estoque_id):

    estoque = get_object_or_404(Estoque, id=estoque_id)

    if request.user.tipo == 'colaborador':
        messages.error(request, 'Você não possui permissão para editar estoque.')
        return redirect('listar_estoque')

    if request.user.tipo == 'gerente' and estoque.franquia != request.user.franquia:
        messages.error(request, 'Você só pode editar estoque da sua própria franquia.')
        return redirect('listar_estoque')

    if request.user.tipo not in ['administrador', 'operador', 'gerente']:
        messages.error(request, 'Você não possui permissão.')
        return redirect('listar_estoque')

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)

        if form.is_valid():
            form.save()
            messages.success(request, 'Estoque atualizado com sucesso.')
            return redirect('listar_estoque')

    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'estoque/editar.html', {
        'form': form,
        'estoque': estoque
    })
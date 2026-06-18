from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Produto
from .forms import ProdutoForm


@login_required
def listar_produtos(request):

    if request.user.tipo != 'administrador':
        messages.error(
            request,
            'Você não possui permissão.'
        )
        return redirect('/')

    nome = request.GET.get('nome', '').strip()
    codigo_barras = request.GET.get('codigo_barras', '').strip()

    produtos = Produto.objects.all()

    if nome:
        produtos = produtos.filter(
            nome__icontains=nome
        )

    if codigo_barras:
        produtos = produtos.filter(
            codigo_barras__icontains=codigo_barras
        )

    produtos = produtos.order_by('nome')

    return render(
        request,
        'produtos/listar.html',
        {
            'produtos': produtos,
            'nome': nome,
            'codigo_barras': codigo_barras
        }
    )


@login_required
def cadastrar_produto(request):

    if request.user.tipo != 'administrador':
        messages.error(
            request,
            'Você não possui permissão.'
        )
        return redirect('/')

    form = ProdutoForm(request.POST or None)

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Produto cadastrado com sucesso.'
        )

        return redirect('/produtos/')

    return render(
        request,
        'produtos/cadastrar.html',
        {
            'form': form
        }
    )


@login_required
def editar_produto(request, produto_id):

    if request.user.tipo != 'administrador':
        messages.error(
            request,
            'Você não possui permissão.'
        )
        return redirect('/')

    produto = get_object_or_404(
        Produto,
        id=produto_id
    )

    form = ProdutoForm(
        request.POST or None,
        instance=produto
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Produto atualizado com sucesso.'
        )

        return redirect('/produtos/')

    return render(
        request,
        'produtos/editar.html',
        {
            'form': form,
            'produto': produto
        }
    )
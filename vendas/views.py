import json

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views.decorators.csrf import csrf_exempt

from produtos.models import Produto
from estoque.models import Estoque
from revendedores.models import Revendedor

from .models import Venda, ItemVenda


@login_required
def identificar_revendedor(request):

    request.session.pop('revendedor_id', None)
    request.session.pop('venda_temp', None)

    if request.method == 'POST':

        identificacao = request.POST.get(
            'identificacao',
            ''
        ).strip()

        revendedor = None

        cpf_limpo = (
            identificacao
            .replace('.', '')
            .replace('-', '')
            .replace(' ', '')
        )

        if identificacao.isdigit():

            revendedor = Revendedor.objects.filter(
                codigo=int(identificacao)
            ).first()

        if not revendedor:

            for rev in Revendedor.objects.all():

                cpf_bd = (
                    rev.cpf
                    .replace('.', '')
                    .replace('-', '')
                    .replace(' ', '')
                )

                if cpf_bd == cpf_limpo:
                    revendedor = rev
                    break

        if not revendedor:

            messages.error(
                request,
                'Revendedor não encontrado.'
            )

            return redirect('identificar_revendedor')

        request.session['revendedor_id'] = revendedor.id

        return redirect('pdv')

    return render(
        request,
        'pdv/identificar_revendedor.html'
    )


@login_required
def pdv(request):

    revendedor_id = request.session.get(
        'revendedor_id'
    )

    if not revendedor_id:
        return redirect(
            'identificar_revendedor'
        )

    revendedor = get_object_or_404(
        Revendedor,
        id=revendedor_id
    )

    produtos = Produto.objects.all()

    produtos_json = []

    for produto in produtos:

        produtos_json.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': float(produto.preco),
            'codigo_barras': produto.codigo_barras
        })

    return render(
        request,
        'pdv/pdv.html',
        {
            'produtos_json': produtos_json,
            'revendedor': revendedor
        }
    )


@login_required
@csrf_exempt
def preparar_pagamento(request):

    if request.method != 'POST':

        return JsonResponse(
            {'erro': 'Método inválido'},
            status=405
        )

    try:

        dados = json.loads(request.body)

        revendedor_id = request.session.get(
            'revendedor_id'
        )

        itens = dados.get('itens', [])

        if not revendedor_id:

            return JsonResponse({
                'erro': 'Revendedor não identificado.'
            }, status=400)

        if not itens:

            return JsonResponse({
                'erro': 'Carrinho vazio.'
            }, status=400)

        revendedor = get_object_or_404(
            Revendedor,
            id=revendedor_id
        )

        request.session['venda_temp'] = {
            'revendedor_id': revendedor.id,
            'itens': itens
        }

        return JsonResponse({
            'redirect': '/pdv/pagamento/'
        })

    except Exception as erro:

        return JsonResponse({
            'erro': str(erro)
        }, status=500)


@login_required
def pagamento(request):

    venda_temp = request.session.get(
        'venda_temp'
    )

    if not venda_temp:

        messages.error(
            request,
            'Nenhuma venda em andamento.'
        )

        return redirect('pdv')

    revendedor = get_object_or_404(
        Revendedor,
        id=venda_temp['revendedor_id']
    )

    itens_resumo = []

    total = Decimal('0.00')

    for item in venda_temp['itens']:

        produto = get_object_or_404(
            Produto,
            id=item['id']
        )

        quantidade = int(item['quantidade'])

        subtotal = produto.preco * quantidade

        itens_resumo.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

        total += subtotal

    return render(
        request,
        'pdv/pagamento.html',
        {
            'revendedor': revendedor,
            'itens': itens_resumo,
            'total': total,
            'formas_pagamento': Venda.FORMAS_PAGAMENTO
        }
    )


@login_required
def confirmar_venda(request):

    if request.method != 'POST':
        return redirect('pdv')

    venda_temp = request.session.get(
        'venda_temp'
    )

    if not venda_temp:

        messages.error(
            request,
            'Nenhuma venda em andamento.'
        )

        return redirect('pdv')

    forma_pagamento = request.POST.get(
        'forma_pagamento'
    )

    formas_validas = [
        forma[0]
        for forma in Venda.FORMAS_PAGAMENTO
    ]

    if forma_pagamento not in formas_validas:

        messages.error(
            request,
            'Forma de pagamento inválida.'
        )

        return redirect('pagamento')

    if not request.user.franquia:

        messages.error(
            request,
            'Usuário sem franquia vinculada.'
        )

        return redirect('pdv')

    revendedor = get_object_or_404(
        Revendedor,
        id=venda_temp['revendedor_id']
    )

    try:

        with transaction.atomic():

            venda = Venda.objects.create(
                usuario=request.user,
                franquia=request.user.franquia,
                revendedor=revendedor,
                forma_pagamento=forma_pagamento,
                valor_total=0
            )

            total = Decimal('0.00')

            for item in venda_temp['itens']:

                produto = Produto.objects.get(
                    id=item['id']
                )

                quantidade = int(
                    item['quantidade']
                )

                estoque = Estoque.objects.select_for_update().get(
                    produto=produto,
                    franquia=request.user.franquia
                )

                if estoque.quantidade < quantidade:

                    messages.error(
                        request,
                        f'Estoque insuficiente para {produto.nome}.'
                    )

                    return redirect('pdv')

                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco
                )

                estoque.quantidade -= quantidade

                estoque.save()

                total += (
                    produto.preco * quantidade
                )

            venda.valor_total = total

            venda.save()

        del request.session['venda_temp']

        return redirect(
            'extrato_venda',
            venda_id=venda.id
        )

    except Estoque.DoesNotExist:

        messages.error(
            request,
            'Produto sem estoque cadastrado para esta franquia.'
        )

        return redirect('pdv')


@login_required
def extrato_venda(request, venda_id):

    venda = get_object_or_404(
        Venda.objects.select_related(
            'usuario',
            'franquia',
            'revendedor'
        ),
        id=venda_id
    )

    itens = venda.itens.select_related(
        'produto'
    ).all()

    return render(
        request,
        'vendas/extrato.html',
        {
            'venda': venda,
            'itens': itens
        }
    )


@login_required
def listar_vendas(request):

    codigo = request.GET.get('codigo', '').strip()
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    revendedor = request.GET.get('revendedor', '').strip()
    pagamento = request.GET.get('pagamento', '').strip()

    vendas = Venda.objects.select_related(
        'usuario',
        'franquia',
        'revendedor'
    )

    if request.user.tipo in ['administrador', 'operador']:
        vendas = vendas.all()

    elif request.user.tipo in ['gerente', 'colaborador']:
        vendas = vendas.filter(
            franquia=request.user.franquia
        )

    else:
        messages.error(request, 'Você não possui permissão.')
        return redirect('home')

    if codigo:
        vendas = vendas.filter(
            codigo_pedido__icontains=codigo
        )

    if data_inicio:
        vendas = vendas.filter(
            data__date__gte=data_inicio
        )

    if data_fim:
        vendas = vendas.filter(
            data__date__lte=data_fim
        )

    if revendedor:
        vendas = vendas.filter(
            Q(revendedor__nome__icontains=revendedor) |
            Q(revendedor__cpf__icontains=revendedor) |
            Q(revendedor__codigo__icontains=revendedor)
        )

    if pagamento:
        vendas = vendas.filter(
            forma_pagamento=pagamento
        )

    total_vendido = vendas.aggregate(
        total=Sum('valor_total')
    )['total'] or 0

    quantidade_vendas = vendas.count()

    vendas = vendas.order_by('-data')

    return render(
        request,
        'vendas/listar.html',
        {
            'vendas': vendas,
            'codigo': codigo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'revendedor': revendedor,
            'pagamento': pagamento,
            'formas_pagamento': Venda.FORMAS_PAGAMENTO,
            'total_vendido': total_vendido,
            'quantidade_vendas': quantidade_vendas
        }
    )


@login_required
def detalhe_venda(request, venda_id):

    venda = get_object_or_404(
        Venda.objects.select_related(
            'usuario',
            'franquia',
            'revendedor'
        ),
        id=venda_id
    )

    itens = venda.itens.select_related(
        'produto'
    ).all()

    return render(
        request,
        'vendas/detalhe.html',
        {
            'venda': venda,
            'itens': itens
        }
    )
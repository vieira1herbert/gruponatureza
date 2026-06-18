from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from django.shortcuts import render

from vendas.models import Venda, ItemVenda
from produtos.models import Produto
from estoque.models import Estoque
from franquias.models import Franquia
from revendedores.models import Revendedor

@login_required
def inicio(request):
    return render(request, 'inicio/home.html')

@login_required
def home(request):

    periodo = request.GET.get('periodo', 'hoje')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    franquia_id = request.GET.get('franquia', '')

    hoje = date.today()

    if periodo == '7':
        inicio = hoje - timedelta(days=7)
        fim = hoje

    elif periodo == '30':
        inicio = hoje - timedelta(days=30)
        fim = hoje

    elif periodo == 'personalizado' and data_inicio and data_fim:
        inicio = data_inicio
        fim = data_fim

    else:
        inicio = hoje
        fim = hoje
        periodo = 'hoje'

    vendas = Venda.objects.select_related(
        'usuario',
        'franquia',
        'revendedor'
    ).filter(
        data__date__gte=inicio,
        data__date__lte=fim
    )

    if request.user.tipo in ['gerente', 'colaborador']:
        vendas = vendas.filter(
            franquia=request.user.franquia
        )

    elif franquia_id:
        vendas = vendas.filter(
            franquia_id=franquia_id
        )

    vendas_hoje = Venda.objects.filter(
        data__date=hoje
    )

    if request.user.tipo in ['gerente', 'colaborador']:
        vendas_hoje = vendas_hoje.filter(
            franquia=request.user.franquia
        )

    elif franquia_id:
        vendas_hoje = vendas_hoje.filter(
            franquia_id=franquia_id
        )

    total_hoje = vendas_hoje.aggregate(
        total=Sum('valor_total')
    )['total'] or 0

    total_periodo = vendas.aggregate(
        total=Sum('valor_total')
    )['total'] or 0

    quantidade_vendas = vendas.count()

    ticket_medio = 0

    if quantidade_vendas > 0:
        ticket_medio = total_periodo / quantidade_vendas

    if request.user.tipo in ['gerente', 'colaborador']:
        estoque_baixo = Estoque.objects.filter(
            franquia=request.user.franquia,
            quantidade__lte=F('estoque_minimo')
        ).count()

        total_revendedores = Revendedor.objects.filter(
            franquia=request.user.franquia
        ).count()

    elif franquia_id:
        estoque_baixo = Estoque.objects.filter(
            franquia_id=franquia_id,
            quantidade__lte=F('estoque_minimo')
        ).count()

        total_revendedores = Revendedor.objects.filter(
            franquia_id=franquia_id
        ).count()

    else:
        estoque_baixo = Estoque.objects.filter(
            quantidade__lte=F('estoque_minimo')
        ).count()

        total_revendedores = Revendedor.objects.count()

    total_produtos = Produto.objects.count()
    total_franquias = Franquia.objects.count()

    ultimas_vendas = vendas.order_by('-data')[:8]

    valor_item = ExpressionWrapper(
        F('quantidade') * F('preco_unitario'),
        output_field=DecimalField()
    )

    top_produtos = ItemVenda.objects.filter(
        venda__in=vendas
    ).values(
        'produto__nome'
    ).annotate(
        quantidade_total=Sum('quantidade'),
        total_vendido=Sum(valor_item)
    ).order_by('-quantidade_total')[:5]

    formas_pagamento = vendas.values(
        'forma_pagamento'
    ).annotate(
        quantidade=Count('id'),
        total=Sum('valor_total')
    ).order_by('-quantidade')

    vendas_por_franquia = vendas.values(
        'franquia__nome'
    ).annotate(
        quantidade=Count('id'),
        total=Sum('valor_total')
    ).order_by('-total')[:5]

    franquias = Franquia.objects.all().order_by('nome')

    context = {
        'periodo': periodo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'franquia_id': franquia_id,
        'franquias': franquias,
        'total_hoje': total_hoje,
        'total_periodo': total_periodo,
        'quantidade_vendas': quantidade_vendas,
        'ticket_medio': ticket_medio,
        'total_produtos': total_produtos,
        'estoque_baixo': estoque_baixo,
        'total_franquias': total_franquias,
        'total_revendedores': total_revendedores,
        'ultimas_vendas': ultimas_vendas,
        'top_produtos': top_produtos,
        'formas_pagamento': formas_pagamento,
        'vendas_por_franquia': vendas_por_franquia,
    }

    return render(request, 'dashboard/home.html', context)
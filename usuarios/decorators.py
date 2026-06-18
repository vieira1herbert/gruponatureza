from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def administrador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo == 'administrador':
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('home')

    return wrapper


def operador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo in ['administrador', 'operador']:
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('home')

    return wrapper


def colaborador_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo in ['administrador', 'operador', 'colaborador']:
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('login')

    return wrapper
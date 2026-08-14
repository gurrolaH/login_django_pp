from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Producto


@login_required
def listar_productos_view(request):
    productos = Producto.objects.all()

    context = {
        'productos': productos
    }

    return render(request, 'productos/lista-productos.html', context)

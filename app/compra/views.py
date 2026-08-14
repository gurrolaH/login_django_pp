from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Compra


@login_required
def listar_compras_view(request):
    compras = Compra.objects.select_related(
        'proveedor',
        'empleado'
    ).prefetch_related(
        'detalles__producto'
    ).all()

    context = {
        'compras': compras
    }

    return render(request, 'compras/lista-compras.html', context)

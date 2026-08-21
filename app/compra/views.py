from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CompraForm, DetalleCompraFormSet
from .models import Compra, DetalleCompra


@login_required
def registrar_compra_view(request):
    compra_form = CompraForm(request.POST or None)
    detalle_formset = DetalleCompraFormSet(request.POST or None, prefix='detalles')

    if request.method == 'POST':
        if compra_form.is_valid() and detalle_formset.is_valid():
            compra = compra_form.save(commit=False)
            compra.subtotal = Decimal('0.00')
            compra.impuesto = Decimal('0.00')
            compra.total = Decimal('0.00')
            compra.save()

            for form in detalle_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    detalle = form.save(commit=False)
                    detalle.compra = compra
                    detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                    detalle.save()

                    compra.subtotal += detalle.subtotal

            compra.total = compra.subtotal + compra.impuesto
            compra.save()

            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('compra:lista')
        else:
            messages.error(request, 'Por favor revisa los errores en la compra y en los detalles.')

    context = {
        'compra_form': compra_form,
        'detalle_formset': detalle_formset,
    }

    return render(request, 'compras/crear-compra.html', context)


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

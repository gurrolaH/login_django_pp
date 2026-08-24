from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CompraForm, DetalleCompraFormSet
from .models import Compra, DetalleCompra

# Movimiento inventario: importamos los modelos e utilidades necesarias
from django.db import transaction, IntegrityError
from django.db.models import F
from inventario.models import MovimientoInventario, Inventario
from inventario.forms import InventarioForm, MovimientoInventarioForm


@login_required
def registrar_compra_view(request):

    # Registrar compra.
    compra_form = CompraForm(request.POST or None)
    detalle_formset = DetalleCompraFormSet(request.POST or None, prefix='detalles')

    if request.method == 'POST':
        if compra_form.is_valid() and detalle_formset.is_valid():
            compra = compra_form.save(commit=False)
            compra.subtotal = Decimal('0.00')
            compra.impuesto = Decimal('0.00')
            compra.total = Decimal('0.00')
            compra.save()

            # Preparar listas para la creación en lote
            movimientos_para_crear = []
            # acumulador por producto para actualizar inventario una sola vez por producto
            cantidades_por_producto = {}

            # Recorremos los formularios de detalle y guardamos cada detalle
            for form in detalle_formset:

                # DELETE indica formularios marcados para eliminación
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    detalle = form.save(commit=False)
                    detalle.compra = compra
                    # calcular subtotal del detalle (cantidad * precio unitario)
                    detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                    detalle.save()  # guardamos el detalle para tener su PK y FK

                    # Construimos la instancia de MovimientoInventario pero NO la guardamos aún.
                    # Usamos los campos requeridos del modelo: producto, empleado, detalle_compra, tipo, cantidad.
                    movimiento = MovimientoInventario(
                        producto=detalle.producto,
                        empleado=compra.empleado,
                        detalle_compra=detalle,
                        tipo=MovimientoInventario.Tipo.ENTRADA,
                        cantidad=detalle.cantidad,
                        motivo=f'Entrada por Compra #{compra.id_compra}',
                    )

                    # Añadimos a la lista para crear en bloque después
                    movimientos_para_crear.append(movimiento)

                    # Acumulamos la cantidad por producto para actualizar inventario en un único update
                    prod_id = detalle.producto_id
                    cantidades_por_producto[prod_id] = (
                        cantidades_por_producto.get(prod_id, 0) + detalle.cantidad
                    )

                    # Acumulador del subtotal de la compra
                    compra.subtotal += detalle.subtotal

            # Usamos una transacción para que la creación de movimientos y la
            # actualización del inventario sea atómica si algo falla, todo hace rollback.
            with transaction.atomic():
                # 1) Crear todos los movimientos en una sola operación de base de datos
                if movimientos_para_crear:
                    MovimientoInventario.objects.bulk_create(movimientos_para_crear)

                # 2) Actualizar el inventario por producto usando F() para operaciones atómicas
                # Hacemos una actualización por producto
                for prod_id, cantidad_total in cantidades_por_producto.items():
                    # Intentamos primero actualizar la fila existente de Inventario
                    # usando una operación atómica en la base de datos.
                    updated = Inventario.objects.filter(producto_id=prod_id).update(
                        existencia=F('existencia') + cantidad_total
                    )

                    # Si no se actualizó ninguna fila, significa que no existe
                    # una entrada de Inventario para ese producto: la creamos.
                    if updated == 0:
                        try:
                            Inventario.objects.create(
                                producto_id=prod_id,
                                existencia=cantidad_total
                            )
                        except IntegrityError:
                            # En ese caso, volvemos a intentar la actualización.
                            Inventario.objects.filter(producto_id=prod_id).update(
                                existencia=F('existencia') + cantidad_total
                            )

                # 3) Calcular y guardar totales finales de la compra
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

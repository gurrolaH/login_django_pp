from decimal import Decimal
from decimal import InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db import models
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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
                    try:
                        subtotal_val = detalle.cantidad * detalle.precio_unitario
                    except Exception:
                        messages.error(request, 'Error calculando subtotal del detalle.')
                        return render(request, 'compras/crear-compra.html', {'compra_form': compra_form, 'detalle_formset': detalle_formset})

                    # Verificar que el subtotal no exceda los dígitos permitidos por el campo
                    MAX_DIGITS = detalle._meta.get_field('subtotal').max_digits
                    DECIMALS = detalle._meta.get_field('subtotal').decimal_places
                    try:
                        # Cuantizamos a los DECIMALS para calcular dígitos totales
                        quant = subtotal_val.quantize(Decimal('1.' + ('0' * DECIMALS)))
                    except InvalidOperation:
                        quant = subtotal_val

                    # Cuenta de dígitos sin signo y sin punto
                    digits = ''.join(str(quant).replace('.', '').lstrip('-')).lstrip('0')
                    total_digits = len(digits) if digits else 1
                    if total_digits > MAX_DIGITS:
                        messages.error(request, f'El subtotal ({subtotal_val}) excede el límite de {MAX_DIGITS} dígitos para el campo subtotal.')
                        return render(request, 'compras/crear-compra.html', {'compra_form': compra_form, 'detalle_formset': detalle_formset})

                    detalle.subtotal = subtotal_val
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
                            estado=MovimientoInventario.Estado.ACTIVO,
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


@login_required
def cancelar_detalle_view(request, detalle_id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

    detalle = get_object_or_404(DetalleCompra, pk=detalle_id)
    compra = detalle.compra

    # Si ya está cancelado, respondemos con error
    if detalle.estado == DetalleCompra.Estado.CANCELADA:
        return JsonResponse({'success': False, 'message': 'El detalle ya está cancelado.'}, status=400)

    # Preparamos los datos para validar con el form de movimiento
    form_data = {
        'producto': detalle.producto.id_producto,
        'empleado': compra.empleado.id_empleado,
        'tipo': MovimientoInventario.Tipo.SALIDA_REVERSA,
        'estado': MovimientoInventario.Estado.ACTIVO,
        'cantidad': detalle.cantidad,
        'detalle_compra': detalle.id_detalle_compra,
        'motivo': f'Cancelación detalle Compra #{compra.id_compra}',
    }

    form = MovimientoInventarioForm(data=form_data)
    if not form.is_valid():
        # Rechazamos si la validación del movimiento falla stock insuficiente
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Realizamos la operación atómica: crear movimiento, actualizar inventario y marcar detalle
    with transaction.atomic():
        movimiento = form.save()

        # Restamos existencia en Inventario atomicamente con F()
        updated = Inventario.objects.filter(producto=detalle.producto).update(
            existencia=F('existencia') - detalle.cantidad
        )

        if updated == 0:
            # No existe inventario registrado para el producto
            transaction.set_rollback(True)
            return JsonResponse({'success': False, 'message': 'No existe inventario para el producto.'}, status=400)

        # Marcamos el detalle como cancelado
        detalle.estado = DetalleCompra.Estado.CANCELADA
        detalle.save()

        # Actualizamos el estado de la compra según renglones
        detalles = compra.detalles.all()
        total = detalles.count()
        cancelados = detalles.filter(estado=DetalleCompra.Estado.CANCELADA).count()

        if cancelados == total:
            compra.estado = Compra.Estado.CANCELADA
        elif cancelados > 0:
            compra.estado = Compra.Estado.CANCELADA_PARCIAL

        compra.save()

    return JsonResponse({'success': True, 'message': 'Detalle cancelado correctamente.'})


@login_required
def cancelar_compra_view(request, compra_id):

    # Cancelar toda la compra completa.

    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

    compra = get_object_or_404(Compra, pk=compra_id)

    # Detalles que aún no estén cancelados
    detalles_a_cancelar = compra.detalles.filter(~models.Q(estado=DetalleCompra.Estado.CANCELADA))  # Filtramos lso que no estén cancelados
    if not detalles_a_cancelar.exists():
        return JsonResponse({'success': False, 'message': 'No hay renglones por cancelar.'}, status=400)

    # Acumulamos cantidades por producto para comprobar stock disponible
    cantidades_por_producto = {}
    for det in detalles_a_cancelar:
        pid = det.producto_id
        cantidades_por_producto[pid] = cantidades_por_producto.get(pid, 0) + det.cantidad

    # Comprobamos inventario para cada producto
    errores = []
    for pid, qty in cantidades_por_producto.items():
        try:
            inv = Inventario.objects.get(producto_id=pid)
            if inv.existencia < qty:
                errores.append(f'Producto {inv.producto.nombre}: stock insuficiente ({inv.existencia} disponible, {qty} requerido)')
        except Inventario.DoesNotExist:
            # No hay inventario creado para el producto
            # Añadimos error y abortamos
            errores.append(f'Producto id {pid}: no existe registro de inventario')

    if errores:
        return JsonResponse({'success': False, 'errors': errores}, status=400)

    # Si todo válido, crear movimientos en lote y actualizar inventario
    movimientos = []
    movimientos_create_objs = []
    detalles_ids = []

    for det in detalles_a_cancelar:
        movimientos_create_objs.append(MovimientoInventario(
            producto=det.producto,
            empleado=compra.empleado,
            detalle_compra=det,
            tipo=MovimientoInventario.Tipo.SALIDA_REVERSA,
            cantidad=det.cantidad,
            motivo=f'Cancelación compra #{compra.id_compra}'
        ))
        detalles_ids.append(det.id_detalle_compra)

    with transaction.atomic():
        # Crear movimientos en lote
        MovimientoInventario.objects.bulk_create(movimientos_create_objs)

        # Restar existencias por producto
        for pid, qty in cantidades_por_producto.items():
            Inventario.objects.filter(producto_id=pid).update(existencia=F('existencia') - qty)

        # Marcar todos los detalles como cancelados
        compra.detalles.filter(id_detalle_compra__in=detalles_ids).update(estado=DetalleCompra.Estado.CANCELADA)

        # Marcar compra como cancelada
        compra.estado = Compra.Estado.CANCELADA
        compra.save()

    return JsonResponse({'success': True, 'message': 'Compra cancelada correctamente.'})

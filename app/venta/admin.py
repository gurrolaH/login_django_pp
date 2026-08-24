from django.contrib import admin

from .models import Venta, DetalleVenta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):

    list_display = (
        'id_venta',
        'cliente',
        'empleado',
        'fecha_venta',
        'estado',
        'subtotal',
        'descuento',
        'impuesto',
        'total',
    )

    search_fields = (
        'cliente__nombre',
        'cliente__apellido',
        'empleado__nombre',
        'empleado__apellido',
    )

    list_filter = (
        'estado',
        'fecha_venta',
    )


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):

    list_display = (
        'id_detalle_venta',
        'venta',
        'producto',
        'cantidad',
        'precio_unitario',
        'descuento',
        'subtotal',
        'estado',
    )

    search_fields = (
        'producto__nombre',
        'producto__sku',
    )

    list_filter = (
        'estado',
        'producto',
    )
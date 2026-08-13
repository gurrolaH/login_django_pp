from django.contrib import admin

from .models import Compra, DetalleCompra


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):

    list_display = (
        'id_compra',
        'proveedor',
        'empleado',
        'fecha_compra',
        'estado',
        'total',
    )

    search_fields = (
        'proveedor__nombre',
        'empleado__nombre',
        'empleado__apellido',
    )

    list_filter = (
        'estado',
        'fecha_compra',
    )


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):

    list_display = (
        'id_detalle_compra',
        'compra',
        'producto',
        'cantidad',
        'precio_unitario',
        'subtotal',
    )

    search_fields = (
        'producto__nombre',
        'producto__sku',
    )
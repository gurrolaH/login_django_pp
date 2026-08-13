from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id_producto',
        'sku',
        'nombre',
        'precio_venta',
        'activo',
    )

    search_fields = (
        'sku',
        'nombre',
    )

    list_filter = (
        'activo',
    )
from django.contrib import admin
from .models import Compra


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
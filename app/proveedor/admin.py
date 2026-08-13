from django.contrib import admin
from .models import Proveedor

# Para poder administrar desde admin

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'id_proveedor',
        'nombre',
        'telefono',
        'email',
        'activo',
    )

    search_fields = (
        'nombre',
        'email',
        'telefono',
    )

    list_filter = (
        'activo',
    )
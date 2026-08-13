from django.contrib import admin
from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'id_empleado',
        'nombre',
        'apellido',
        'telefono',
        'email',
        'puesto',
        'fecha_ingreso',
        'activo',
    )

    search_fields = (
        'nombre',
        'apellido',
        'email',
        'telefono',
    )

    list_filter = (
        'activo',
        'puesto',
    )
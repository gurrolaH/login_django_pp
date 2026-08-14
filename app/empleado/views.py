from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Empleado



# Esta vista nos permitirá listar a todos los empleados:
@login_required
def listar_empleados_view(request):

    # Obtener lso datos del modelo sin filtros.
    empleados = Empleado.objects.all()

    # Pasar los datos a un context.
    context = {
        'empleados': empleados
    }

    # Hacer la el reenderizado.
    return render(request, 'empleados/lista-empleados.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Proveedor


# Está función nos va a permitir consultar todo los proveedore en existencia.
@login_required
def listar_provedores_view(request):

    # 1. Obtener los proveedores de la base de datos.
    proveedores = Proveedor.objects.all()  

    # 2. Pasamos los datos por el context.
    context = {
        'proveedores': proveedores
    }

    # 3. Reenderizamos la plantilla específica con los datos.
    return render(request, 'proveedores/lista-proveedores.html', context)


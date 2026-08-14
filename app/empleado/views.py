from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmpleadoForm
from .models import Empleado


# Esta vista nos permitirá registrar nuevo usuarios:
@login_required
def registrar_empleados_view(request):

    # 1 Identificar si llega un GET o Post
    if request.method == 'POST':

        # 2 Hacer la intancia del FORM con la información llenada por el usuario
        form = EmpleadoForm(request.POST)

        # 3 Identificar si el FORM es válido
        if form.is_valid():

            # 4 Hacer la persistencia de los datos.
            form.save()

            # 5 Mensaje de éxito
            messages.success(request, 'Empleado registrado de forma exitosa.')

            # 6 Redireccionamiento para actulizar la página
            return redirect('empleado:lista')

        # 7 Si el form no es válido.
        else:
            messages.error(request, 'Por favor revisa los errores en el formulario.')


    # 8 Si llega un GET una instancia vacía
    else:
        form = EmpleadoForm()

    # 9 Reenderizado de la respuesta.
    return render(request, 'empleados/crear-empleado.html', {'form': form})



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

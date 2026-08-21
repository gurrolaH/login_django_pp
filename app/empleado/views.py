from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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


# Esta función permitirá editar un empleado existente en la base de datos.
@login_required
def actualizar_empleado_view(request, pk):

    # 1. Buscamos el registro en la BD por su PK. Si no existe se lanza un error 404.
    empleado = get_object_or_404(Empleado, id_empleado=pk)

    # 2. Detectamos si es POST o GET.
    if request.method == 'POST':

        # 3. Se llena el formulario con los nuevos datos enviados (request.POST)
        #  Y se vincula a la instancia existente (instance=empleado).
        form = EmpleadoForm(request.POST, instance=empleado)

        # 4. Comprobaciones automáticas del ModelForm.
        if form.is_valid():

            # 5. Se actualizan y guardan los cambios del objeto Empleado en la base de datos.
            form.save()

            # 6. Mensaje temporal en la sesión para informar la actualización correcta.
            messages.success(request, 'Empleado actualizado exitosamente.')

            # 7. Redirección hacia la vista de la lista para evitar el reenvío del formulario al recargar.
            return redirect('empleado:lista')

        else:
            # 8. Si la validación falla, se agrega un mensaje de advertencia.
            messages.error(request, 'Por favor revisa los errores en el formulario.')

    else:
        # 9. Si viene por GET, se precarga el formulario con la información actual de la instancia existente.
        form = EmpleadoForm(instance=empleado)

    # 10. Muestra la plantilla HTML enviando el formulario prellenado mediante el contexto.
    return render(request, 'empleados/editar-empleado.html', {'form': form, 'empleado': empleado})

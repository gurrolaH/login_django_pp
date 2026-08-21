from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto


@login_required
def registrar_productos_view(request):

    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto registrado de forma exitosa.')
            return redirect('producto:lista')
        else:
            messages.error(request, 'Por favor revisa los errores en el formulario.')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear-producto.html', {'form': form})


@login_required
def listar_productos_view(request):
    productos = Producto.objects.all()

    context = {
        'productos': productos
    }

    return render(request, 'productos/lista-productos.html', context)


# Este método nos permitirá actualizar un producto específico.
@login_required
def actualizar_producto_view(request, pk):

    # 1. Obtener el el objeto específico de la base de datos, si no mandamos el 404.
    producto = get_object_or_404(Producto, pk=pk)

    # 2. Identificar si el request viene por POST o Get.
    if request.method == 'POST':

        # 3. Hacer la instacia del formulario, mandando la consulta del post.
        form = ProductoForm(request.POST, instance=producto)  # Para editar se usa instance.

        # 4. Identificar si los datos que vienen en el formulario son válidos
        if form.is_valid():

            # 5. Persisistir los datos actualizados en la base de datos.
            form.save()

            # 6. Mensaje de éxito
            messages.success(request, 'Producto actualizado exitosamente.')

            # 7. Redireccionamos para evitar el reenvió de los datos
            return redirect('producto:lista')

    
        # Si los datos del formulario no son válidos.
        else:

            8. # Mensaje de error y volver a mandar el formulario para llenarlo.
            messages.error(request, 'Por favor revisa los errores en el formulario.')


    # 9. Si viene por GET reenderizamos el formulario prellenado.
    else:

        form = ProductoForm(instance=producto)
        #messages.error(request, 'Por favor revisa los errores en el formulario.')
        

    # 10. Llenar el context.
    context = {
        'form': form,
        'producto': producto
    }

    # 11. Hacer un render por si es GET o si se equivocaron en el form.
    return render(request, 'productos/editar-producto.html', context)

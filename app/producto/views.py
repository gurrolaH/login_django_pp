from django.contrib import messages
from django.shortcuts import render, redirect
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

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Proveedor
from django.contrib import messages
from .forms import ProveedorForm


# Está función permitirá que se pueda crear un nuevo proveedor en la base de datos.
@login_required
def registrar_proveedor_view(request):
    
    # 2. Detectamos si es post o get
    if request.method == 'POST':
        
        # 3. Se llena el formulario con la información enviada por el usuario desde el HTML.
        form = ProveedorForm(request.POST)
        
        # 4. Comprobaciones automáticas del ModelForm
        if form.is_valid():
            
            # 5. Se inserta y guarda el nuevo objeto Proveedor directamente en la base de datos.
            form.save()
            
            # 6. Mensaje temporal en la sesión para informar la creación correcta.
            messages.success(request, 'Proveedor registrado exitosamente.')
            
            # 7. Respuesta hacia la vista de la lista para evitar duplicados al recargar la página.
            return redirect('proveedor:lista')
        
        else:
            # 8. Si la validación falla, se agrega un mensaje de advertencia.
            messages.error(request, 'Por favor revisa los errores en el formulario.')
            
    else:
        # 9. Si viene por GET se manda la instancia a un formulario vacío listo para ser renderizado en la plantilla.
        form = ProveedorForm()  # Se irá el form vacío.

    # 10. Muestra la plantilla HTML enviando la instancia del formulario mediante el contexto.
    return render(request, 'proveedores/crear-proveedor.html', {'form': form})



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


# Esta función permitirá editar un proveedor existente en la base de datos.
@login_required
def actualizar_proveedores_view(request, pk):
    
    # 1. Buscamos el registro en la BD por su PK. Si no existe se lanza un error 404.
    proveedor = get_object_or_404(Proveedor, id_proveedor=pk)
    
    # 2. Detectamos si es POST o GET.
    if request.method == 'POST':
        
        # 3. Se llena el formulario con los nuevos datos enviados (request.POST) 
        #  Y se vincula a la instancia existente (instance=proveedor).
        form = ProveedorForm(request.POST, instance=proveedor)
        
        # 4. Comprobaciones automáticas del ModelForm
        if form.is_valid():
            
            # 5. Se actualizan y guardan los cambios del objeto Proveedor en la base de datos.
            form.save()
            
            # 6. Mensaje temporal en la sesión para informar la actualización correcta.
            messages.success(request, 'Proveedor actualizado exitosamente.')
            
            # 7. Redirección hacia la vista de la lista para evitar el reenvió del formulario al recargar.
            return redirect('proveedor:lista')
        
        else:
            # 8. Si la validación falla, se agrega un mensaje de advertencia.
            messages.error(request, 'Por favor revisa los errores en el formulario.')
            
    else:
        # 9. Si viene por GET, se precarga el formulario con la información actual de la instancia existente.
        form = ProveedorForm(instance=proveedor)  # Se enviará el form con los datos prellenados.

    # 10. Muestra la plantilla HTML enviando el formulario prellenado mediante el contexto.
    return render(request, 'proveedores/editar-proveedor.html', {'form': form, 'proveedor': proveedor})






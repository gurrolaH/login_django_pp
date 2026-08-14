from django.shortcuts import redirect, render
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




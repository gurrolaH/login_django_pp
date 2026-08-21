from django.urls import path
from . import views

app_name = 'proveedor'

urlpatterns = [
    path('listar-proveedores/', views.listar_provedores_view, name='lista'),
    path('registrar-proveedores/', views.registrar_proveedor_view, name='crear'),
    path('modificar-proveedores/<int:pk>', views.actualizar_proveedores_view, name='actualizar'),
    
]
from django.urls import path
from . import views

app_name = 'proveedor'

urlpatterns = [
    path('listar-proveedores/', views.listar_provedores_view, name='lista'),
]
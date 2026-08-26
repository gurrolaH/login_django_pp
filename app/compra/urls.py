from django.urls import path
from . import views

app_name = 'compra'

urlpatterns = [
    path('listar-compras/', views.listar_compras_view, name='lista'),
    path('registrar-compra/', views.registrar_compra_view, name='crear'),
    # Endpoints para cancelaciones (detalle y compra completa)
    path('detalle/<int:detalle_id>/cancelar/', views.cancelar_detalle_view, name='cancelar_detalle'),
    path('<int:compra_id>/cancelar/', views.cancelar_compra_view, name='cancelar_compra'),
]
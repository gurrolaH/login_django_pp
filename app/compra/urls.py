from django.urls import path
from . import views

app_name = 'compra'

urlpatterns = [
    path('listar-compras/', views.listar_compras_view, name='lista'),
]
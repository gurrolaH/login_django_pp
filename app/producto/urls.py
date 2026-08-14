from django.urls import path
from . import views

app_name = 'producto'

urlpatterns = [
    path('listar-productos/', views.listar_productos_view, name='lista'),
]
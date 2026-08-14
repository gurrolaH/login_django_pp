from django.urls import path
from . import views

app_name = 'empleado'

urlpatterns = [
    path('listar-empleados/', views.listar_empleados_view, name='lista'),
    #path('registrar-empleados', views.registrar_empleados_view, name='crear'),
]
from django import forms
from .models import Empleado


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'email',
            'puesto',
            'fecha_ingreso',
            'activo',
        ]
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'puesto': 'Puesto o Cargo',
            'fecha_ingreso': 'Fecha de Ingreso',
            'activo': 'Empleado Activo',
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={'placeholder': 'Ej. Carlos'}
            ),
            'apellido': forms.TextInput(
                attrs={'placeholder': 'Ej. Mendoza Pérez'}
            ),
            'telefono': forms.TextInput(
                attrs={'placeholder': 'Ej. 4921234567'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'empleado@empresa.com'}
            ),
            'puesto': forms.TextInput(
                attrs={'placeholder': 'Ej. Desarrollador, Vendedor, Gerente'}
            ),
            'fecha_ingreso': forms.DateInput(
                attrs={
                    'type': 'date',  # Permite usar el selector de fecha nativo del navegador
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',  # Opcional si usas estilos tipo Bootstrap
                }
            ),
        }
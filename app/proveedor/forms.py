from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'direccion', 'contacto']
        labels = {
            'nombre': 'Nombre o Razón Social',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'contacto': 'Persona de Contacto',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Andrea / Comercializadora S.A.'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej. 4921234567'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Calle, Número, Colonia, Ciudad'}),
            'contacto': forms.TextInput(attrs={'placeholder': 'Nombre del contacto directo'}),
        }
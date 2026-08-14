from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'sku',
            'nombre',
            'descripcion',
            'precio_venta',
            'activo',
        ]
        labels = {
            'sku': 'Modelo',
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio_venta': 'Precio de Venta',
            'activo': 'Producto Activo',
        }
        widgets = {
            'sku': forms.TextInput(
                attrs={'placeholder': 'Ej. PRD-001'}
            ),
            'nombre': forms.TextInput(
                attrs={'placeholder': 'Ej. Laptop Lenovo'}
            ),
            'descripcion': forms.Textarea(
                attrs={'placeholder': 'Describe el producto...', 'rows': 4}
            ),
            'precio_venta': forms.NumberInput(
                attrs={'placeholder': 'Ej. 1500.00', 'step': '0.01'}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

from django import forms
from django.forms import formset_factory

from .models import Compra, DetalleCompra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = [
            'proveedor',
            'empleado',
            'estado',
            'observaciones',
        ]
        labels = {
            'proveedor': 'Proveedor',
            'empleado': 'Empleado',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones de la compra'}),
        }


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = [
            'producto',
            'cantidad',
            'precio_unitario',
        ]
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
        }
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
        }


DetalleCompraFormSet = formset_factory(
    DetalleCompraForm,
    extra=1,
    min_num=1,
    validate_min=True,
)

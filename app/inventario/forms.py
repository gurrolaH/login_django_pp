from django import forms
from django.core.exceptions import ValidationError
from .models import Inventario, MovimientoInventario


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'producto',
            'existencia',
            'stock_minimo',
            'stock_maximo',
            'ubicacion',
            'activo',
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pasillo 3, Estante B'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        stock_minimo = cleaned_data.get('stock_minimo')
        stock_maximo = cleaned_data.get('stock_maximo')

        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo > stock_maximo:
                raise ValidationError({
                    'stock_minimo': 'El stock mínimo no puede ser mayor que el stock máximo.'
                })
        return cleaned_data


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = [
            'producto',
            'empleado',
            'tipo',
            'estado',
            'cantidad',
            'motivo',
            'observaciones',
            'detalle_compra',
            'detalle_venta',
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del movimiento'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'detalle_compra': forms.Select(attrs={'class': 'form-select'}),
            'detalle_venta': forms.Select(attrs={'class': 'form-select'}),
        }

    # Validaciones.
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')

        # Validar existencia suficiente si es una salida manual/ajuste
        if producto and tipo in [MovimientoInventario.Tipo.SALIDA, MovimientoInventario.Tipo.SALIDA_REVERSA] and cantidad:
            try:
                inventario = producto.inventario
                if inventario.existencia < cantidad:
                    raise ValidationError({
                        'cantidad': f'Stock insuficiente. Disponibles: {inventario.existencia}'
                    })
            except Inventario.DoesNotExist:
                raise ValidationError({
                    'producto': 'El producto seleccionado no tiene un registro de inventario creado.'
                })

        return cleaned_data
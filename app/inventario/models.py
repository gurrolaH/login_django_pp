from django.db import models

from producto.models import Producto
from compra.models import DetalleCompra
from venta.models import DetalleVenta
from empleado.models import Empleado

class Inventario(models.Model):

    id_inventario = models.BigAutoField(primary_key=True)

    producto = models.OneToOneField(
        Producto,
        on_delete=models.PROTECT,
        related_name='inventario'
    )

    existencia = models.PositiveIntegerField(
        default=0
    )

    stock_minimo = models.PositiveIntegerField(
        default=0
    )

    stock_maximo = models.PositiveIntegerField(
        default=0
    )

    ubicacion = models.CharField(
        max_length=100,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'inventario'
        ordering = ['producto__nombre']

    def __str__(self):
        return f'{self.producto.nombre} - Stock: {self.cantidad}'


class MovimientoInventario(models.Model):

    class Tipo(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SALIDA = 'salida', 'Salida'
        AJUSTE = 'ajuste', 'Ajuste'
        ENTRADA_REVERSA = 'entrada_reversa', 'Entrada reversa'
        SALIDA_REVERSA = 'salida_reversa', 'Salida reversa'

    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        REVERTIDO = 'revertido', 'Revertido'

    id_movimiento = models.BigAutoField(
        primary_key=True
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='movimientos_inventario'
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='movimientos_inventario'
    )

    detalle_compra = models.ForeignKey(
        DetalleCompra,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='movimientos_inventario'
    )

    detalle_venta = models.ForeignKey(
        DetalleVenta,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='movimientos_inventario'
    )

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices
    )

    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    cantidad = models.PositiveIntegerField()

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True
    )

    motivo = models.CharField(
        max_length=150,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    class Meta:
        db_table = 'movimiento_inventario'
        ordering = ['-fecha_movimiento']

    def __str__(self):
        return (
            f'{self.tipo} - '
            f'{self.producto.nombre} - '
            f'{self.cantidad}'
        )
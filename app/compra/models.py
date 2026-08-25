from django.db import models

from producto.models import Producto
from proveedor.models import Proveedor
from empleado.models import Empleado


class Compra(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        RECIBIDA = 'RECIBIDA', 'Recibida'
        RECIBIDA_PARCIAL = 'RECIBIDA_PARCIAL', 'Recibida parcial'
        CANCELADA_PARCIAL = 'CANCELADA_PARCIAL', 'Cancelada parcial'
        CANCELADA = 'CANCELADA', 'Cancelada'

    id_compra = models.BigAutoField(primary_key=True)

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='compras'
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='compras'
    )

    fecha_compra = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    impuesto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    observaciones = models.TextField(
        blank=True
    )

    class Meta:
        db_table = 'compra'
        ordering = ['-fecha_compra']

    def __str__(self):
        return f'Compra #{self.id_compra}'


class DetalleCompra(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        RECIBIDA = 'RECIBIDA', 'Recibida'
        RECHAZADA = 'RECHAZADA', 'Rechazada'  # llegó dañado o incorrecto
        CANCELADA = 'CANCELADA', 'Cancelada'  # se canceló antes de recibir

    id_detalle_compra = models.BigAutoField(primary_key=True)

    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_compra'
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    class Meta:
        db_table = 'detalle_compra'
        ordering = ['id_detalle_compra']

    def save(self, *args, **kwargs):
        self.subtotal = (
            self.cantidad * self.precio_unitario
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'Compra #{self.compra.id_compra} - '
            f'{self.producto.nombre}'
        )
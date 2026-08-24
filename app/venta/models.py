from django.db import models

from cliente.models import Cliente
from empleado.models import Empleado
from producto.models import Producto


class Venta(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADA = 'PAGADA', 'Pagada'
        CANCELADA_PARCIAL = 'CANCELADA_PARCIAL', 'Cancelada parcial'
        CANCELADA = 'CANCELADA', 'Cancelada'

    id_venta = models.BigAutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ventas'
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        related_name='ventas'
    )

    fecha_venta = models.DateTimeField(
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

    descuento = models.DecimalField(
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
        db_table = 'venta'
        ordering = ['-fecha_venta']

    def __str__(self):
        return f'Venta #{self.id_venta}'


class DetalleVenta(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADA = 'PAGADA', 'Pagada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    id_detalle_venta = models.BigAutoField(
        primary_key=True
    )

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_venta'
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    descuento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
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
        db_table = 'detalle_venta'
        ordering = ['id_detalle_venta']

    def save(self, *args, **kwargs):
        self.subtotal = (
            self.cantidad * self.precio_unitario
        ) - self.descuento

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'Venta #{self.venta.id_venta} - '
            f'{self.producto.nombre}'
        )
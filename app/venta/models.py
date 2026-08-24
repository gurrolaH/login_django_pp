from django.db import models

from cliente.models import Cliente
from empleado.models import Empleado


class Venta(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADA = 'PAGADA', 'Pagada'
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
from django.db import models

from proveedor.models import Proveedor
from empleado.models import Empleado


class Compra(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        RECIBIDA = 'RECIBIDA', 'Recibida'
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
        
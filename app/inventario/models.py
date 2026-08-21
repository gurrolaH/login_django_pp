from django.db import models

from producto.models import Producto


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
from django.db import models

# Modelo de Producto:
class Producto(models.Model):

    id_producto = models.BigAutoField(primary_key=True)

    sku = models.CharField(
        max_length=50,
        unique=True
    )

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True
    )

    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'producto'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.sku} - {self.nombre}'

from django.db import models


class Cliente(models.Model):

    id_cliente = models.BigAutoField(primary_key=True)

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        max_length=150,
        blank=True
    )

    direccion = models.CharField(
        max_length=255,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'cliente'
        ordering = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
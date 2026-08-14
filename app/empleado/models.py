from django.db import models

# Entidad Empleado
class Empleado(models.Model):

    id_empleado = models.BigAutoField(primary_key=True)

    nombre = models.CharField(max_length=100)

    apellido = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,      
        unique=True     
    )

    email = models.EmailField(
        max_length=150,
        blank=True,
        null=True,      
        unique=True     
    )

    puesto = models.CharField(
        max_length=100,
        blank=True
    )

    fecha_ingreso = models.DateField()

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'empleado'
        ordering = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

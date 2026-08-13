from django.db import models

# Create your models here.
class Proveedor(models.Model):

    # Llave primaria:
    id_proveedor = models.BigAutoField(primary_key=True)

    nombre = models.CharField(max_length=150)

    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=100, blank=True)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'proveedor'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
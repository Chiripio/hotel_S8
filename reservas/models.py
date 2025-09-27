from django.db import models

class Habitacion(models.Model):
    tipo = models.CharField(max_length=30)       # Individual | Doble | Suite
    capacidad = models.PositiveSmallIntegerField()
    precio_noche = models.PositiveIntegerField() # CLP (sin decimales)

    def __str__(self):
        return f"{self.tipo} ({self.capacidad} pax)"

class Reserva(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name='reserva')
    fecha_entrada = models.DateField()
    fecha_salida  = models.DateField()
    nombre = models.CharField(max_length=80)
    email  = models.EmailField()
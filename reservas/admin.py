from django.contrib import admin
from .models import Habitacion, Reserva

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "capacidad", "precio_noche")
    list_filter = ("capacidad",)
    search_fields = ("tipo",)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "habitacion",
        "fecha_entrada",
        "fecha_salida",
        "nombre",
        "email",
    )
    list_filter = ("habitacion", "fecha_entrada", "fecha_salida")
    search_fields = ("nombre", "email")

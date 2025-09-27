from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('habitaciones/<int:id>/', views.detalle, name='detalle'),
    path('reservar/<int:id>/', views.reservar, name='reservar'),
    path('reserva/<int:id>/confirmada/', views.confirmada, name='confirmada'),
]
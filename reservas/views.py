from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Habitacion, Reserva


def home(request):
    return render(request, 'reservas/home.html')


def buscar(request):
    # Muestra el formulario de fechas. El submit (GET) va a /habitaciones
    return render(request, 'reservas/buscar.html')


def _rango_invalido(ci, co):
    return not (ci and co) or co <= ci


def _hay_solape(hab, ci, co):
    return Reserva.objects.filter(
        habitacion=hab,
        fecha_entrada__lt=co,
        fecha_salida__gt=ci
    ).exists()


def habitaciones(request):
    ci = parse_date(request.GET.get('checkin', ''))
    co = parse_date(request.GET.get('checkout', ''))

    if _rango_invalido(ci, co):
        # Si no hay fechas válidas, vuelve al formulario con mensaje
        return render(request, 'reservas/buscar.html', {
            'error': 'La fecha de salida debe ser posterior a la de entrada.'
        })

    disponibles = Habitacion.objects.exclude(
        reserva__fecha_entrada__lt=co,
        reserva__fecha_salida__gt=ci
    ).distinct().order_by('precio_noche')

    ctx = {
        'habitaciones': disponibles,
        'ci': request.GET.get('checkin', ''),
        'co': request.GET.get('checkout', ''),
    }
    return render(request, 'reservas/habitaciones.html', ctx)


def detalle(request, id):
    h = get_object_or_404(Habitacion, id=id)
    ci = request.GET.get('checkin', '')
    co = request.GET.get('checkout', '')
    return render(request, 'reservas/detalle.html', {'h': h, 'ci': ci, 'co': co})


def reservar(request, id):
    h = get_object_or_404(Habitacion, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        ci = parse_date(request.POST.get('checkin', ''))
        co = parse_date(request.POST.get('checkout', ''))

        if _rango_invalido(ci, co):
            return render(request, 'reservas/reservar.html', {
                'h': h,
                'error': 'Rango de fechas inválido.',
                'ci': request.POST.get('checkin', ''),
                'co': request.POST.get('checkout', ''),
                'nombre': nombre,
                'email': email,
            })

        if _hay_solape(h, ci, co):
            return render(request, 'reservas/reservar.html', {
                'h': h,
                'error': 'La habitación ya está reservada en ese rango.',
                'ci': request.POST.get('checkin', ''),
                'co': request.POST.get('checkout', ''),
                'nombre': nombre,
                'email': email,
            })

        r = Reserva.objects.create(
            habitacion=h,
            fecha_entrada=ci,
            fecha_salida=co,
            nombre=nombre,
            email=email,
        )
        return redirect('confirmada', id=r.id)

    # GET
    ci = request.GET.get('checkin', '')
    co = request.GET.get('checkout', '')
    return render(request, 'reservas/reservar.html', {'h': h, 'ci': ci, 'co': co})


def confirmada(request, id):
    r = get_object_or_404(Reserva, id=id)
    return render(request, 'reservas/confirmada.html', {'r': r})

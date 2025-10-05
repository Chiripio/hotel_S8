from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Habitacion, Reserva

import requests, datetime
from django.http import JsonResponse


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

    # --- Cálculo de precio en USD usando el tipo de cambio actual ---
    fx_data = fx_rate_context(request)
    fx = fx_data.get("fx_clp_usd", 0.0011)  # 1 CLP -> USD
    for h in disponibles:
        try:
            h.precio_usd = round(float(h.precio_noche) * float(fx), 2)
        except Exception:
            h.precio_usd = None

    ctx = {
        'habitaciones': disponibles,
        'ci': request.GET.get('checkin', ''),
        'co': request.GET.get('checkout', ''),
        'fx_usd_clp': fx_data.get('fx_usd_clp'),
        'fx_clp_usd': fx_data.get('fx_clp_usd'),
        'fx_ts': fx_data.get('fx_ts'),
        'fx_fallback': fx_data.get('fx_fallback'),
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


def fx_rate(request):
    """
    Devuelve el tipo de cambio entre CLP y USD usando una API externa.
    Incluye fallback si no hay conexión.
    Params opcionales: ?base=CLP&quote=USD
    """
    base = request.GET.get("base", "CLP")
    quote = request.GET.get("quote", "USD")
    try:
        # Proveedor 1: exchangerate.host
        url = f"https://api.exchangerate.host/latest?base={base}&symbols={quote}"
        r = requests.get(url, timeout=6)
        data = r.json()
        clp_usd = float(data["rates"][quote])     # 1 CLP -> USD
        usd_clp = 1.0 / clp_usd                     # 1 USD -> CLP

    except Exception:
        try:
            # Proveedor 2 (respaldo real): open.er-api.com
            # Ejemplo: https://open.er-api.com/v6/latest/CLP
            u2 = f"https://open.er-api.com/v6/latest/{base}"
            r2 = requests.get(u2, timeout=6)
            j2 = r2.json()
            clp_usd = float(j2["rates"][quote])   # 1 CLP -> USD
            usd_clp = 1.0 / clp_usd
        except Exception:
            # Fallback fijo si ningún proveedor responde
            clp_usd = 0.0011
            usd_clp = 1.0 / clp_usd
            payload = {
                "base": base,
                "quote": quote,
                "rate": clp_usd,            # compat con versión previa
                "clp_per_usd": usd_clp,     # compat con versión previa
                "clp_usd": clp_usd,         # 1 CLP -> USD (claro)
                "usd_clp": usd_clp,         # 1 USD -> CLP (claro)
                "ts": datetime.datetime.utcnow().isoformat() + "Z",
                "fallback": True,
            }
            return JsonResponse(payload, status=200)

    payload = {
        "base": base,
        "quote": quote,
        "rate": clp_usd,            # compat con versión previa
        "clp_per_usd": usd_clp,     # compat con versión previa
        "clp_usd": clp_usd,         # 1 CLP -> USD
        "usd_clp": usd_clp,         # 1 USD -> CLP
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "fallback": False,
    }
    return JsonResponse(payload, status=200)


# --- Context processor: expone tipo de cambio en todas las plantillas ---
# Asegúrate de tener en settings.py -> TEMPLATES[0]['OPTIONS']['context_processors']
# la línea: 'reservas.views.fx_rate_context',

def fx_rate_context(request):
    """Entrega variables fx_* globales para templates."""
    base = "CLP"
    quote = "USD"
    try:
        url = f"https://api.exchangerate.host/latest?base={base}&symbols={quote}"
        r = requests.get(url, timeout=6)
        data = r.json()
        clp_usd = float(data["rates"][quote])
        usd_clp = 1.0 / clp_usd
        return {
            "fx_base": base,
            "fx_quote": quote,
            "fx_rate": clp_usd,            # compat
            "fx_clp_per_usd": usd_clp,     # compat
            "fx_clp_usd": clp_usd,         # 1 CLP -> USD
            "fx_usd_clp": usd_clp,         # 1 USD -> CLP
            "fx_ts": datetime.datetime.utcnow().isoformat() + "Z",
            "fx_fallback": False,
        }
    except Exception:
        try:
            u2 = f"https://open.er-api.com/v6/latest/{base}"
            r2 = requests.get(u2, timeout=6)
            j2 = r2.json()
            clp_usd = float(j2["rates"][quote])
            usd_clp = 1.0 / clp_usd
            return {
                "fx_base": base,
                "fx_quote": quote,
                "fx_rate": clp_usd,
                "fx_clp_per_usd": usd_clp,
                "fx_clp_usd": clp_usd,
                "fx_usd_clp": usd_clp,
                "fx_ts": datetime.datetime.utcnow().isoformat() + "Z",
                "fx_fallback": False,
            }
        except Exception:
            clp_usd = 0.0011
            usd_clp = 1.0 / clp_usd
            return {
                "fx_base": base,
                "fx_quote": quote,
                "fx_rate": clp_usd,
                "fx_clp_per_usd": usd_clp,
                "fx_clp_usd": clp_usd,
                "fx_usd_clp": usd_clp,
                "fx_ts": datetime.datetime.utcnow().isoformat() + "Z",
                "fx_fallback": True,
            }

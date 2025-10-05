# Hotel Andino — Semana 8 (MVP)

Prototipo funcional con **Django 5.2.7**, **Oracle (oracledb)** y consumo de **API externa** de tipo de cambio (CLP ↔ USD).

## Requisitos
- Python 3.12
- Oracle XE local (Docker) con service name `XEPDB1`
- Usuario Oracle: `hotel` / Pass: `duoc2024`

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración
`hotel_s7/settings.py` ya apunta a Oracle:
```
ENGINE: django.db.backends.oracle
NAME: 127.0.0.1:1521/XEPDB1
USER: hotel
PASSWORD: duoc2024
```

## Datos de demostración
```bash
python manage.py loaddata fixtures/demo.json
```

## Ejecutar
```bash
python manage.py runserver
```
- Home: http://127.0.0.1:8000/
- Buscar: http://127.0.0.1:8000/buscar/
- Listado: http://127.0.0.1:8000/habitaciones/?checkin=2025-10-15&checkout=2025-10-18
- API FX: http://127.0.0.1:8000/api/fx/?base=CLP&quote=USD
- Admin: http://127.0.0.1:8000/admin/

## Notas
- El banner superior muestra CLP ↔ USD usando `exchangerate.host` y fallback.
- Admin ya registra: **Habitación** y **Reserva**.

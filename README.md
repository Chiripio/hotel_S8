# 🏨 Hotel S8 — MVP Semana 8

Proyecto de **Ingeniería de Software (PRY3211)** — Semana 8  
Caso: **Sistema de Reservas de Hotel**

## 🚀 Tecnologías
- Django 4.2
- Python 3.9
- SQLite (BD de pruebas incluida)

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Chiripio/hotel_S7.git
   cd hotel_S7
   ```

2. Crear y activar entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar migraciones y cargar datos de prueba:
   ```bash
   python manage.py migrate
   python manage.py loaddata reservas/fixtures/seed.json
   ```

5. Iniciar servidor:
   ```bash
   python manage.py runserver
   ```

## 🖥️ Funcionalidades MVP
- Home (`/`)
- Buscar habitaciones por fechas (`/buscar`)
- Listado de habitaciones disponibles (`/habitaciones`)
- Detalle de habitación (`/habitaciones/<id>`)
- Reserva con validaciones (`/reservar/<id>`)
- Confirmación de reserva (`/reserva/<id>/confirmada`)

## 📦 Datos de prueba
- 5 habitaciones (Individual, Dobles, Suites)
- 3 reservas pre-cargadas para validar solapamientos

## ✅ Casos de prueba principales
- Fechas válidas → muestra disponibles
- Fecha salida ≤ entrada → error
- Reserva exitosa → confirmación con ID
- Reserva solapada → bloqueo con mensaje

---

✍️ *Desarrollado por Eduardo (Chiripio) para el ramo Ingeniería de Software*

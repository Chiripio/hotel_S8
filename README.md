# 🏨 Hotel S8 — MVP Semana 8

Este proyecto corresponde al **Mínimo Producto Viable (MVP)** solicitado en la **Semana 8 de Ingeniería de Software**.  
El objetivo fue desarrollar un sistema funcional de reservas de hotel, conectado a una **base de datos Oracle**, con integración a un **servicio externo de tipo de cambio (CLP ↔ USD)**, cumpliendo los criterios de la rúbrica de esta semana.

---

## ✅ Funcionalidades implementadas

1. **Búsqueda de habitaciones** por rango de fechas (check-in / check-out).
2. **Listado de habitaciones disponibles**, con validación automática de solapamiento.
3. **Detalle individual de habitación** (tipo, capacidad, precio).
4. **Formulario de reserva**, con validaciones y registro en base de datos Oracle.
5. **Página de confirmación** con datos de la reserva creada.
6. **Integración de API externa:**  
   - Se consulta la API `https://api.exchangerate.host/latest` para mostrar el tipo de cambio CLP ↔ USD.  
   - Si la API falla, el sistema usa un **valor de respaldo** (fallback).
7. **Panel de administración Django** con modelos `Habitacion` y `Reserva` registrados.
8. **Datos precargados** (fixture `fixtures/demo.json`) con 3 habitaciones y una reserva.

---

## 🧱 Arquitectura general

- **Backend:** Django 5.2.7  
- **Base de datos:** Oracle XE (Docker local, `service_name = XEPDB1`)  
- **Conector:** `oracledb` 3.3.0  
- **API externa:** `exchangerate.host`  
- **Frontend:** Plantillas HTML nativas con integración de datos dinámicos (`fx_base`, `fx_usd_clp`, `fx_clp_usd`, etc.)

---

## ⚙️ Configuración de base de datos (en `hotel_s7/settings.py`)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '127.0.0.1:1521/XEPDB1',
        'USER': 'hotel',
        'PASSWORD': 'duoc2024',
        'HOST': '127.0.0.1',
        'PORT': '1521',
    }
}
```

> ✅ Conexión verificada.  
> Se confirmaron 3 habitaciones en Oracle mediante script de prueba:  
> `Habitaciones en Oracle: 3`

---

## 🧩 Modelos principales

### Habitacion
- tipo (CharField)  
- capacidad (IntegerField)  
- precio_noche (IntegerField)

### Reserva
- habitacion (ForeignKey → Habitacion)
- fecha_entrada / fecha_salida  
- nombre / email

Validaciones implementadas:
- Rango de fechas válido.  
- Evita solapamiento de reservas existentes.

---

## 💻 Instalación y ejecución

```bash
# 1. Crear entorno
python -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Cargar datos de demostración
python manage.py loaddata fixtures/demo.json

# 4. Ejecutar el servidor
python manage.py runserver
```

---

## 🌐 Rutas principales

| Ruta | Descripción |
|------|--------------|
| `/` | Página principal (Home con tipo de cambio CLP↔USD) |
| `/buscar/` | Formulario de búsqueda por fechas |
| `/habitaciones/` | Listado de habitaciones disponibles |
| `/habitaciones/<id>/` | Detalle de habitación |
| `/reservar/<id>/` | Formulario de reserva |
| `/api/fx/` | Endpoint JSON con tipo de cambio CLP↔USD |
| `/admin/` | Panel de administración Django |

---

## 🧪 Validación de la rúbrica Semana 8

| Criterio | Cumplimiento |
|-----------|--------------|
| MVP funcional (mínimo viable) | ✅ |
| Conexión a base de datos Oracle | ✅ |
| Inserciones y consultas reales | ✅ |
| API externa funcional (con fallback) | ✅ |
| Persistencia y validación de reservas | ✅ |
| Entorno virtual + requirements.txt | ✅ |
| Estructura de proyecto en GitHub | ✅ [Repositorio](https://github.com/Chiripio/hotel_S8) |

---

## 📦 Dependencias principales

```
Django==5.2.7
oracledb==3.3.0
requests==2.32.5
```

---

## 👤 Autor
**Eduardo Guerrero**  
Correo: [edua.guerrero@gmail.com](mailto:edua.guerrero@gmail.com)  
Proyecto desarrollado para Duoc UC — *Ingeniería de Software, Semana 8 (MVP Funcional)*.

# 🌿 Tz'ib'al Ulew — Plan de Desarrollo

App de escritorio para registrar salidas de campo, documentar especies encontradas y visualizar expediciones en un mapa interactivo.

---

## 🧭 Visión general

CampoLog es una herramienta para naturalistas, biólogos o entusiastas que salen al campo y quieren documentar sus hallazgos de forma estructurada — sin depender de internet, con todo en local.

Es el complemento de escritorio de [Uk'ux Ulew](https://github.com/Adriianh/ukux-ulew) (app web 3D para visualizar biodiversidad de Guatemala). Los datos recolectados en campo con Tz'ib'al Ulew pueden exportarse y sincronizarse opcionalmente con Uk'ux Ulew.

---

## 🛠 Stack tecnológico

| Capa | Herramienta | Rol |
|---|---|---|
| UI de escritorio | **PyQt6** | Ventanas, formularios, layout |
| Mapa interactivo | **Folium + QWebEngineView** | Mapa Leaflet embebido en la ventana |
| API local | **FastAPI + Uvicorn** | Lógica de negocio, endpoints REST |
| Validación | **Pydantic v2** | Modelos de datos tipados |
| ORM | **SQLAlchemy 2.0** | Abstracción de base de datos |
| Base de datos | **SQLite** | Persistencia local sin servidor |
| Migraciones | **Alembic** | Control de versiones del esquema |
| Tipado estático | **mypy** | Verificación de tipos en desarrollo (como TypeScript para Python) |
| Formato + lint | **ruff** | Linter y formatter unificado (ultrarrápido, escrito en Rust) |
| Tests | **pytest + pytest-qt** | Pruebas unitarias y de UI |
| Sync con Uk'ux Ulew | **módulo `sync/`** | Exportación a JSON/CSV compatible con Uk'ux Ulew |

---

## 🏗 Arquitectura: convivencia FastAPI + PyQt6

FastAPI y PyQt6 corren en **procesos separados**:

```
┌─────────────────────────────────────────────────┐
│  main.py (QProcess)                             │
│  ┌──────────────┐     ┌──────────────────────┐  │
│  │ FastAPI       │     │ PyQt6 UI            │  │
│  │ (proceso hijo)│ ◄── │ (proceso padre)     │  │
│  │ :8000         │ HTTP │ QMainWindow         │  │
│  │ SQLAlchemy    │     │ httpx → API         │  │
│  │ SQLite        │     │ Folium/WebEngine    │  │
│  └──────────────┘     └──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

- `main.py` lanza FastAPI como proceso hijo con `QProcess` y luego levanta la ventana PyQt6.
- La UI se comunica con la API vía HTTP (`httpx`).
- Si la UI crashea, la API puede seguir corriendo.
- En desarrollo se pueden correr por separado (`uvicorn api.main:app` y `python -m ui.app`).
- Endpoint interno `POST /shutdown` para que la UI apague la API limpiamente al cerrar.

**Alternativa considerada (descartada):** `QThread` + `uvicorn.run()` en el mismo proceso. Se descartó porque:
- Mezcla event loops (asyncio de uvicorn + Qt loop).
- Si la API crashea, arrastra la UI.
- Más difícil de depurar.

---

## 📁 Estructura del proyecto

```
campolog/
├── main.py                     # Punto de entrada — lanza API (QProcess) + UI
├── config.py                   # Configuración centralizada (rutas, puerto, DB_URL)
│
├── core/                       # Lógica compartida entre API y UI
│   ├── __init__.py
│   └── logging_config.py       # Configuración de logging centralizada
│
├── api/
│   ├── __init__.py
│   ├── main.py                 # App FastAPI, registro de routers
│   ├── database.py             # Configuración SQLAlchemy + sesión
│   ├── dependencies.py         # Dependencias compartidas (get_db, etc.)
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── salida.py
│   │   ├── especie.py
│   │   └── registro.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── salida.py
│   │   ├── especie.py
│   │   └── registro.py
│   │
│   └── routers/                # Endpoints agrupados por recurso
│       ├── __init__.py
│       ├── salidas.py
│       ├── especies.py
│       ├── registros.py
│       ├── mapa.py
│       └── stats.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py                  # Ventana principal (QMainWindow)
│   │
│   ├── views/                  # Vistas/páginas de la app
│   │   ├── __init__.py
│   │   ├── dashboard_view.py   # Resumen inicial
│   │   ├── salidas_view.py     # Lista y detalle de salidas
│   │   ├── nueva_salida.py     # Formulario nueva salida
│   │   ├── especies_view.py    # Catálogo de especies
│   │   ├── mapa_view.py        # Mapa interactivo embebido
│   │   └── estadisticas.py     # Dashboard de resumen
│   │
│   └── widgets/                # Componentes reutilizables
│       ├── __init__.py
│       ├── mapa_widget.py
│       └── tabla_widget.py
│
├── sync/                       # Sincronización con Uk'ux Ulew
│   ├── __init__.py
│   ├── exporter.py             # Exportar a JSON/CSV compatible con Uk'ux Ulew
│   └── types.py                # Tipos compartidos entre ambas apps
│
├── tests/                      # Tests con pytest
│   ├── __init__.py
│   ├── conftest.py             # Fixtures: db de prueba, cliente HTTP test
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── test_salidas.py
│   │   ├── test_especies.py
│   │   ├── test_registros.py
│   │   └── test_stats.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── test_views.py
│
├── alembic/                    # Migraciones de base de datos
├── assets/                     # Íconos, estilos QSS
├── alembic.ini
├── pyproject.toml              # Configuración centralizada (pytest, mypy, ruff)
├── requirements.txt
└── README.md
```

**Nota:** Todos los `__init__.py` permiten importar limpiamante: `from api.models.salida import Salida`.

---

## 🗄 Modelos de datos

### Salida
```python
class Salida(Base):
    id: int
    nombre: str              # "Expedición Volcán Tajumulco"
    fecha: date
    lugar: str               # Nombre del lugar
    latitud: float
    longitud: float
    altitud_m: float | None
    clima: str | None        # "Nublado", "Lluvia ligera"
    temperatura_c: float | None
    notas: str | None
    creado_en: datetime
```

### Especie
```python
class Especie(Base):
    id: int
    nombre_comun: str        # "Quetzal"
    nombre_cientifico: str   # "Pharomachrus mocinno"
    tipo: str                # "fauna" | "flora" | "fungi" | "otro"
    descripcion: str | None
```

### Registro
```python
class Registro(Base):
    id: int
    salida_id: int           # FK → Salida
    especie_id: int          # FK → Especie
    cantidad: int | None
    notas: str | None
    foto_path: str | None    # Ruta local a imagen
    creado_en: datetime
```

---

## 🌐 Endpoints FastAPI

### Salidas
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/salidas` | Lista todas las salidas |
| GET | `/salidas/{id}` | Detalle de una salida |
| POST | `/salidas` | Crear nueva salida |
| PUT | `/salidas/{id}` | Editar salida |
| DELETE | `/salidas/{id}` | Eliminar salida |
| GET | `/salidas/{id}/registros` | Registros de una salida |

### Especies
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/especies` | Lista especies (con filtro por tipo) |
| GET | `/especies/{id}` | Detalle de especie |
| POST | `/especies` | Crear especie |
| PUT | `/especies/{id}` | Editar especie |

### Registros
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/registros` | Añadir registro a una salida |
| PUT | `/registros/{id}` | Editar registro |
| DELETE | `/registros/{id}` | Eliminar registro |

### Mapa
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/mapa/puntos` | Todos los puntos para el mapa (lat, lng, resumen) |

### Estadísticas
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/stats/resumen` | Total salidas, especies únicas, registros |
| GET | `/stats/top-especies` | Especies más frecuentes |
| GET | `/stats/por-mes` | Salidas agrupadas por mes |

### Sistema (internos, para la UI)
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/shutdown` | Apaga la API limpiamente (llamado por la UI al cerrar) |
| GET | `/health` | Health check para que la UI sepa que la API está lista |

---

## 🖥 Vistas de la UI

### 1. Dashboard / Inicio
- Resumen rápido: salidas este mes, especies únicas, último avistamiento
- Acceso rápido a "Nueva salida"

### 2. Mapa interactivo
- Mapa Leaflet embebido con todos los puntos de salidas
- Click en punto → popup con nombre, fecha, especies encontradas
- Filtro por rango de fechas o tipo de especie

### 3. Salidas
- Tabla/lista de todas las salidas ordenadas por fecha
- Click en salida → detalle con registros encontrados
- Botón "Nueva salida" → formulario

### 4. Formulario nueva salida
- Campos: nombre, fecha, lugar, coordenadas (picker en mapa mini), clima, temperatura, notas
- Sección para añadir registros (especie + cantidad + foto + notas)
- Autocompletado de especies ya registradas

### 5. Especies
- Catálogo de todas las especies con filtro por tipo
- Modal para crear/editar especie

### 6. Estadísticas
- Gráficas simples: salidas por mes, top 10 especies, distribución flora/fauna

---

## 🗓 Roadmap de desarrollo

### Fase 0 — Setup del proyecto (Día 1)
- [ ] Crear entorno virtual y `pyproject.toml` con dependencias
- [ ] Configurar ruff (linter + formatter) y mypy (type checking)
- [ ] Configurar pytest y escribir `conftest.py` con fixtures básicas
- [ ] Crear `config.py` con rutas y configuraciones centralizadas
- [ ] Estructura de directorios con `__init__.py`
- [ ] `.gitignore` y primer commit

### Fase 1 — Backend (Semanas 1–2)
- [ ] Configuración de SQLAlchemy + SQLite
- [ ] Modelos ORM: Salida, Especie, Registro
- [ ] Migraciones iniciales con Alembic
- [ ] Schemas Pydantic para request/response
- [ ] Endpoints CRUD de Salidas
- [ ] Endpoints CRUD de Especies
- [ ] Endpoints de Registros
- [ ] Endpoint `/mapa/puntos`
- [ ] Endpoints de estadísticas
- [ ] Endpoints `/health` y `/shutdown`
- [ ] Tests de API con pytest + httpx TestClient
- [ ] Pruebas manuales con Swagger UI

### Fase 2 — UI base (Semanas 3–4)
- [ ] Setup PyQt6, ventana principal con navegación lateral
- [ ] `main.py` con lanzamiento de API via QProcess + health check
- [ ] Vista de Salidas (lista + detalle) conectada a la API
- [ ] Formulario nueva salida conectado a la API local
- [ ] Catálogo de Especies
- [ ] Dashboard / Inicio con resumen desde `/stats/resumen`
- [ ] Tests de UI con pytest-qt

### Fase 3 — Mapa interactivo (Semana 5)
- [ ] Integrar Folium para generar HTML del mapa
- [ ] Embeber con QWebEngineView
- [ ] Popups con info de cada salida
- [ ] Regenerar mapa al añadir/editar salidas
- [ ] Filtros en mapa (rango de fechas, tipo de especie)

### Fase 4 — Pulido (Semana 6)
- [ ] Vista de estadísticas con gráficas (matplotlib o pyqtgraph)
- [ ] Subida y visualización de fotos por registro
- [ ] Exportar datos a CSV/JSON
- [ ] Módulo `sync/` para exportar a formato compatible con Uk'ux Ulew
- [ ] Manejo de errores y validaciones en UI
- [ ] Estilos QSS para UI consistente
- [ ] Pasada de mypy y ruff a todo el proyecto

---

## 📦 Dependencias principales

```
# App
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic[email]
PyQt6
PyQt6-WebEngine
folium
httpx
pillow
matplotlib

# Calidad
mypy
ruff

# Tests
pytest
pytest-qt
```

---

## ⚙️ Configuración de herramientas

### pyproject.toml (esquema inicial)
```toml
[project]
name = "campolog"
version = "0.1.0"
requires-python = ">=3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
strict = true
python_version = "3.11"

[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]

[tool.ruff.format]
quote-style = "double"
```

---

## 🚀 Cómo correr el proyecto (objetivo final)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr migraciones
alembic upgrade head

# Lanzar la app (inicia FastAPI + PyQt6 simultáneamente)
python main.py
```

Durante desarrollo:
```bash
# Terminal 1: API sola
uvicorn api.main:app --reload

# Terminal 2: UI sola (apuntando a la API en :8000)
python -m ui.app

# Tests
pytest -v

# Type checking
mypy .

# Lint + format
ruff check .
ruff format .
```

---

## 🔗 Conexión con Uk'ux Ulew

Tz'ib'al Ulew y Uk'ux Ulew comparten el mismo dominio de datos (biodiversidad de Guatemala). El módulo `sync/` se encarga de:

1. **Exportar**: convertir salidas, registros y especies a JSON/CSV con estructura compatible con Uk'ux Ulew.
2. **Estructura compartida**: los tipos en `sync/types.py` reflejan los mismos campos que Uk'ux Ulew espera.
3. **Sincronización futura**: en una versión posterior, la app podría enviar datos directamente a Uk'ux Ulew via API.

Esto asegura que ambos proyectos puedan coexistir e intercambiar datos sin fricción.

---

## 💡 Posibles extensiones futuras

- Importar datos de GBIF o eBird para enriquecer el catálogo de especies
- Exportar salidas como PDF con mapa incluido
- Sincronización bidireccional con Uk'ux Ulew
- Modo oscuro en la UI
- Mapas offline (tiles descargados para uso sin internet)
- Reconocimiento de especies por foto (ML)

# Imagineria Visual

Aplicacion web Django para entrenamiento estructurado de **imagineria visual**: un programa de 8 semanas basado en neurociencia, con un catalogo curado de 35 obras de arte organizadas en 6 fases de complejidad creciente.

El sistema entrena la capacidad del cerebro para crear, mantener y manipular imagenes mentales, progresando desde geometria simple (Malevich, *Cuadrado Negro*) hasta reconstruccion completa de escenas (Vermeer, *El arte de la pintura*).

---

## Tabla de contenidos

- [Caracteristicas principales](#caracteristicas-principales)
- [Modo Flat Affect (TEPT)](#modo-flat-affect-tept)
- [Stack tecnologico](#stack-tecnologico)
- [Instalacion](#instalacion)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelos de datos](#modelos-de-datos)
- [Rutas y vistas](#rutas-y-vistas)
- [JavaScript y funcionalidad cliente](#javascript-y-funcionalidad-cliente)
- [PWA](#pwa)
- [Comandos de gestion](#comandos-de-gestion)
- [Template tags personalizados](#template-tags-personalizados)
- [Base neurocientifica](#base-neurocientifica)
- [Licencia](#licencia)

---

## Caracteristicas principales

- **Catalogo de 35 obras** organizadas en 6 fases, cada una dirigida a areas cerebrales especificas (V1, V4, FFA, PPA, LOC, etc.)
- **Sesiones de entrenamiento inmersivas** con temporizador de visualizacion (countdown) y fase de retencion (countup) en pantalla completa
- **Image Streaming** (metodo Win Wenger) con temporizador dedicado, barra de progreso y prompts rotativos cada 2 minutos
- **Autoevaluacion post-sesion** con escalas de vivacidad, estabilidad y nivel de detalle (1-10)
- **Capturas de campo** para registrar eventos de imagineria visual espontanea o deliberada en la vida diaria
- **Cuestionario VVIQ** completo (16 items) para medir la capacidad de imagineria visual con seguimiento de linea base
- **Panel de progreso** con graficos Chart.js: evolucion de ratings, sesiones por fase, evolucion VVIQ
- **Programa de 8 semanas** con calendario, mapeo semana-fase, conteo de sesiones y semanas de consolidacion
- **Modo oscuro** con toggle persistente via cookie
- **PWA** con service worker que cachea las imagenes de Wikimedia para acceso offline
- **Aplicacion de usuario unico** — sin autenticacion, diseñada como herramienta personal

---

## Modo Flat Affect (TEPT)

La aplicacion incluye un modo adaptado para personas con aplanamiento afectivo por TEPT cronico estabilizado. Al activar este modo:

- Las obras se reordenan para diferir las emocionalmente intensas (categoria C al final)
- Las instrucciones se enfocan en descripcion perceptual (forma, color, textura) en lugar de engagement emocional
- Aparecen checkboxes adicionales para rastrear indicadores emocionales sutiles (cambio prosodia, reaccion corporal)
- El protocolo de Image Streaming se presenta en 3 fases progresivas (perceptual -> material -> noticing)
- Se muestran prompts de re-exposicion gradual para obras especificas

El modo se configura en **Ajustes** (`/settings/`).

---

## Stack tecnologico

| Componente | Tecnologia |
|------------|------------|
| Framework | Django 6.0 |
| Base de datos | SQLite3 |
| CSS | Tailwind CSS 3.4.17 (binario standalone, sin Node.js) |
| Graficos | Chart.js 4.4.7 (CDN) |
| Formularios | django-widget-tweaks |
| PWA | manifest.json + Service Worker |
| Modo oscuro | Estrategia `class` de Tailwind con cookie |
| Idioma | Español (`es`), timezone `Europe/Madrid` |

---

## Instalacion

### Requisitos previos

- Python 3.12+

### Pasos

```bash
# 1. Clonar el repositorio
git clone git@github.com:AEGISL0L/para-la-imagineria.git
cd para-la-imagineria

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Cargar datos de referencia (16 areas cerebrales, 6 fases, 5 metodos, 35 obras)
python manage.py seed_artworks

# 6. (Opcional) Corregir URLs de imagenes de Wikimedia
python manage.py fix_urls

# 7. Ejecutar el servidor
python manage.py runserver
```

La aplicacion estara disponible en `http://127.0.0.1:8000/`.

### Recompilar Tailwind CSS (opcional)

El repositorio incluye el CSS compilado (`static/css/output.css`) y un binario standalone de Tailwind. Si modificas estilos:

```bash
./tailwindcss -i static/css/input.css -o static/css/output.css --watch
```

---

## Uso

### Flujo tipico de una sesion

1. Ir a **Sesion** → seleccionar una obra del catalogo
2. Elegir duracion de visualizacion (30, 60 o 90 segundos)
3. La sesion inmersiva inicia en pantalla completa:
   - **Fase de visualizacion**: la obra se muestra con countdown
   - **Fase de retencion**: pantalla negra, cerrar los ojos y retener la imagen mental (countup)
4. Autoevaluacion: calificar vivacidad, estabilidad y detalle (1-10)
5. Revisar resultados de la sesion

### Controles de teclado en sesion

| Tecla | Accion |
|-------|--------|
| `Espacio` / `Enter` | Iniciar visualizacion / Terminar retencion |
| `Escape` | Abortar sesion |

### Image Streaming

Herramienta independiente accesible desde **Streaming** en el menu. Temporizador configurable (10/15/20 minutos) con prompts que guian la descripcion verbal de imagenes mentales.

### Capturas de campo

Registrar eventos de imagineria visual en la vida diaria desde **Capturas** → **Nueva captura**. Clasificar por tipo (FFA=caras, PPA=lugares, NAV=navegacion, etc.), condiciones y calidad.

### VVIQ

Cuestionario estandarizado de 16 items para medir la vivacidad de la imagineria visual. El primer resultado se establece automaticamente como linea base.

---

## Estructura del proyecto

```
.
├── imagery/                    # Proyecto Django (settings, urls, wsgi/asgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── training/                   # App principal
│   ├── models.py               # 8 modelos (ver seccion Modelos)
│   ├── views.py                # 19 vistas (ver seccion Rutas)
│   ├── urls.py                 # Rutas con namespace "training"
│   ├── forms.py                # 5 formularios
│   ├── admin.py                # Admin personalizado para los 8 modelos
│   ├── apps.py                 # Configuracion de la app
│   ├── context_processors.py   # Inyecta UserProfile en todo template
│   ├── templatetags/
│   │   └── training_tags.py    # 5 filtros personalizados
│   ├── management/commands/
│   │   ├── seed_artworks.py    # Carga datos de referencia
│   │   └── fix_urls.py         # Corrige URLs de Wikimedia
│   └── migrations/
├── templates/
│   ├── base.html               # Template base (Tailwind, dark mode, SW)
│   ├── components/
│   │   ├── _navbar.html        # Barra de navegacion responsive
│   │   └── _artwork_card.html  # Tarjeta reutilizable de obra
│   └── training/               # 18 templates de vistas
├── static/
│   ├── css/
│   │   ├── input.css           # Componentes Tailwind (@layer)
│   │   └── output.css          # CSS compilado
│   ├── js/
│   │   ├── session-timer.js    # Motor de sesion inmersiva
│   │   ├── image-streaming-timer.js  # Temporizador Image Streaming
│   │   └── charts.js           # Graficos Chart.js de progreso
│   ├── img/                    # Imagenes estaticas
│   ├── manifest.json           # Configuracion PWA
│   └── sw.js                   # Service Worker (cache de imagenes)
├── tailwindcss                 # Binario standalone Tailwind CSS
├── manage.py
└── requirements.txt
```

---

## Modelos de datos

### BrainArea
Area cerebral involucrada en el procesamiento visual.

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `code` | CharField(10) | Codigo unico: V1, FFA, PFC, etc. |
| `name` | CharField(100) | Nombre completo |
| `description` | TextField | Descripcion neurocientifica |
| `analogy` | TextField | Analogia para no especialistas |

### Phase
Fase de entrenamiento (1-6).

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `number` | SmallInt(1-6) | Numero de fase |
| `title` | CharField(200) | Titulo de la fase |
| `objective` | TextField | Objetivos de aprendizaje |
| `protocol_instructions` | TextField | Instrucciones paso a paso |
| `primary_circuits` | M2M → BrainArea | Areas cerebrales que entrena |

### TrainingMethod
Metodo de entrenamiento (MET-1 a MET-5).

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `code` | CharField(10) | MET-1 a MET-5 |
| `name` | CharField(200) | Nombre del metodo |
| `protocol_steps` | TextField | Protocolo estandar |
| `adaptation_flat_affect` | TextField | Version adaptada para TEPT |
| `implementable_in_app` | BooleanField | Implementable en la app (MET-1, MET-4) |

### Artwork
Obra de arte del catalogo (35 obras).

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `catalog_id` | CharField(10) | F1-01 a F6-06 |
| `phase` | FK → Phase | Fase de entrenamiento |
| `order_standard` | SmallInt | Orden en modo estandar |
| `order_flat_affect` | SmallInt | Orden en modo flat affect |
| `artist` | CharField(200) | Artista |
| `title` | CharField(300) | Titulo de la obra |
| `year` | CharField(50) | Año o rango |
| `wikimedia_url` | URLField(500) | URL de imagen en Wikimedia |
| `emotional_category` | Char(1): A/B/C | A=sin dependencia, B=parcial, C=alta |
| `brain_areas` | M2M → BrainArea | Areas cerebrales objetivo |
| `training_purpose` | TextField | Proposito de entrenamiento |
| `instructions_standard` | TextField | Instrucciones modo estandar |
| `instructions_flat_affect` | TextField | Instrucciones modo flat affect |
| `emotional_intensity_level` | SmallInt(0-3) | Nivel de intensidad emocional |
| `reexposure_prompt` | TextField | Prompt de re-exposicion gradual |

### UserProfile
Perfil de usuario (singleton, pk=1).

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `mode` | CharField: standard/flat_affect | Modo de entrenamiento |
| `program_start_date` | DateField | Inicio del programa de 8 semanas |
| `current_phase` | FK → Phase | Fase actual |
| `vviq_baseline` | SmallInt(16-80) | Puntuacion VVIQ inicial |

### TrainingSession
Sesion de entrenamiento individual.

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `artwork` | FK → Artwork | Obra de la sesion |
| `session_type` | CharField | standard / image_streaming / free |
| `viewing_duration` | Int | Segundos de visualizacion |
| `retention_duration` | Int | Segundos de retencion |
| `vividness_rating` | SmallInt(1-10) | Calificacion de vivacidad |
| `stability_rating` | SmallInt(1-10) | Calificacion de estabilidad |
| `detail_rating` | SmallInt(1-10) | Calificacion de detalle |
| `emotional_response` | TextField | Respuesta emocional (texto libre) |
| `emotional_indicator_detected` | Boolean | Indicador emocional detectado |
| `prosody_change_noted` | Boolean | Cambio de prosodia detectado |
| `body_reaction_noted` | Boolean | Reaccion corporal detectada |
| `notes` | TextField | Notas |

### FieldCapture
Captura de campo (imagineria en la vida diaria).

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `capture_type` | CharField | FFA/EBA/PPA/OPA/NAV/OBJ/COLOR/MOTION/MULTI/OTHER |
| `quality` | SmallInt(1-10) | Calidad de la imagineria |
| `description` | TextField | Descripcion del evento |
| `eyes_open` | Boolean | Con ojos abiertos |
| `in_motion` | Boolean | En movimiento |
| `deliberate` | Boolean | Deliberada vs espontanea |
| `immediate_retention` | Boolean | Retencion inmediata |
| `session_end_retention` | Boolean | Retencion al final del dia |
| `next_day_retention` | Boolean | Retencion al dia siguiente |
| `repetition_count` | SmallInt | Repeticiones deliberadas |

### VVIQResponse
Resultado del cuestionario VVIQ.

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `total_score` | SmallInt(16-80) | Puntuacion total |
| `item_scores` | JSONField | Puntuaciones individuales (16 items) |
| `context` | CharField(100) | Contexto: "baseline", "semana 4", etc. |

---

## Rutas y vistas

| Ruta | Vista | Descripcion |
|------|-------|-------------|
| `/` | `dashboard` | Panel principal: estadisticas, fases, sesiones y capturas recientes |
| `/catalog/` | `catalog` | Galeria de las 35 obras, filtrable por fase y categoria emocional |
| `/catalog/<id>/` | `artwork_detail` | Detalle de obra: imagen, metadata, instrucciones, areas cerebrales, historial |
| `/phase/<n>/` | `phase_detail` | Detalle de fase: objetivo, protocolo, circuitos, obras |
| `/program/` | `program` | Programa de 8 semanas con calendario y conteo de sesiones |
| `/session/start/` | `session_start` | Selector de obra para iniciar sesion |
| `/session/start/<id>/` | `session_start_artwork` | Configuracion pre-sesion (duracion) |
| `/session/<pk>/view/` | `session_view` | Sesion inmersiva (pantalla completa) |
| `/session/<pk>/assess/` | `session_assess` | Autoevaluacion post-sesion |
| `/session/<pk>/` | `session_detail` | Resultados de sesion completada |
| `/sessions/` | `session_log` | Historial de sesiones, filtrable por fase |
| `/image-streaming/` | `image_streaming` | Temporizador Image Streaming |
| `/captures/` | `capture_list` | Lista de capturas de campo |
| `/captures/new/` | `capture_new` | Registrar nueva captura |
| `/progress/` | `progress` | Dashboard de progreso con graficos |
| `/vviq/` | `vviq` | Cuestionario VVIQ (16 items) |
| `/settings/` | `settings_view` | Ajustes: modo, fecha inicio, linea base VVIQ |
| `/api/session/<pk>/update-timing/` | API | Actualiza tiempos de sesion (POST, JSON) |
| `/api/progress-data/` | API | Datos para graficos de progreso (GET, JSON) |

---

## JavaScript y funcionalidad cliente

### Motor de sesion (`session-timer.js`)

Controla la experiencia inmersiva de entrenamiento:

1. **Pantalla de inicio** — click o tecla para comenzar
2. **Fase de visualizacion** — la obra se muestra con countdown configurable (30/60/90s)
3. **Campana de transicion** — sonido WAV integrado (base64) al cambiar de fase
4. **Fase de retencion** — pantalla negra con countup, el usuario cierra los ojos
5. **Guardado** — POST via `fetch()` con tiempos reales a la API, redirige a evaluacion

Solicita pantalla completa, oculta la barra de navegacion y aplica fondo negro total.

### Temporizador Image Streaming (`image-streaming-timer.js`)

- Duraciones configurables: 10, 15 o 20 minutos
- Controles: Iniciar / Pausar / Reiniciar
- Barra de progreso visual
- 8 prompts rotativos cada 2 minutos guiando la descripcion verbal
- Campana al completar

### Graficos de progreso (`charts.js`)

Tres visualizaciones Chart.js con datos de `/api/progress-data/`:

1. **Evolucion de ratings** (linea): vivacidad, estabilidad, detalle en el tiempo
2. **Sesiones por fase** (barras): distribucion de practica por fase
3. **Evolucion VVIQ** (linea): puntuacion total a lo largo del programa

---

## PWA

La aplicacion funciona como Progressive Web App:

- **`manifest.json`**: nombre "Imagineria Visual", display standalone, tema indigo (#4f46e5)
- **Service Worker** (`sw.js`):
  - Estrategia cache-first para imagenes de Wikimedia (`upload.wikimedia.org`)
  - Cachea las obras en primer acceso para visualizacion offline
  - Placeholder SVG de fallback cuando no hay conexion
  - Cache `imagery-v1` con auto-limpieza de versiones anteriores

Instalable desde el navegador como app independiente.

---

## Comandos de gestion

### `seed_artworks`

```bash
python manage.py seed_artworks
```

Carga todos los datos de referencia en la base de datos:

- **16 areas cerebrales**: V1, V2, V3A, V4, V5/MT, LOC, FFA, EBA, STS, PPA, OPA, IPS, RETRO, AMIG, PFC, PAR — con descripciones neurocientificas y analogias
- **6 fases** con objetivos, protocolos e instrucciones
- **5 metodos** de entrenamiento (con adaptaciones flat affect)
- **35 obras** de Malevich, Mondrian, Kelly, Albers, Vasarely, Riley, Escher, Zurbaran, Morandi, Chardin, Hopper, de Chirico, Hokusai, O'Keeffe, af Klint, Vermeer, Turner
- **1 UserProfile** singleton

Idempotente — usa `update_or_create`, se puede ejecutar multiples veces.

### `fix_urls`

```bash
python manage.py fix_urls
```

Corrige URLs de imagenes de Wikimedia para las 35 obras del catalogo.

---

## Template tags personalizados

Disponibles en `{% load training_tags %}`:

| Filtro | Uso | Descripcion |
|--------|-----|-------------|
| `get_item` | `{{ dict\|get_item:key }}` | Acceso a diccionario por clave |
| `multiply` | `{{ value\|multiply:arg }}` | Multiplicacion aritmetica |
| `format_duration` | `{{ seconds\|format_duration }}` | Formatea segundos a `M:SS` |
| `emotional_category_badge` | `{{ cat\|emotional_category_badge }}` | Clases Tailwind para badge A/B/C |
| `phase_color` | `{{ number\|phase_color }}` | Clase de color Tailwind por fase |

---

## Base neurocientifica

### Las 6 fases y la jerarquia visual

El programa sigue la jerarquia del procesamiento visual del cerebro:

| Fase | Foco | Areas cerebrales | Obras ejemplo |
|------|------|-----------------|---------------|
| 1 | Formas y colores solidos | V1, V4 | Malevich, Mondrian, Kelly |
| 2 | Patrones y profundidad | V2, V3A, IPS | Vasarely, Riley, Escher |
| 3 | Objetos y superficies | LOC, V4 | Zurbaran, Morandi, Chardin |
| 4 | Espacios y atmosferas | PPA, OPA, RETRO | Hopper, de Chirico, Hokusai |
| 5 | Formas organicas y movimiento | V4, V5/MT, FFA | O'Keeffe, af Klint |
| 6 | Escenas complejas (integracion) | Multi-area | Vermeer, Turner |

### Categorias emocionales de las obras

- **A** (verde): sin dependencia emocional — funciona igual en ambos modos
- **B** (amarillo): dependencia parcial — instrucciones adaptadas en flat affect
- **C** (rojo): alta dependencia emocional — diferidas en flat affect, con re-exposicion gradual

### Programa de 8 semanas

| Semana | Fases | Tipo |
|--------|-------|------|
| 1 | 1-2 | Introduccion |
| 2 | 2-3 | Progresion |
| 3 | 3-4 | Progresion |
| 4 | 4-5 | Progresion |
| 5 | 5-6 | Progresion |
| 6 | 5-6 | Consolidacion |
| 7 | 6 | Integracion |
| 8 | 1-6 | Consolidacion final |

### VVIQ (Vividness of Visual Imagery Questionnaire)

Cuestionario estandarizado de 16 items (Marks, 1973). Cada item se evalua de 1 (sin imagen) a 5 (tan vivida como ver realmente). Rango total: 16-80. Se usa como metrica de progreso a lo largo del programa.

---

## Licencia

Es software libre.

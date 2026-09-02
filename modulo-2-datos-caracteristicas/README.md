# Módulo 2 — Datos: preprocesamiento e ingeniería de características (S4–S5, 7 h)

> Estado: **contenido pendiente** (Fase 2 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

## Objetivos

Al finalizar el módulo, el estudiante será capaz de recolectar datos de distintas fuentes,
diagnosticar y corregir sus problemas de calidad, explorarlos con criterio estadístico y
construir características informativas dentro de un `Pipeline` reproducible que no filtre
información del conjunto de prueba.

## Contenidos

### ✅ Núcleo

- **S4** — Datos estructurados vs. no estructurados. Lectura desde CSV, SQL y API.
- **S4** — Valores faltantes (mecanismos y estrategias de imputación), duplicados y outliers.
- **S4** — Análisis exploratorio de datos (EDA): distribuciones, relaciones, visualización.
- **S5** — Escalado y normalización. Codificación de variables categóricas. Transformaciones.
- **S5** — Selección de características: filtro (`SelectKBest`), envoltura (RFE) y embebidos.
- **S5** — `Pipeline` y `ColumnTransformer` como forma canónica de encadenar el
  preprocesamiento.
- **S5** — **Fuga de datos** (data leakage): qué es, cómo se cuela y cómo evitarla.

### 🔵 Opcional

- Web scraping con `requests` y BeautifulSoup.
- Datos desbalanceados desde la perspectiva del preprocesamiento (se retoma en S9).
- Creación de características a partir de fechas y coordenadas geográficas.

## Materiales

### Teoría

| # | Documento | Sesión | Tema | Estado |
|---|---|---|---|---|
| 01 | `teoria/01-recoleccion-datos.md` | S4 | Fuentes, formatos, estructurados vs. no estructurados, scraping | ⬜ |
| 02 | `teoria/02-limpieza-y-calidad.md` | S4 | Faltantes, duplicados, outliers, consistencia | ⬜ |
| 03 | `teoria/03-analisis-exploratorio.md` | S4 | EDA: qué mirar y qué decisiones se derivan | ⬜ |
| 04 | `teoria/04-ingenieria-caracteristicas.md` | S5 | Escalado, codificación, transformaciones, creación de variables | ⬜ |
| 05 | `teoria/05-seleccion-y-pipelines.md` | S5 | Filtro, envoltura, embebidos; `Pipeline`, `ColumnTransformer`, fuga de datos | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-limpieza-eda-aplicado.ipynb` | aplicado | Diagnóstico y limpieza de un dataset real + EDA completo | ⬜ |
| 02 | `notebooks/02-webscraping-aplicado.ipynb` 🔵 | aplicado | Extracción de una tabla web con BeautifulSoup | ⬜ |
| 03 | `notebooks/03-fuga-de-datos-intuicion.ipynb` | intuición | Demostración del sobreoptimismo al escalar antes de partir los datos | ⬜ |
| 04 | `notebooks/04-pipeline-caracteristicas-aplicado.ipynb` | aplicado | `ColumnTransformer` + selección de características de punta a punta | ⬜ |

### Datos

| Archivo | Descripción | Variables | Estado |
|---|---|---|---|
| — | Dataset conductor del módulo, pendiente de elegir (candidato heredado: Titanic) | — | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-limpieza.md` | `ej01-limpieza-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-pipeline.md` | `ej02-pipeline-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-2.md` | `quiz/quiz-modulo-2-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E2 — Datos.** EDA del caso, decisiones de limpieza justificadas y `Pipeline` de
preprocesamiento reproducible. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../environment.yml`](../environment.yml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

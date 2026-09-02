# Módulo 6 — MLOps: trazabilidad y despliegue (S14, 3.5 h)

> Estado: **contenido pendiente** (Fase 6 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

## Objetivos

Al finalizar el módulo, el estudiante será capaz de registrar y comparar experimentos de
forma trazable, versionar y empaquetar un modelo entrenado, exponerlo como un servicio HTTP
consumible por otras aplicaciones, y describir cómo se monitorea su desempeño en producción.

## Contenidos

### ✅ Núcleo

- **S14** — MLflow: tracking de experimentos, comparación de runs, model registry.
- **S14** — Serialización y versionado del modelo. Del notebook al artefacto reproducible.
- **S14** — APIs: qué son, métodos HTTP relevantes, contrato de entrada y salida.
- **S14** — API de inferencia con **FastAPI**: endpoints `/health` y `/predict`, validación
  del payload.
- **S14** — Empaquetado con **Docker**.
- **S14** — Monitoreo en producción: **drift** de datos y de concepto; criterios de
  reentrenamiento.

### 🔵 Opcional

- Integración continua para proyectos de ML (tests del pipeline, linting de notebooks).
- Alternativas de despliegue: servicios gestionados, contenedores en la nube.
- Cierre: sustentación de los proyectos integradores.

## Materiales

### Teoría

| # | Documento | Tema | Estado |
|---|---|---|---|
| 01 | `teoria/01-trazabilidad-mlflow.md` | Tracking, runs, métricas, artefactos, model registry | ⬜ |
| 02 | `teoria/02-apis-para-modelos.md` | Qué es una API, métodos HTTP, diseño del contrato de predicción | ⬜ |
| 03 | `teoria/03-empaquetado-y-despliegue.md` | Serialización, Docker, entornos de ejecución | ⬜ |
| 04 | `teoria/04-monitoreo-y-drift.md` | Drift de datos y de concepto, métricas en producción, reentrenamiento | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-mlflow-aplicado.ipynb` | aplicado | Registrar experimentos, comparar runs y promover un modelo | ⬜ |
| 02 | `notebooks/02-drift-intuicion.ipynb` | intuición | Simular drift y ver cómo se degrada el desempeño | ⬜ |

### Código de despliegue

| Ruta | Contenido | Estado |
|---|---|---|
| `api/main.py` | API FastAPI con `/health` y `/predict` | ⬜ |
| `api/esquemas.py` | Validación del payload de entrada y salida | ⬜ |
| `api/README.md` | Cómo ejecutar y probar la API localmente | ⬜ |
| `docker/Dockerfile` | Imagen del servicio de inferencia | ⬜ |
| `docker/README.md` | Construcción y ejecución del contenedor | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-mlflow.md` | `ej01-mlflow-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-api.md` | `ej02-api-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-6.md` | `quiz/quiz-modulo-6-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E6 — Entrega final.** Modelo registrado en MLflow, expuesto como API, más el informe final
del caso y su sustentación. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Docker solo se necesita en este módulo; si no puedes instalarlo, la sesión incluye la
> alternativa de ejecutar la API con `uvicorn`. Ver
> [`../docs/guia-entorno.md`](../docs/guia-entorno.md).

# Curso de Machine Learning

Repositorio educativo del curso de **Machine Learning** de la Maestría en Ingeniería de
Sistemas y Computación (Universidad Tecnológica de Pereira) — **48 horas**, 14 sesiones de
3.5 h distribuidas en 7 semanas. Material en español, con teoría en `.md` (LaTeX) y notebooks
ejecutables en **Python**.

Docente: MSc. Délany Ramírez del Río — `delram@utp.edu.co`

## 📚 Programa

| Módulo | Sesiones | Tema | Carpeta |
|---|---|---|---|
| 0 | antes de S1 | Instalación del software (tutorial para estudiantes) | [`modulo-0-instalacion/`](modulo-0-instalacion/) |
| 1 | S1–S3 | Fundamentos y ciclo de vida | [`modulo-1-fundamentos-ciclo-vida/`](modulo-1-fundamentos-ciclo-vida/) |
| 2 | S4–S5 | Datos: preprocesamiento e ingeniería de características | [`modulo-2-datos-caracteristicas/`](modulo-2-datos-caracteristicas/) |
| 3 | S6–S8 | Supervisado I: regresión y evaluación | [`modulo-3-regresion-evaluacion/`](modulo-3-regresion-evaluacion/) |
| 4 | S9–S11 | Supervisado II: clasificación y ensambles | [`modulo-4-clasificacion-ensambles/`](modulo-4-clasificacion-ensambles/) |
| 5 | S12–S13 | No supervisado y deep learning | [`modulo-5-no-supervisado-deep-learning/`](modulo-5-no-supervisado-deep-learning/) |
| 6 | S14 | MLOps: trazabilidad y despliegue | [`modulo-6-mlops-despliegue/`](modulo-6-mlops-despliegue/) |
| — | — | Proyecto integrador | [`proyecto-integrador/`](proyecto-integrador/) |
| — | — | Recursos generales | [`recursos/`](recursos/) |

El detalle de contenidos sesión por sesión está en [`docs/programa.md`](docs/programa.md),
que es la **fuente de verdad** del curso.

Cada módulo sigue la misma estructura: `teoria/` · `notebooks/` · `datos/` · `ejercicios/` ·
`quiz/`.

## 🗂️ Estructura del repositorio

```
ml/
├── docs/
│   ├── programa.md               # malla de 14 sesiones (fuente de verdad)
│   ├── convenciones.md           # estilo .md/LaTeX, notebooks, nombres, commits
│   └── guia-entorno.md           # instalación (versión corta)
├── modulo-0-instalacion/
│   ├── README.md                 # tutorial de instalación para estudiantes + FAQ
│   └── verificar-entorno.py      # script que comprueba el entorno
├── modulo-1-fundamentos-ciclo-vida/
│   ├── teoria/   notebooks/   datos/   ejercicios/   quiz/
├── modulo-2-datos-caracteristicas/          (misma sub-estructura)
├── modulo-3-regresion-evaluacion/           (misma sub-estructura)
├── modulo-4-clasificacion-ensambles/        (misma sub-estructura)
├── modulo-5-no-supervisado-deep-learning/   (misma sub-estructura)
├── modulo-6-mlops-despliegue/               (+ api/  docker/)
├── proyecto-integrador/
├── recursos/
├── pyproject.toml / uv.lock      # entorno del curso (uv); requirements.txt como respaldo pip
└── PLAN.md                       # bitácora de construcción del repositorio
```

## ⚙️ Puesta en marcha

Si es tu primera vez con Python, `uv` o Git, sigue el tutorial completo de
[`modulo-0-instalacion/`](modulo-0-instalacion/) (instalación por sistema operativo, FAQ y
solución de problemas). El resumen para quien ya conoce las herramientas:

**Opción A — uv (recomendada):** con [uv](https://docs.astral.sh/uv/) instalado, desde la
raíz del repositorio:

```bash
uv sync
```

```bash
uv run python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
```

```bash
uv run jupyter lab
```

**Opción B — venv + pip** (requiere Python 3.11):

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

Verifica la instalación con `uv run modulo-0-instalacion/verificar-entorno.py`. Referencia
corta en [`docs/guia-entorno.md`](docs/guia-entorno.md).

## 📝 Evaluación

- **Proyecto integrador** (6 entregas, una por módulo): un caso único que crece durante todo
  el curso hasta desplegarse como API con trazabilidad. Ver
  [`proyecto-integrador/`](proyecto-integrador/).
- **Quiz teórico por módulo**: en la carpeta `quiz/` de cada módulo.
- **Ejercicios guiados**: en la carpeta `ejercicios/` de cada módulo.

## 🛠️ Para el docente

- [`PLAN.md`](PLAN.md) lleva la bitácora de construcción del repositorio: qué fases están
  hechas y cuáles faltan. Se actualiza al cerrar cada fase.
- Los archivos `*-sol.md` (soluciones de ejercicios y claves de quiz) son material del
  docente. Si vas a compartir el repositorio con los estudiantes, considera publicar una rama
  o release sin ellos.

## 📄 Licencia

Contenido educativo bajo [CC BY 4.0](LICENSE); el código (notebooks y scripts) además bajo
MIT. Los datasets de terceros conservan la licencia de sus fuentes originales.

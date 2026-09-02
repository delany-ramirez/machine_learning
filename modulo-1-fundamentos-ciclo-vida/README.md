# Módulo 1 — Fundamentos y ciclo de vida (S1–S3, 10.5 h)

> Estado: **contenido pendiente** (Fase 1 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

## Objetivos

Al finalizar el módulo, el estudiante será capaz de encuadrar un problema real como una tarea
de Machine Learning, describir y aplicar el ciclo de vida de un proyecto de ML con control de
versiones de código y datos, y manejar el andamiaje matemático (álgebra lineal, gradientes y
probabilidad) sobre el que se construyen los algoritmos del curso.

## Contenidos

### ✅ Núcleo

- **S1** — Definición y alcance del ML. IA vs. ML vs. DL. Tipos de aprendizaje: supervisado,
  no supervisado y por refuerzo. Taxonomía de problemas. Cuándo *no* usar ML.
- **S1** — Ecosistema Python y primer flujo `fit`/`predict` de punta a punta.
- **S2** — Las 7 etapas del ciclo de vida. Definición del problema: métricas de negocio vs.
  métricas técnicas. Estructura de un proyecto de ML.
- **S2** — Control de versiones con Git; versionado de datos con DVC.
- **S3** — Álgebra lineal con NumPy: vectores, matrices, producto punto, normas y distancias.
  Descomposiciones (eigen, SVD).
- **S3** — Cálculo: derivadas, gradientes y regla de la cadena. Probabilidad: distribuciones
  y teorema de Bayes.

### 🔵 Opcional

- Historia y oleadas de la IA; panorama de aplicaciones por sector.
- Flujos de trabajo con Git en equipo (ramas, pull requests) aplicados a proyectos de datos.

## Materiales

### Teoría

| # | Documento | Sesión | Tema | Estado |
|---|---|---|---|---|
| 01 | `teoria/01-que-es-machine-learning.md` | S1 | Definición, IA/ML/DL, tipos de aprendizaje, taxonomía de problemas | ⬜ |
| 02 | `teoria/02-ciclo-de-vida.md` | S2 | Las 7 etapas; métricas de negocio vs. técnicas | ⬜ |
| 03 | `teoria/03-versionado-codigo-datos.md` | S2 | Git y DVC en proyectos de ML | ⬜ |
| 04 | `teoria/04-algebra-lineal.md` | S3 | Vectores, matrices, normas, distancias, eigen y SVD | ⬜ |
| 05 | `teoria/05-calculo-y-probabilidad.md` | S3 | Gradientes, regla de la cadena, distribuciones, Bayes | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-primer-modelo-aplicado.ipynb` | aplicado | Flujo mínimo y completo de punta a punta: datos → modelo → evaluación | ⬜ |
| 02 | `notebooks/02-proyecto-reproducible-aplicado.ipynb` | aplicado | Estructura de proyecto, semillas, versionado de datos con DVC | ⬜ |
| 03 | `notebooks/03-algebra-lineal-intuicion.ipynb` | intuición | NumPy desde cero; SVD calculada a mano y verificada | ⬜ |
| 04 | `notebooks/04-gradientes-intuicion.ipynb` | intuición | Derivadas numéricas y descenso del gradiente en 1D (prepara S6) | ⬜ |

### Datos

| Archivo | Descripción | Variables | Estado |
|---|---|---|---|
| — | Dataset conductor del módulo, pendiente de elegir | — | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-encuadre-problema.md` | `ej01-encuadre-problema-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-algebra-gradientes.md` | `ej02-algebra-gradientes-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-1.md` | `quiz/quiz-modulo-1-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E1 — Definición del problema.** Encuadrar el caso como tarea de ML, definir la variable
objetivo y las métricas de éxito (de negocio y técnicas), y montar el repositorio con Git y
DVC. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../environment.yml`](../environment.yml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

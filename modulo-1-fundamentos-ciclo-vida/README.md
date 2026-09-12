# Módulo 1 — Fundamentos y ciclo de vida (S1–S3, 10.5 h)

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
- Pipelines de DVC para encadenar etapas reproducibles.

## Materiales

### Teoría

| # | Documento | Sesión | Tema |
|---|---|---|---|
| 01 | [`teoria/01-que-es-machine-learning.md`](teoria/01-que-es-machine-learning.md) | S1 | Definición operativa, IA/ML/DL, tipos de aprendizaje, encuadre de problemas, cuándo no usar ML |
| 02 | [`teoria/02-ciclo-de-vida.md`](teoria/02-ciclo-de-vida.md) | S2 | Las 7 etapas, definición del problema, métricas de negocio vs. técnicas, dónde fracasan los proyectos |
| 03 | [`teoria/03-versionado-codigo-datos.md`](teoria/03-versionado-codigo-datos.md) | S2 | Git aplicado a datos, qué versionar, DVC |
| 04 | [`teoria/04-algebra-lineal.md`](teoria/04-algebra-lineal.md) | S3 | Producto punto, normas, distancias, covarianza, vectores propios, SVD |
| 05 | [`teoria/05-calculo-y-probabilidad.md`](teoria/05-calculo-y-probabilidad.md) | S3 | Gradientes, descenso, regla de la cadena, pérdidas, Bayes, máxima verosimilitud |

### Notebooks

| # | Notebook | Tipo | Contenido |
|---|---|---|---|
| 01 | [`notebooks/01-primer-modelo-aplicado.ipynb`](notebooks/01-primer-modelo-aplicado.ipynb) | aplicado | Flujo completo: encuadre, partición, `fit`/`predict`, métricas, referencia trivial, residuales |
| 02 | [`notebooks/02-proyecto-reproducible-aplicado.ipynb`](notebooks/02-proyecto-reproducible-aplicado.ipynb) | aplicado | Ciclo de vida, estructura de proyecto y los 4 niveles de reproducibilidad (semilla, entorno, datos, modelo) |
| 03 | [`notebooks/03-algebra-lineal-intuicion.ipynb`](notebooks/03-algebra-lineal-intuicion.ipynb) | intuición | NumPy desde cero: producto punto, normas, distancias, covarianza, eigen y SVD |
| 04 | [`notebooks/04-gradientes-intuicion.ipynb`](notebooks/04-gradientes-intuicion.ipynb) | intuición | Derivadas, descenso 1D y 2D, tasa de aprendizaje, regla de la cadena, regresión sin scikit-learn |

### Datos

**Dataset conductor del módulo:** `rendimiento-estudiantes.csv`

| Archivo | Descripción | Variables |
|---|---|---|
| [`datos/rendimiento-estudiantes.csv`](datos/rendimiento-estudiantes.csv) | 400 estudiantes ficticios de posgrado. **Datos sintéticos** con semilla fija: conocemos los coeficientes que los generaron, lo que permite verificar si el modelo los recupera | `id_estudiante`, `programa` (4 niveles), `edad` (21–48), `estrato` (1–6), `trabaja` (0/1), `promedio_anterior` (2.0–5.0), `horas_estudio_semana`, `asistencia_pct` (40–100), `nota_final` (0–5, objetivo de regresión), `aprobo` (0/1, objetivo de clasificación; 74 % positivos) |
| [`datos/generar-rendimiento-estudiantes.py`](datos/generar-rendimiento-estudiantes.py) | Script generador con `SEMILLA = 42`. Ejecutarlo reproduce el CSV byte a byte | — |

> **Por qué datos simulados.** Sin problemas de licencia ni privacidad, y con una ventaja
> pedagógica que ningún dataset real ofrece: como conocemos el proceso generador, podemos
> comparar lo que el modelo *estima* con la verdad. El módulo 2 pasa a datos reales, con toda
> su suciedad.
>
> **Ojo:** `aprobo` se deriva de `nota_final`. Usar una para predecir la otra es fuga de
> datos, y el notebook 01 lo señala explícitamente.

### Ejercicios

| # | Enunciado | Solución | Duración | Tipo |
|---|---|---|---|---|
| 01 | [`ejercicios/ej01-encuadre-problema.md`](ejercicios/ej01-encuadre-problema.md) | [`ej01-encuadre-problema-sol.md`](ejercicios/ej01-encuadre-problema-sol.md) | 45 min | Sin código |
| 02 | [`ejercicios/ej02-algebra-gradientes.md`](ejercicios/ej02-algebra-gradientes.md) | [`ej02-algebra-gradientes-sol.md`](ejercicios/ej02-algebra-gradientes-sol.md) | 90 min | Con código |

El ejercicio 01 trabaja el encuadre de un caso de deserción estudiantil y la detección de
fugas de datos (incluida una fuga por retroalimentación, difícil de ver). El 02 recorre
álgebra lineal y descenso del gradiente con NumPy, y muestra empíricamente por qué hay que
estandarizar.

### Quiz

| Enunciado | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-1.md`](quiz/quiz-modulo-1.md) | [`quiz-modulo-1-sol.md`](quiz/quiz-modulo-1-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E1 — Definición del problema.** Encuadrar el caso como tarea de ML, definir la variable
objetivo y las métricas de éxito (de negocio y técnicas), y montar el repositorio con Git y
DVC. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

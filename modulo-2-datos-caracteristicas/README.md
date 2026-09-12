# Módulo 2 — Datos: preprocesamiento e ingeniería de características (S4–S5, 7 h)

## Objetivos

Al finalizar el módulo, el estudiante será capaz de recolectar datos de distintas fuentes,
diagnosticar y corregir sus problemas de calidad **con criterio y no con recetas**, explorarlos
con rigor estadístico, y construir características informativas dentro de un `Pipeline`
reproducible que no filtre información del conjunto de prueba.

## Contenidos

### ✅ Núcleo

- **S4** — Datos estructurados vs. no estructurados. Lectura desde CSV, SQL y API. Diccionario
  de datos y disponibilidad temporal. Marco legal (Ley 1581, RGPD).
- **S4** — Valores faltantes: mecanismos MCAR, MAR y MNAR, y qué imputación admite cada uno.
  Faltantes disfrazados. Duplicados reales vs. aparentes. Outliers: error, valor legítimo u
  otra población.
- **S4** — Análisis exploratorio: univariante, bivariante y multivariante. Interacciones.
  Las cuatro trampas de la correlación.
- **S5** — Escalado, codificación de categóricas y transformaciones de distribución.
- **S5** — Creación de variables: combinar, descomponer, indicadores, agregaciones,
  interacciones. Cómo **demostrar** que una variable aporta.
- **S5** — Selección de características: filtro, envoltura y embebidos.
- **S5** — `Pipeline` y `ColumnTransformer`. **Fuga de datos**: tipos, magnitudes medidas y
  cómo evitarla.

### 🔵 Opcional

- Web scraping con `requests` y BeautifulSoup; ética, `robots.txt` y legalidad.
- Codificación por objetivo (*target encoding*) y alta cardinalidad.
- Imputación iterativa y por KNN.

## Materiales

### Teoría

| # | Documento | Sesión | Tema |
|---|---|---|---|
| 01 | [`teoria/01-recoleccion-datos.md`](teoria/01-recoleccion-datos.md) | S4 | Fuentes, formatos, diccionario de datos, marco legal y sesgo de representatividad |
| 02 | [`teoria/02-limpieza-y-calidad.md`](teoria/02-limpieza-y-calidad.md) | S4 | MCAR/MAR/MNAR, duplicados, outliers, calidad |
| 03 | [`teoria/03-analisis-exploratorio.md`](teoria/03-analisis-exploratorio.md) | S4 | EDA univariante, bivariante y multivariante; interacciones |
| 04 | [`teoria/04-ingenieria-caracteristicas.md`](teoria/04-ingenieria-caracteristicas.md) | S5 | Escalado, codificación, transformaciones, creación de variables |
| 05 | [`teoria/05-seleccion-y-pipelines.md`](teoria/05-seleccion-y-pipelines.md) | S5 | Selección, `Pipeline`, `ColumnTransformer`, fuga de datos |

### Notebooks

| # | Notebook | Tipo | Contenido |
|---|---|---|---|
| 01 | [`notebooks/01-limpieza-eda-aplicado.ipynb`](notebooks/01-limpieza-eda-aplicado.ipynb) | aplicado | Diagnóstico completo del Titanic: redundancia, fuga, mecanismos de ausencia, duplicados, outliers, EDA e interacción sexo × clase |
| 02 🔵 | [`notebooks/02-webscraping-aplicado.ipynb`](notebooks/02-webscraping-aplicado.ipynb) | aplicado | BeautifulSoup, `read_html`, conversión de tipos, ética y `robots.txt` |
| 03 | [`notebooks/03-fuga-de-datos-intuicion.ipynb`](notebooks/03-fuga-de-datos-intuicion.ipynb) | intuición | **Medición** del sobreoptimismo de cada tipo de fuga, con error estándar |
| 04 | [`notebooks/04-pipeline-caracteristicas-aplicado.ipynb`](notebooks/04-pipeline-caracteristicas-aplicado.ipynb) | aplicado | `ColumnTransformer`, variables nuevas, selección, artefacto desplegable |

> **El notebook 03 es el corazón del módulo.** Sobre ruido puro —donde no hay absolutamente
> nada que aprender— seleccionar características fuera de la validación produce un 81 % de
> accuracy. Hecho bien, da 46 %. Y midiendo con error estándar sobre 100 particiones, el sesgo
> del escalado y de la imputación resulta **indistinguible de cero**, mientras el de la
> selección llega a +13 puntos. Ese sentido de la proporción es lo que suele faltar cuando se
> enseña fuga de datos.

### Datos

**Dataset conductor del módulo:** `titanic.csv`

| Archivo | Descripción | Por qué este |
|---|---|---|
| [`datos/titanic.csv`](datos/titanic.csv) | 891 pasajeros, 15 columnas. Dominio público, vía [seaborn-data](https://github.com/mwaskom/seaborn-data) | Está sucio de todas las formas interesantes: `age` 19.9 % nulo (MAR), `deck` 77.2 % nulo (MNAR), `alive` es una **fuga de datos que viene de fábrica**, `class`/`embark_town`/`adult_male` son redundantes, 107 filas idénticas que **no** son duplicados, y outliers legítimos (un bebé de 5 meses, tarifas de 512) |
| [`datos/descargar-titanic.py`](datos/descargar-titanic.py) | Script de descarga idempotente | Documenta la procedencia exacta |
| [`datos/matriculas-sucio.csv`](datos/matriculas-sucio.csv) | 620 solicitudes de admisión, **sintéticas**, con 11 defectos plantados | Dataset del ejercicio 01: el estudiante hace el diagnóstico sin haberlo visto antes |
| [`datos/generar-matriculas-sucio.py`](datos/generar-matriculas-sucio.py) | Generador con semilla fija; documenta cada defecto plantado | Reproducible byte a byte |
| [`datos/pagina-ejemplo.html`](datos/pagina-ejemplo.html) | Página HTML local para el notebook de scraping | Evita depender de una web viva que cambie y rompa el notebook |

### Ejercicios

| # | Enunciado | Solución | Duración |
|---|---|---|---|
| 01 | [`ejercicios/ej01-limpieza.md`](ejercicios/ej01-limpieza.md) | [`ej01-limpieza-sol.md`](ejercicios/ej01-limpieza-sol.md) | 90 min |
| 02 | [`ejercicios/ej02-pipeline.md`](ejercicios/ej02-pipeline.md) | [`ej02-pipeline-sol.md`](ejercicios/ej02-pipeline-sol.md) | 90 min |

El ejercicio 01 pide diagnosticar `matriculas-sucio.csv`, que tiene **nueve problemas
distintos**, incluidos dos faltantes disfrazados que `isna()` no detecta y una mezcla de
duplicados reales y aparentes. El 02 lo convierte en un `Pipeline` desplegable y hace medir al
estudiante las tres fugas sobre sus propios datos.

### Quiz

| Enunciado | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-2.md`](quiz/quiz-modulo-2.md) | [`quiz-modulo-2-sol.md`](quiz/quiz-modulo-2-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E2 — Datos.** EDA del caso, decisiones de limpieza justificadas y `Pipeline` de
preprocesamiento reproducible. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

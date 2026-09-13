# Convenciones del repositorio

Guía de estilo y reproducibilidad para todo el material del curso. Toda fase de construcción
registrada en [`../PLAN.md`](../PLAN.md) debe respetar estas convenciones.

La fuente de verdad sobre **qué** se enseña y en qué orden es
[`programa.md`](programa.md); este documento define **cómo** se escribe.

## 1. Estructura de cada módulo

```
modulo-N-nombre/
├── README.md        # índice del módulo: objetivos, contenidos núcleo/opcional, rutas
├── teoria/          # documentos .md con LaTeX (uno por tema)
├── notebooks/       # .ipynb ejecutables (solo Python)
├── datos/           # datasets .csv usados por notebooks y ejercicios
├── ejercicios/      # enunciados y soluciones
└── quiz/            # quiz teórico de cierre de módulo + clave
```

El módulo 6 añade `api/` y `docker/` por su naturaleza de despliegue.

## 2. Núcleo vs. opcional

Cada README de módulo clasifica los contenidos:

- ✅ **Núcleo** — material evaluable, imprescindible.
- 🔵 **Opcional** — profundización o lecturas para ampliar.

Usar estos emojis de forma consistente en títulos y tablas de contenido.

## 3. Estilo de los `.md` con LaTeX

- Fórmulas **inline** con `$...$`: por ejemplo $\hat{y} = \mathbf{X}\boldsymbol{\beta}$.
- Fórmulas en **bloque** con `$$...$$` en su propia línea, con líneas en blanco alrededor.
  Nunca dos bloques `$$` consecutivos sin texto o línea en blanco entre ellos.
- Notación estándar (Hastie et al., *The Elements of Statistical Learning*):
  $\mathbf{X} \in \mathbb{R}^{n \times p}$ matriz de diseño, $y$ variable objetivo,
  $\hat{y}$ predicción, $\boldsymbol{\beta}$ o $\boldsymbol{\theta}$ parámetros,
  $\mathcal{L}$ función de pérdida, $\lambda$ hiperparámetro de regularización.
- Un archivo `.md` por tema, con encabezado `# Título` y una sección de objetivos al inicio.
- Reservar los bloques de código para Python; las tablas de resultados en Markdown.
- Idioma: **español**. Términos técnicos en inglés entre paréntesis la primera vez que
  aparecen (p. ej. "fuga de datos (data leakage)"), y en redonda a partir de ahí.

## 4. Notebooks ejecutables

Todos los notebooks son de **Python** (no hay versión en R, a diferencia del curso `doe`).

### 4.1 Dos tipos de notebook por tema

Esta es la convención central del curso. Cada tema puede tener uno o ambos:

| Tipo | Sufijo | Propósito |
|---|---|---|
| **Intuición** | `-intuicion` | El concepto desde cero: datos sintéticos y el algoritmo implementado a mano (bucles, NumPy) **antes** de llamar a la librería. Responde *por qué funciona*. |
| **Aplicado** | `-aplicado` | Dataset real y flujo completo con `Pipeline`, validación y métricas. Responde *cómo se usa bien*. |

Un tema simple puede tener solo el aplicado; un tema puramente conceptual, solo el de
intuición. Nunca dos notebooks que cubran lo mismo.

### 4.2 Cómo se escriben

Los notebooks se redactan primero como `.py` en **formato percent** (`# %%` / `# %% [markdown]`)
y se convierten con [`../herramientas/percent2ipynb.py`](../herramientas/percent2ipynb.py).

La razón es práctica: el `.py` se puede **ejecutar como script** para comprobar que corre sin
errores antes de publicarlo, y produce diffs legibles mientras se redacta.

```bash
python herramientas/percent2ipynb.py borrador.py --solo-codigo
```

```bash
python herramientas/percent2ipynb.py borrador.py modulo-N/notebooks/NN-tema.ipynb
```

Los archivos `.py` intermedios no se versionan: el entregable es el `.ipynb`.

### 4.3 Reglas de ejecución

- Los notebooks **deben ejecutarse de principio a fin sin errores** con el entorno de
  [`../pyproject.toml`](../pyproject.toml).
- Leer los datos desde `../datos/` con rutas relativas; **nunca** rutas absolutas.
- Fijar la semilla aleatoria siempre que haya aleatoriedad: definir `SEMILLA = 42` en la
  celda de importaciones y pasarla a `random_state=SEMILLA`.
- Primera celda (Markdown): título, sesión a la que pertenece, objetivos y lista de paquetes.
- **Primera celda de código: el arranque para Google Colab**, etiquetada `colab-arranque`. En
  Colab clona el repositorio y hace `%cd` a la carpeta del notebook para que `../datos` exista
  (e instala con `%pip` lo que Colab no trae); **en local no hace nada**. La genera
  [`../herramientas/celda_colab.py`](../herramientas/celda_colab.py) y `percent2ipynb.py` la
  inserta al convertir; no se escribe a mano ni se edita en el notebook.
- Siguiente celda (código): importaciones y `SEMILLA`.
- Guardar los notebooks **con las salidas limpias** (`Kernel → Restart & Clear Output`) para
  que los diffs de git sean legibles.
- Si un dataset debe descargarse, hacerlo en una celda idempotente que compruebe primero si
  el archivo ya existe en `../datos/`.

### 4.4 Un dataset canónico por módulo

Cada módulo tiene un **dataset conductor** que se usa en la mayoría de sus notebooks, para
que el estudiante profundice en un problema en vez de saltar entre datasets. Los notebooks de
intuición pueden usar datos sintéticos; los ejercicios pueden usar un dataset secundario.

## 5. Convención de nombres

| Elemento | Patrón | Ejemplo |
|---|---|---|
| Módulo | `modulo-N-tema-corto/` | `modulo-3-regresion-evaluacion/` |
| Teoría | `NN-tema-corto.md` | `01-regresion-lineal.md` |
| Notebook | `NN-tema-corto-{intuicion\|aplicado}.ipynb` | `01-descenso-gradiente-intuicion.ipynb` |
| Datos | `nombre-descriptivo.csv` | `ames-housing.csv` |
| Script de datos | `descargar-nombre.py` | `descargar-wine-quality.py` |
| Ejercicio | `ejNN-tema.md` (+ `ejNN-tema-sol.md`) | `ej01-residuales.md` |
| Quiz | `quiz-modulo-N.md` (+ `-sol.md`) | `quiz-modulo-3.md` |

La numeración `NN` es **continua dentro del módulo** y coherente con el orden de sesiones de
`programa.md`.

## 6. Datos

- Formato `.csv` con encabezados claros en `snake_case` sin tildes, separador coma, punto
  decimal.
- Se versionan en git los datasets **menores a 1 MB**. Los mayores se descargan con un script
  documentado (`descargar-*.py`) y quedan excluidos en `.gitignore`.
- Los datasets simulados incluyen siempre el script generador con semilla fija.
- Documentar cada dataset (origen, licencia, variables, unidades) en una tabla del README del
  módulo.

## 7. Ejercicios y quizzes

- Cada ejercicio tiene **enunciado** y **solución** en archivos separados; la solución es
  material del docente.
- El enunciado indica: objetivo, datos a usar, pasos esperados y tiempo estimado.
- El quiz de módulo tiene entre 8 y 12 preguntas conceptuales (no de código memorístico), con
  clave de respuestas comentada en el archivo `-sol.md`.

## 8. Commits

- Un commit por fase completada de [`../PLAN.md`](../PLAN.md), o por hito claro dentro de una
  fase.
- Mensaje en español, imperativo: `Fase 3: módulo 3 (regresión, regularización, evaluación)`.
- Actualizar `PLAN.md` en el mismo commit que cierra la fase.

## 9. Material de la edición anterior

`contenido_anterior/` guarda las diapositivas y notebooks de la edición previa. Es
**insumo de referencia, no plantilla**: sirve para consultar alcance, datasets y ejemplos,
pero el contenido se reescribe. No se versiona en git (está en `.gitignore`) y ningún archivo
del curso nuevo debe enlazar hacia esa carpeta.

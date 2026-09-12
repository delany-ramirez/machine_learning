# Módulo 5 — No supervisado y deep learning (S12–S13, 7 h)

> Estado: **contenido pendiente** (Fase 5 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

## Objetivos

Al finalizar el módulo, el estudiante será capaz de descubrir estructura en datos sin
etiquetas mediante clustering y reducción de dimensionalidad, validar los grupos obtenidos, y
comprender los fundamentos de una red neuronal —arquitectura, retropropagación y
entrenamiento— con criterio para decidir cuándo un problema tabular no necesita deep learning.

## Contenidos

### ✅ Núcleo

- **S12** — Clustering particional: K-Means y K-Means++. Clustering jerárquico aglomerativo y
  dendrograma. Clustering por densidad: DBSCAN.
- **S12** — Validación de clusters: método del codo, coeficiente de silueta, índice de
  Davies-Bouldin. Cómo elegir $k$.
- **S12** — Reducción de dimensionalidad: PCA (varianza explicada, cargas, scree plot) y
  t-SNE.
- **S13** — Perceptrón y perceptrón multicapa (MLP). Funciones de activación.
- **S13** — Retropropagación: la regla de la cadena de S3 aplicada a una red.
- **S13** — Entrenamiento en PyTorch: optimizadores, batches, early stopping, dropout.
- **S13** — Cuándo *no* usar deep learning: comparación honesta contra los ensambles de S11
  en datos tabulares.

### 🔵 Opcional

- UMAP como alternativa moderna a t-SNE.
- Detección de anomalías (Isolation Forest, DBSCAN como detector de ruido).
- Vistazo a redes convolucionales (CNN) y transfer learning.

## Materiales

### Teoría

| # | Documento | Sesión | Tema | Estado |
|---|---|---|---|---|
| 01 | `teoria/01-clustering.md` | S12 | K-Means, jerárquico, DBSCAN; supuestos de cada uno | ⬜ |
| 02 | `teoria/02-validacion-clusters.md` | S12 | Codo, silueta, Davies-Bouldin; interpretación de grupos | ⬜ |
| 03 | `teoria/03-reduccion-dimensionalidad.md` | S12 | PCA (a partir del SVD de S3), t-SNE, UMAP | ⬜ |
| 04 | `teoria/04-redes-neuronales.md` | S13 | Perceptrón, MLP, activaciones, retropropagación | ⬜ |
| 05 | `teoria/05-entrenamiento-y-limites.md` | S13 | Optimizadores, regularización, cuándo no usar DL | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-clustering-intuicion.ipynb` | intuición | K-Means implementado a mano; comparación de los tres algoritmos | ⬜ |
| 02 | `notebooks/02-clustering-aplicado.ipynb` | aplicado | Segmentación real: elección de $k$, validación e interpretación | ⬜ |
| 03 | `notebooks/03-pca-tsne-intuicion.ipynb` | intuición | PCA paso a paso desde la matriz de covarianza; t-SNE comparado | ⬜ |
| 04 | `notebooks/04-mlp-intuicion.ipynb` | intuición | Retropropagación a mano en NumPy sobre una red mínima | ⬜ |
| 05 | `notebooks/05-mlp-pytorch-aplicado.ipynb` | aplicado | MLP en PyTorch vs. Gradient Boosting sobre datos tabulares | ⬜ |

### Datos

| Archivo | Descripción | Variables | Estado |
|---|---|---|---|
| — | Dataset conductor del módulo, pendiente de elegir | — | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-clustering.md` | `ej01-clustering-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-pca.md` | `ej02-pca-sol.md` | ⬜ |
| 03 | `ejercicios/ej03-mlp.md` | `ej03-mlp-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-5.md` | `quiz/quiz-modulo-5-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E5 — Exploración no supervisada.** Segmentación del caso (o variante con MLP) y qué aporta
al problema original. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> **Nota sobre el alcance de S13.** Esta sesión es un **puente** hacia el curso especializado
> de Deep Learning del programa. Da el fundamento (arquitectura, retropropagación,
> entrenamiento) y el criterio para decidir cuándo usarlo, no una cobertura completa del área.

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

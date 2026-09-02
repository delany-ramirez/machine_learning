# Módulo 4 — Supervisado II: clasificación y ensambles (S9–S11, 10.5 h)

> Estado: **contenido pendiente** (Fase 4 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

## Objetivos

Al finalizar el módulo, el estudiante será capaz de construir y evaluar clasificadores
eligiendo la métrica adecuada al costo de cada tipo de error, manejar el desbalance de
clases, combinar modelos débiles mediante bagging y boosting, y explicar las predicciones de
un modelo de caja negra.

## Contenidos

### ✅ Núcleo

- **S9** — Regresión logística: odds, log-odds, máxima verosimilitud y softmax multiclase.
- **S9** — K-Nearest Neighbors. Máquinas de vectores de soporte (SVM) y kernels.
- **S9** — Métricas: matriz de confusión, accuracy, precisión, recall, F1, ROC-AUC y curva
  precisión-recall. Ajuste del umbral de decisión.
- **S9** — Clases desbalanceadas: remuestreo, pesos de clase y elección de métrica.
- **S10** — Árboles de decisión: impureza (Gini, entropía), profundidad, poda, sobreajuste.
- **S10** — Bagging y **Random Forest**. Importancia de variables.
- **S11** — AdaBoost, Gradient Boosting, **XGBoost** y **LightGBM**. Stacking.
- **S11** — Interpretabilidad: permutation importance y **SHAP**.

### 🔵 Opcional

- Naive Bayes y su relación con el teorema de Bayes visto en S3.
- Calibración de probabilidades (Platt, isotónica).
- Análisis de errores por segmento y sesgos del modelo.

## Materiales

### Teoría

| # | Documento | Sesión | Tema | Estado |
|---|---|---|---|---|
| 01 | `teoria/01-regresion-logistica.md` | S9 | Odds, log-odds, verosimilitud, softmax | ⬜ |
| 02 | `teoria/02-knn-y-svm.md` | S9 | KNN, distancias, SVM, margen y kernels | ⬜ |
| 03 | `teoria/03-metricas-clasificacion.md` | S9 | Matriz de confusión, ROC-AUC, PR, umbral, desbalance | ⬜ |
| 04 | `teoria/04-arboles-y-bagging.md` | S10 | Impureza, poda, bootstrap aggregating, Random Forest | ⬜ |
| 05 | `teoria/05-boosting.md` | S11 | AdaBoost, Gradient Boosting, XGBoost/LightGBM, stacking | ⬜ |
| 06 | `teoria/06-interpretabilidad.md` | S11 | Permutation importance, valores de Shapley, SHAP | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-logistica-intuicion.ipynb` | intuición | De la recta a la sigmoide; odds y verosimilitud paso a paso | ⬜ |
| 02 | `notebooks/02-clasificacion-aplicado.ipynb` | aplicado | Logística, KNN y SVM comparados; métricas, umbral y desbalance | ⬜ |
| 03 | `notebooks/03-arboles-intuicion.ipynb` | intuición | Impureza y fronteras de decisión según la profundidad | ⬜ |
| 04 | `notebooks/04-ensambles-aplicado.ipynb` | aplicado | Random Forest, Gradient Boosting, XGBoost y LightGBM comparados | ⬜ |
| 05 | `notebooks/05-interpretabilidad-aplicado.ipynb` | aplicado | Permutation importance y SHAP sobre el mejor modelo | ⬜ |

### Datos

| Archivo | Descripción | Variables | Estado |
|---|---|---|---|
| — | Dataset conductor del módulo, pendiente de elegir (candidato heredado: Wine Quality, UCI) | — | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-metricas-umbral.md` | `ej01-metricas-umbral-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-ensambles.md` | `ej02-ensambles-sol.md` | ⬜ |
| 03 | `ejercicios/ej03-interpretabilidad.md` | `ej03-interpretabilidad-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-4.md` | `quiz/quiz-modulo-4-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E4 — Modelos avanzados.** Ensambles ajustados sobre el caso, comparados contra la línea
base de E3, con interpretación de las variables que más pesan. Ver
[`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../environment.yml`](../environment.yml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

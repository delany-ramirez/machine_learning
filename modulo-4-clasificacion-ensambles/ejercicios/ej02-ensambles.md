# Ejercicio 02 · Bosques y boosting sobre Adult Census

**Módulo 4 · Sesiones 10–11** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Repetir sobre Adult Census la comparación que los notebooks 04 y 06 hicieron
> sobre Wine Quality —y descubrir que la conclusión **cambia**. Con 39 000 filas de
> entrenamiento y categóricas de alta cardinalidad, el orden entre bosques y boosting no es
> el mismo que con 4 000 vinos. Medirlo con la comparación pareada, elegir el número de
> rondas con early stopping, y cerrar con el conjunto de prueba.

## Contexto

Misma partición, mismo `crear_pipeline()` y mismo `StratifiedKFold` del ejercicio 01. La
métrica principal es la **AP**; los costos son los de C.3 del ejercicio 01 (FN = 5 × FP).

```python
from lightgbm import LGBMClassifier, early_stopping
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
```

Los árboles no necesitan escalado: usa `crear_pipeline(..., escalar=False)`.

Entrega un notebook `ej02-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — Cuatro ensambles con valores por defecto (15 min)

**A.1** Evalúa con la CV de 5 pliegues: Random Forest (300 árboles), Extra-Trees (300
árboles), LightGBM con valores por defecto, y LightGBM con `n_estimators=1000,
learning_rate=0.03`. Reporta AP, AUC-ROC y tiempo de ajuste por pliegue.

**A.2** Compara con la tabla de la sección 2 de `06-boosting-aplicado.ipynb`. ¿Qué cambió
de orden respecto a Wine Quality? Propón una explicación a partir de lo que dice
`05-boosting.md` sobre cuándo boosting tiende a ganar.

## Parte B — Random Forest: hojas mínimas (10 min)

**B.1** En Wine Quality, `min_samples_leaf=1` era la mejor opción para Random Forest
(`04-arboles-bagging-aplicado.ipynb`, sección 4). Prueba aquí `min_samples_leaf` en
$\{1, 5, 20\}$ y reporta AP y AUC-ROC.

**B.2** ¿Se sostiene la conclusión de Wine Quality? Si no, ¿qué tiene este dataset que
haga que los árboles completamente desarrollados funcionen peor?

## Parte C — LightGBM: categóricas nativas y early stopping (25 min)

**C.1** LightGBM acepta variables categóricas sin *one-hot*: convierte las columnas de texto
a `dtype="category"` en entrenamiento **y** prueba (con las mismas categorías) y entrena
`LGBMClassifier(n_estimators=1000, learning_rate=0.03)` directamente sobre el `DataFrame`,
sin `ColumnTransformer`. Compara AP y tiempo con la versión *one-hot* de A.1.

**C.2** Sobre el primer pliegue de la CV, entrena LightGBM con `n_estimators=5000`,
`learning_rate=0.03`, `eval_set` sobre el pliegue de validación, `eval_metric="average_precision"`
y `callbacks=[early_stopping(200)]`. Grafica la AP de validación por ronda y reporta
`best_iteration_`.

**C.3** Comparación pareada de LightGBM (con el número de rondas de C.2) contra Random Forest
(con el mejor `min_samples_leaf` de B.1) sobre los mismos pliegues de
`RepeatedStratifiedKFold(n_splits=5, n_repeats=2, random_state=42)`. Reporta la diferencia
media, su error estándar y el cociente.

## Parte D — Conjunto de prueba (15 min)

**D.1** Con el mejor modelo de C.3, elige el umbral de mínimo costo (FN = 5 × FP) con
probabilidades de `cross_val_predict`, ajusta sobre todo el entrenamiento y reporta sobre el
conjunto de prueba: AUC-ROC, AP, precisión, recall, F1 y costo.

**D.2** Compara con la regresión logística del ejercicio 01 sobre el mismo conjunto de
prueba (con su propio umbral óptimo). ¿La mejora es relevante en términos de costo?

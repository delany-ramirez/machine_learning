# Ejercicio 01 · Ajuste, métricas y diagnóstico de residuales

**Módulo 3 · Sesión 6** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Repetir, con tus propias manos y sobre un subconjunto de variables distinto al
> de los notebooks, el ciclo completo de `01-regresion-lineal.md`: ajustar, medir con las
> cinco métricas, y verificar los supuestos del modelo mirando los residuales — no solo el
> $R^2$.

## Contexto

Vas a usar `../datos/ames-housing.csv`, pero con un conjunto de variables **distinto** al de
`02-regresion-multiple-aplicado.ipynb`: en vez del tamaño y la calidad general, esta vez el
foco está en la distribución de espacio entre pisos y la cimentación de la vivienda.

```python
import numpy as np
import pandas as pd

datos = pd.read_csv("../datos/ames-housing.csv")

numericas = [
    "lot_frontage", "lot_area", "year_built", "total_bsmt_sf",
    "1st_flr_sf", "2nd_flr_sf", "full_bath", "half_bath",
    "fireplaces", "wood_deck_sf", "open_porch_sf",
]
categoricas = ["foundation"]
objetivo = "saleprice"
```

> **Ojo.** `lot_frontage` tiene un 16.7 % de valores nulos. Tu `Pipeline` necesita
> imputación, no solo escalado — igual que en `02-regresion-multiple-aplicado.ipynb`.

Entrega un notebook `ej01-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — Ajuste y métricas (25 min)

**A.1** Parte los datos 80/20 con `random_state=42`. Calcula el RMSE de la línea base
(predecir siempre el precio promedio de entrenamiento).

**A.2** Construye un `Pipeline` con `ColumnTransformer` (imputación + escalado para las
numéricas, codificación para `foundation`) y una `LinearRegression`. Ajusta y calcula, sobre
el conjunto de prueba: MSE, RMSE, MAE, $R^2$ y $R^2$ ajustado. Compara el RMSE contra la línea
base.

**A.3** ¿Cuántas columnas tiene la matriz de diseño después de codificar? ¿El $R^2$ ajustado
se aleja mucho del $R^2$ ordinario? Relaciónalo con la fórmula de `01-regresion-lineal.md` y
con $n$ y $p$ de este problema.

## Parte B — Diagnóstico de residuales (25 min)

**B.1** Grafica los residuales contra los valores ajustados, y el histograma de los
residuales.

**B.2** De los cinco supuestos de `01-regresion-lineal.md`, ¿cuál se ve claramente violado en
tu gráfico? Descríbelo con tus palabras: ¿en qué rango de precios el modelo se equivoca más?

**B.3** Calcula la correlación entre $|\text{residual}|$ y el valor ajustado. ¿Qué tan fuerte
es, comparada con lo que viste en `02-regresion-multiple-aplicado.ipynb`?

## Parte C — ¿Ayuda modelar en log(precio)? (15 min)

**C.1** Reentrena el mismo `Pipeline` prediciendo $\log(1+\text{precio})$, revierte las
predicciones con $\exp(\cdot)-1$, y recalcula RMSE, MAE y MAPE en dólares.

**C.2** Compara contra el modelo directo de la parte A. ¿El resultado va en la misma
dirección que `02-regresion-multiple-aplicado.ipynb`, o es distinto? Sea cual sea tu
resultado, repórtalo tal cual — no ajustes la conclusión para que "coincida" con el notebook.

## Parte D — Interpretación con cautela (10 min)

**D.1** Lista los tres coeficientes de mayor magnitud (en valor absoluto) del modelo de la
parte A. ¿Su signo tiene sentido de negocio?

**D.2** Dos variables del conjunto miden aspectos de "cuántos baños tiene la casa". Revisa sus
coeficientes. Si alguno tiene un signo que no esperarías, no lo "corrijas" — anótalo como
candidato a revisar con VIF. Ese hallazgo se retoma en el ejercicio 02.

## Entrega

Notebook con el código, las gráficas, y una respuesta corta (2-3 líneas) a cada pregunta con
letra y número (B.2, C.2, D.1, D.2 son las que más pesan).

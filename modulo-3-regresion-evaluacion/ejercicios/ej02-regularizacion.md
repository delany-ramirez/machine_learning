# Ejercicio 02 · VIF, y Ridge/Lasso/Elastic Net sobre tu propio hallazgo

**Módulo 3 · Sesión 7** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Calcular VIF sobre el conjunto de variables del ejercicio 01, y usar
> Ridge, Lasso y **Elastic Net** para ver si la regularización resuelve el signo
> contraintuitivo que detectaste en `ej01-residuales.md` (D.2) — y si de paso mejora la
> predicción, o no.

## Contexto

Mismas variables de `ej01-residuales.md`:

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

Entrega un notebook `ej02-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — VIF (15 min)

**A.1** Imputa los nulos de las numéricas con la mediana **del entrenamiento** (nunca con
datos de prueba), estandariza, y calcula el VIF de cada una con
`statsmodels.stats.outliers_influence.variance_inflation_factor` — igual que en
`04-regularizacion-aplicado.ipynb`.

**A.2** ¿Alguna variable supera el umbral convencional de 5 (`03-multicolinealidad-polinomica.md`)?
Si tu respuesta es "ninguna", no te detengas ahí: en el ejercicio 01 encontraste coeficientes
con signo contraintuitivo (`full_bath`, `half_bath`) **sin necesidad de un VIF alto**. Explica
en tus palabras por qué el umbral de VIF > 5 no es una garantía de que todos los coeficientes
individuales sean interpretables con confianza.

## Parte B — Ridge y Lasso (25 min)

**B.1** Aparta una porción de validación **del entrenamiento** (nunca del test), igual que en
`04-regularizacion-aplicado.ipynb`. Barre $\lambda$ en una rejilla logarítmica (por ejemplo,
`np.logspace(-2, 3, 15)`) para Ridge y Lasso, y grafica el RMSE de validación de cada uno.

**B.2** Elige, para cada método, un $\lambda$ razonable con base en tu curva (no tiene que ser
el mínimo exacto — justifica tu elección en un par de líneas).

**B.3** Grafica (o tabula) cómo cambian los coeficientes de `full_bath` y `half_bath` con
$\lambda$, para Ridge. ¿En algún punto de la trayectoria el signo se vuelve el esperado?
¿Qué $\lambda$ hace falta para eso, comparado con el $\lambda$ que elegiste en B.2 por RMSE?

## Parte C — Elastic Net (20 min)

**C.1** `04-regularizacion-aplicado.ipynb` advirtió que la escala de `alpha` en
`ElasticNet` de `scikit-learn` no es comparable directamente a la de `Ridge` o `Lasso` solos.
Compruébalo: evalúa `ElasticNet` con `alpha` en `[0.01, 0.1, 1, 10, 50]` y `l1_ratio` en
`[0.1, 0.5, 0.9]` (15 combinaciones) sobre tu partición de validación. ¿Qué le pasa al RMSE
con `alpha=50`, comparado con lo que viste para Ridge o Lasso en ese mismo orden de magnitud?

**C.2** Elige la mejor combinación de tu barrido.

## Parte D — Comparación final (15 min)

**D.1** Entrena OLS, Ridge (con el $\lambda$ de B.2), Lasso (con el $\lambda$ de B.2) y
Elastic Net (con la combinación de C.2) sobre **todo** el entrenamiento, y evalúa los cuatro
en el conjunto de prueba (RMSE).

**D.2** ¿Algún modelo le gana claramente a OLS en predicción? Conecta tu respuesta con
`03-multicolinealidad-polinomica.md`, sección 2: ¿tiene sentido que la ganancia (si la hay)
sea chica, dado lo que encontraste sobre el VIF en la parte A?

## Entrega

Notebook con código, gráficas de las tres trayectorias (B.1, B.3) y respuestas cortas a A.2,
B.3, C.1 y D.2.

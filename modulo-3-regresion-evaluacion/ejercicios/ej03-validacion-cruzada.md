# Ejercicio 03 · CV, grid vs. random, CV anidada y ¿ayuda `foundation`?

**Módulo 3 · Sesión 8** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Cerrar el módulo aplicando, sobre las variables de los ejercicios 01 y 02, las
> herramientas de `05-sesgo-varianza-validacion.md` y `06-seleccion-hiperparametros.md`:
> reemplazar el split de validación informal del ejercicio 02 por validación cruzada de
> verdad, medir el optimismo de no anidar la búsqueda, y decidir con evidencia —no con un solo
> número— si `foundation` realmente ayuda a predecir o es una variable de relleno.

## Contexto

Mismas variables de los ejercicios 01 y 02.

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

Entrega un notebook `ej03-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — Elegir $\lambda$ con `GridSearchCV` (15 min)

**A.1** Usa `KFold(n_splits=5, shuffle=True, random_state=42)` y `GridSearchCV` para elegir el
$\lambda$ de Ridge sobre la misma rejilla logarítmica del ejercicio 02. Repite para Lasso.

**A.2** Compara el $\lambda$ elegido por CV contra el que elegiste "a ojo" en `ej02-regularizacion.md`
(parte B.2). ¿Coinciden aproximadamente? ¿El RMSE de validación cruzada es más alto o más bajo
que el que habías visto con el split único, y por qué tendría que ser distinto?

## Parte B — Grid vs. random (15 min)

**B.1** Sobre el mismo Ridge, compara una rejilla de 40 valores de $\lambda$
(`GridSearchCV`) contra 15 valores muestreados de una `scipy.stats.loguniform`
(`RandomizedSearchCV`, con `random_state=42`). Reporta RMSE de CV y tiempo de cada uno.

**B.2** ¿Se sostiene, en este caso, la afirmación de `06-seleccion-hiperparametros.md` de que
random search encuentra un resultado comparable con menos evaluaciones?

## Parte C — Validación cruzada anidada (20 min)

**C.1** Implementa CV anidada para Ridge: un bucle externo de 5 pliegues, y dentro de cada uno
un `GridSearchCV` con su propio `KFold` interno de 5 pliegues (igual que
`06-seleccion-modelos-aplicado.ipynb`). Reporta el RMSE promedio del bucle externo, con su
error estándar.

**C.2** Compara ese número contra el RMSE "ingenuo" de la parte A (el mismo CV que elige y
reporta). ¿Cuánto optimismo mide tu experimento? ¿Es grande o chico frente al error estándar
de la CV anidada?

## Parte D — ¿`foundation` ayuda de verdad? (25 min)

**D.1** Construye dos pipelines de Ridge (con el $\lambda$ de la parte A): uno con las 11
variables numéricas **y** `foundation`, y otro **solo** con las 11 numéricas.

**D.2** Compara ambos con validación cruzada de **10 pliegues, usando los mismos pliegues
para los dos modelos** (comparación pareada, `05-sesgo-varianza-validacion.md` sección 3).
Calcula la diferencia media de RMSE por pliegue y su error estándar.

**D.3** ¿La diferencia es mayor o menor que dos errores estándar? A diferencia de la
comparación Ridge-vs-Lasso de `06-seleccion-modelos-aplicado.ipynb` (sesión 8), donde no se
encontró diferencia detectable, aquí puede que sí la haya — o puede que no. Reporta lo que tu
experimento realmente diga, y concluye si vale la pena mantener `foundation` en el modelo.

## Entrega

Notebook con código y respuestas cortas a A.2, B.2, C.2 y D.3 — la D.3 es la que más pesa: es
la conclusión de todo el módulo.

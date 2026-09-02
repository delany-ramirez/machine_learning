# Ejercicio 02 · Álgebra lineal y gradientes con NumPy

**Módulo 1 · Sesión 3** · Tiempo estimado: **90 min** · Con código

> **Objetivo.** Manipular datos como vectores y matrices; comprobar en la práctica el efecto
> de la escala sobre distancias y similitudes; calcular componentes principales a mano; e
> implementar el descenso del gradiente para una regresión de dos variables.

## Preparación

Trabaja sobre `../datos/rendimiento-estudiantes.csv`. Empieza así:

```python
import numpy as np
import pandas as pd

SEMILLA = 42
datos = pd.read_csv("../datos/rendimiento-estudiantes.csv")
variables = ["promedio_anterior", "horas_estudio_semana", "asistencia_pct"]
X = datos[variables].to_numpy()
y = datos["nota_final"].to_numpy()
```

Entrega un notebook llamado `ej02-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — Producto punto y similitud (20 min)

**A.1** Usando los coeficientes $\beta_0 = -0.15$ y
$\boldsymbol{\beta} = (0.62,\ 0.055,\ 0.011)$, calcula las predicciones para **los 400
estudiantes de una sola vez**, sin bucles, con un producto matricial. Reporta las primeras
cinco predicciones y el MAE frente a `nota_final`.

**A.2** Escribe una función `similitud_coseno(u, v)`. Calcula la similitud entre los
estudiantes `E0001` y `E0002` usando las tres variables:

1. Con los datos **crudos**.
2. Con los datos **estandarizados** ($z = (x-\mu)/\sigma$, usando la media y la desviación de
   las 400 observaciones).

Los dos resultados son muy distintos. **Explica por qué**, mirando los valores concretos de
ambos estudiantes.

## Parte B — Distancias y escalado (25 min)

**B.1** Escribe código que, dado el índice de un estudiante, devuelva sus **3 vecinos más
cercanos** por distancia euclidiana (excluyéndolo a él mismo).

**B.2** Aplícalo al estudiante `E0001`, dos veces: con los datos crudos y con los datos
estandarizados. ¿Son los mismos tres vecinos?

**B.3** Predice la nota de `E0001` como el **promedio de la nota de sus 3 vecinos** en cada
caso. Compara con su nota real. (Acabas de implementar KNN a mano; lo formalizaremos en la
sesión 9.)

**B.4** Explica, mirando la desviación estándar de cada variable, **cuál domina la distancia**
cuando no se estandariza y por qué.

## Parte C — Componentes principales a mano (25 min)

**C.1** Estandariza `X` y calcula su matriz de covarianza **sin usar `np.cov`**:

$$
\mathbf{\Sigma} = \frac{1}{n-1}\,\mathbf{X}_c^{\top}\mathbf{X}_c
$$

Verifica que coincide con `np.cov(Xz, rowvar=False)`.

**C.2** Obtén valores y vectores propios con `np.linalg.eigh`, ordénalos de mayor a menor
valor propio, y construye una tabla con la varianza explicada y la acumulada por componente.

**C.3** Comprueba numéricamente que dos vectores propios cualesquiera son **ortogonales**
(producto punto igual a cero). ¿Qué propiedad de la matriz de covarianza lo garantiza?

**C.4** Mira el porcentaje de varianza que explica la primera componente. ¿Dirías que en este
dataset la reducción de dimensionalidad aporta algo? Justifica con la matriz de correlación.

## Parte D — Descenso del gradiente (20 min)

Ajusta `nota_final` en función de `promedio_anterior` y `horas_estudio_semana`, usando
**solo NumPy**.

**D.1** Estandariza las dos variables predictoras. Implementa el descenso del gradiente para

$$
\mathcal{L}(\beta_0, \boldsymbol{\beta}) = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - (\beta_0 + \boldsymbol{\beta}\cdot\mathbf{x}_i)\right)^2
$$

con las derivadas parciales

$$
\frac{\partial \mathcal{L}}{\partial \beta_0} = -\frac{2}{n}\sum_i r_i
\qquad
\frac{\partial \mathcal{L}}{\partial \beta_j} = -\frac{2}{n}\sum_i r_i x_{ij}
\qquad\text{con } r_i = y_i - \hat{y}_i
$$

Usa 500 pasos y guarda el historial de la pérdida.

**D.2** Prueba con $\eta \in \{0.001,\ 0.01,\ 0.1,\ 0.5\}$. Reporta la pérdida final de cada
una y explica qué ocurre con la más pequeña.

**D.3** Compara los coeficientes obtenidos con la **solución exacta** por ecuación normal:

```python
A = np.c_[np.ones(len(Xz)), Xz]
beta_exacto = np.linalg.solve(A.T @ A, A.T @ y)
```

**D.4** Repite el entrenamiento con $\eta = 0.1$ **sin estandarizar** las variables. ¿Qué
ocurre? Relaciónalo con lo que observaste en la Parte B.

**D.5** Grafica la curva de aprendizaje (pérdida vs. paso) en escala logarítmica para las
tasas que sí convergen.

---

> **Entrega.** El notebook ejecutado, con las respuestas escritas en celdas Markdown. Se
> valora tanto el código correcto como la **explicación** de lo observado: las partes A.2,
> B.4, C.4 y D.4 se evalúan por el razonamiento, no por el número.

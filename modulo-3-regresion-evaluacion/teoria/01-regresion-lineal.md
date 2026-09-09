# 01 · Regresión lineal: formulación, ajuste y diagnóstico

**Módulo 3 · Sesión 6** — Regresión lineal

## Objetivos

- Formular la regresión lineal simple y múltiple en notación matricial.
- Derivar la solución de mínimos cuadrados ordinarios (OLS) y entender qué está optimizando.
- Verificar los supuestos del modelo lineal mediante el análisis de residuales.
- Elegir e interpretar correctamente las métricas de error: MSE, RMSE, MAE, $R^2$ y $R^2$
  ajustado.

## 1. De la regresión simple a la múltiple

En la regresión simple, una sola variable $x$ predice $y$ mediante una recta:

$$
\hat{y} = \beta_0 + \beta_1 x
$$

En la práctica casi ningún fenómeno depende de una sola variable. La regresión **múltiple**
generaliza el modelo a $p$ predictores:

$$
\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_p x_p
$$

Escrito con la matriz de diseño $\mathbf{X} \in \mathbb{R}^{n \times (p+1)}$ (con una columna
de unos para el intercepto) y el vector de parámetros $\boldsymbol{\beta} \in
\mathbb{R}^{p+1}$:

$$
\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\beta}
$$

Esta es la misma notación de `03-algebra-lineal-intuicion.ipynb` (módulo 1): un producto
matriz-vector. Cada fila de $\mathbf{X}$ es una observación; cada columna, una variable.

## 2. Mínimos cuadrados ordinarios (OLS)

"Ajustar" el modelo significa elegir $\boldsymbol{\beta}$ que minimice el error cuadrático
total. La función de costo de OLS es:

$$
\mathcal{L}(\boldsymbol{\beta}) = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \lVert \mathbf{y} -
\mathbf{X}\boldsymbol{\beta} \rVert_2^2
$$

Es una función cuadrática y convexa en $\boldsymbol{\beta}$: tiene un único mínimo global, sin
óptimos locales que confundan la búsqueda. Igualando el gradiente a cero se obtiene la
**ecuación normal**, con solución cerrada:

$$
\boldsymbol{\beta} = (\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y}
$$

Dos observaciones importantes, que reaparecen en las sesiones 6 y 7:

- La ecuación normal requiere invertir $\mathbf{X}^{\top}\mathbf{X}$, una matriz $(p+1)\times
  (p+1)$. Si $p$ es grande, invertir es costoso ($O(p^3)$); el descenso del gradiente
  (`02-descenso-gradiente.md`) evita esa inversión.
- Si las columnas de $\mathbf{X}$ están muy correlacionadas entre sí (multicolinealidad,
  sesión 7), $\mathbf{X}^{\top}\mathbf{X}$ se vuelve casi singular y la inversión se
  desestabiliza: pequeños cambios en los datos producen coeficientes muy distintos.

### ¿Por qué el cuadrado y no el valor absoluto?

Porque produce una solución cerrada, diferenciable en todas partes, y penaliza los errores
grandes más que proporcionalmente. Ese último punto es una elección de diseño, no una ley
física: si los outliers no deben pesar tanto, se usa una pérdida más robusta (regresión
robusta, sección opcional del módulo).

## 3. Los cinco supuestos del modelo lineal

OLS produce coeficientes válidos *bajo ciertos supuestos*. Verificarlos no es un trámite: si
fallan, los coeficientes pueden seguir siendo el mejor ajuste lineal posible, pero los
intervalos de confianza y las pruebas de hipótesis dejan de ser confiables.

| # | Supuesto | Qué significa | Cómo se verifica |
|---|---|---|---|
| 1 | Linealidad | La relación real entre $\mathbf{X}$ e $y$ es (aproximadamente) lineal en los parámetros | Gráfico de residuales vs. valores ajustados: no debe haber patrón curvo |
| 2 | Independencia | Los errores $\varepsilon_i$ no están correlacionados entre sí | Gráfico de residuales en el orden de recolección; en series de tiempo, Durbin-Watson |
| 3 | Homocedasticidad | La varianza del error es constante para todos los niveles de $\hat{y}$ | Residuales vs. ajustados: la dispersión no debe ensancharse ("forma de embudo") |
| 4 | Normalidad de residuales | $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$ | Histograma o gráfico Q-Q de los residuales |
| 5 | Sin multicolinealidad severa | Los predictores no son combinaciones casi lineales entre sí | VIF (sesión 7) |

El supuesto que más se ignora en la práctica es la homocedasticidad, y es también el más fácil
de ver: si el gráfico de residuales contra valores ajustados tiene forma de embudo (el error
crece con el precio, por ejemplo), significa que el modelo es peor prediciendo los valores
altos que los bajos — algo que el $R^2$ global no revela.

### Residuales: la principal herramienta de diagnóstico

El residual de la observación $i$ es $e_i = y_i - \hat{y}_i$. Un buen ajuste produce
residuales que se ven como ruido puro, sin estructura, cuando se grafican contra los valores
ajustados o contra cada predictor. Si aparece un patrón (una curva, un embudo, una tendencia),
el patrón es información que el modelo no capturó.

## 4. Métricas de error

Todas se calculan sobre los residuales, pero comunican cosas distintas.

**Error cuadrático medio (MSE):**

$$
\text{MSE} = \frac{1}{n}\sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

Es la misma cantidad que minimiza OLS (salvo la constante $n$). Penaliza fuerte los errores
grandes, pero sus unidades son las de $y$ al cuadrado — difícil de interpretar directamente.

**Raíz del error cuadrático medio (RMSE):** $\text{RMSE} = \sqrt{\text{MSE}}$. Recupera las
unidades originales de $y$: "en promedio, el modelo se equivoca por RMSE unidades", con más
peso a los errores grandes que el MAE.

**Error absoluto medio (MAE):**

$$
\text{MAE} = \frac{1}{n}\sum_{i=1}^{n} |y_i - \hat{y}_i|
$$

También está en las unidades de $y$, pero trata todos los errores proporcionalmente a su
tamaño, sin el peso extra a los grandes que tiene el RMSE. Si $\text{RMSE} \gg \text{MAE}$,
hay algunos errores grandes (outliers de predicción) que están dominando el RMSE.

**Coeficiente de determinación ($R^2$):**

$$
R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2} = 1 -
\frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}
$$

Compara el modelo contra la referencia trivial de predecir siempre $\bar{y}$ (la misma
referencia trivial del notebook `01-primer-modelo-aplicado.ipynb` del módulo 1). $R^2=1$ es
ajuste perfecto; $R^2=0$ significa que el modelo no mejora sobre predecir el promedio;
$R^2<0$ es posible en test y significa que el modelo es **peor** que esa referencia trivial.

**$R^2$ ajustado.** El $R^2$ ordinario nunca puede bajar al agregar variables, aunque sean
ruido puro — mecánicamente, más columnas en $\mathbf{X}$ nunca aumentan $\text{SS}_{\text{res}}$.
Eso lo hace inútil para comparar modelos con distinto número de predictores. El $R^2$ ajustado
penaliza por cada variable agregada:

$$
R^2_{\text{ajustado}} = 1 - (1 - R^2)\frac{n - 1}{n - p - 1}
$$

Si una variable nueva no aporta señal real, el $R^2$ ajustado baja aunque el $R^2$ ordinario
suba (ligerísimamente). Es la primera defensa, muy barata, contra el sobreajuste por exceso de
variables — el tema completo de la sesión 8.

## Resumen

| Concepto | Para qué sirve | Dónde reaparece |
|---|---|---|
| Ecuación normal | Solución exacta de OLS | Comparación contra el descenso del gradiente (sesión 6, notebook 01) |
| Residuales | Diagnóstico visual de los 5 supuestos | Regularización (sesión 7), sesgo-varianza (sesión 8) |
| $R^2$ ajustado | Penaliza variables sin señal | Selección de modelos (sesión 8) |
| Multicolinealidad (supuesto 5) | Inestabilidad de $\boldsymbol{\beta}$ | VIF y regularización (sesión 7) |

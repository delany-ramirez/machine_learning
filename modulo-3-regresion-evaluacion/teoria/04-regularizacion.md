# 04 · Regularización: Ridge, Lasso y Elastic Net

**Módulo 3 · Sesión 7** — Regresión avanzada

## Objetivos

- Entender la regularización como una penalización al tamaño de $\boldsymbol{\beta}$ que
  estabiliza la solución frente a la multicolinealidad de `03-multicolinealidad-polinomica.md`.
- Derivar Ridge ($L_2$) y su solución cerrada; entender por qué Lasso ($L_1$) no tiene una y
  produce coeficientes exactamente cero.
- Interpretar geométricamente por qué Lasso selecciona variables y Ridge no.
- Saber cuándo usar Elastic Net.

## 1. La idea: penalizar el tamaño de $\boldsymbol{\beta}$

OLS minimiza solo el error de ajuste:

$$
\mathcal{L}_{\text{OLS}}(\boldsymbol{\beta}) = \lVert \mathbf{y} - \mathbf{X}\boldsymbol{\beta}
\rVert_2^2
$$

Cuando hay multicolinealidad, esa minimización puede lograrse con coeficientes enormes y de
signos opuestos que se cancelan entre sí (uno compensando al otro), porque el problema está
casi indeterminado. La regularización agrega un segundo término que penaliza justamente eso:
coeficientes grandes.

$$
\mathcal{L}_{\text{regularizado}}(\boldsymbol{\beta}) = \underbrace{\lVert \mathbf{y} -
\mathbf{X}\boldsymbol{\beta} \rVert_2^2}_{\text{ajuste}} + \underbrace{\lambda \, R
(\boldsymbol{\beta})}_{\text{penalización}}
$$

$\lambda \geq 0$ controla el compromiso: $\lambda=0$ recupera OLS exactamente; $\lambda \to
\infty$ fuerza todos los coeficientes hacia cero (el modelo se acerca a predecir siempre
$\bar{y}$). Lo que cambia entre Ridge, Lasso y Elastic Net es la forma de $R(\boldsymbol{\beta})$.

**El intercepto no se regulariza.** No representa el efecto de ninguna variable, así que
penalizarlo no tiene el mismo sentido — y en la práctica desplazaría todas las predicciones.

## 2. Ridge ($L_2$)

$$
R(\boldsymbol{\beta}) = \sum_{j=1}^p \beta_j^2 = \lVert \boldsymbol{\beta} \rVert_2^2
$$

Igual que OLS, Ridge **tiene solución cerrada** —y a diferencia de Lasso (sección 3), que no la
tiene—. Es la razón por la que se usa como primer remedio a la multicolinealidad:

$$
\boldsymbol{\beta}_{\text{Ridge}} = (\mathbf{X}^{\top}\mathbf{X} + \lambda \mathbf{I})^{-1}
\mathbf{X}^{\top}\mathbf{y}
$$

Sumar $\lambda \mathbf{I}$ (con $\lambda > 0$) a $\mathbf{X}^{\top}\mathbf{X}$ antes de
invertir es precisamente lo que evita la casi-singularidad de `03-multicolinealidad-polinomica.md`:
la matriz siempre es invertible, sin importar cuán correlacionadas estén las columnas de
$\mathbf{X}$. El efecto sobre los coeficientes es *shrinkage* (encogimiento): todos se acercan
a cero de forma proporcional y suave, pero ninguno llega exactamente a cero salvo en el límite
$\lambda \to \infty$.

## 3. Lasso ($L_1$)

$$
R(\boldsymbol{\beta}) = \sum_{j=1}^p |\beta_j| = \lVert \boldsymbol{\beta} \rVert_1
$$

El valor absoluto no es diferenciable en $\beta_j = 0$, así que Lasso **no tiene solución
cerrada** — se resuelve con métodos iterativos (descenso por coordenadas es el más común; el
notebook 03 implementa una versión simplificada). La diferencia práctica con Ridge es
notable: Lasso produce coeficientes **exactamente iguales a cero** para las variables menos
relevantes. Es, de facto, un método de selección de variables incorporado al ajuste.

### Por qué Lasso selecciona variables y Ridge no: la geometría

Ambos problemas se pueden reescribir como "minimizar el error de ajuste sujeto a que
$R(\boldsymbol{\beta})$ no exceda un presupuesto $t$" (una forma equivalente a la penalización,
para un $\lambda$ y $t$ que se corresponden). La región permitida es:

- **Ridge**: una bola (círculo en 2D, esfera en más dimensiones) — $\beta_1^2 + \beta_2^2 \leq
  t$.
- **Lasso**: un rombo (diamante en 2D) — $|\beta_1| + |\beta_2| \leq t$.

El óptimo del problema es el punto de esa región donde las curvas de nivel de
$\mathcal{L}_{\text{OLS}}$ (elipses centradas en $\hat{\boldsymbol{\beta}}_{\text{OLS}}$) tocan
por primera vez la frontera de la región permitida. Un círculo no tiene esquinas: el punto de
tangencia casi nunca cae exactamente sobre un eje, así que ningún $\beta_j$ es forzado a cero.
Un diamante sí tiene esquinas —sobre los ejes, donde alguna coordenada vale cero— y esas
esquinas son puntos donde es geométricamente mucho más probable que las elipses de nivel
"encajen" primero. Esa es, literalmente, la razón geométrica de la dispersión (*sparsity*) de
Lasso.

## 4. Elastic Net

$$
R(\boldsymbol{\beta}) = \alpha \lVert \boldsymbol{\beta} \rVert_1 + (1-\alpha) \lVert
\boldsymbol{\beta} \rVert_2^2, \qquad \alpha \in [0, 1]
$$

Combina ambas penalizaciones. $\alpha=1$ es Lasso puro; $\alpha=0$ es Ridge puro.

> **Cuidado con los nombres en `scikit-learn`.** Al $\alpha$ de esta fórmula lo llama
> `l1_ratio`; su parámetro `alpha` es el $\lambda$ de este documento. Además, `ElasticNet`
> reparte un mismo `alpha` entre las dos penalizaciones, así que un valor que resulta suave
> para `Ridge` o `Lasso` por separado puede ser mucho más agresivo para `ElasticNet`: las
> rejillas de búsqueda **no** son intercambiables entre los tres métodos.

La razón para usarlo, más allá de "un punto intermedio": cuando hay un **grupo** de variables
muy correlacionadas entre sí y todas relevantes, Lasso tiende a elegir una del grupo de forma
casi arbitraria y poner las demás en cero — inestable de una muestra a otra. Elastic Net,
gracias al componente Ridge, tiende a mantener el grupo completo con coeficientes similares,
en vez de una elección arbitraria.

## 5. $\lambda$: el hiperparámetro que lo controla todo

$\lambda$ gobierna directamente el compromiso sesgo-varianza que la sesión 8 formaliza:

- $\lambda$ pequeño → el modelo se parece a OLS: bajo sesgo, alta varianza (sensible a la
  muestra de entrenamiento).
- $\lambda$ grande → coeficientes muy encogidos: alto sesgo, baja varianza (el modelo apenas
  reacciona a los datos).

No hay una fórmula para el $\lambda$ "correcto" — se elige con validación cruzada, comparando
el error en datos que el modelo no vio durante el ajuste (sesión 8). Aquí, sección de
introducción, se explora su efecto con una curva de validación simple; la búsqueda
sistemática y rigurosa llega en la siguiente sesión.

## 6. Por qué estandarizar es obligatorio, no opcional

`02-descenso-gradiente.md` ya exigía estandarizar para que el descenso convergiera rápido. Con
regularización, estandarizar deja de ser una cuestión de velocidad y se vuelve una cuestión de
**corrección**: la penalización $\lambda \sum \beta_j^2$ (o $\sum|\beta_j|$) trata a todos los
coeficientes por igual, sin saber en qué unidades está cada variable. Si `lot_area` se mide en
pies² (números en las decenas de miles) y `overall_qual` va de 1 a 10, el coeficiente de
`lot_area` va a ser minúsculo de por sí —por la escala, no por relevancia— y la penalización lo
encogerá mucho menos que a `overall_qual`, cuyo coeficiente natural es mucho más grande. El
resultado no compara relevancia real, compara escalas. Estandarizando ($z = (x-\bar{x})/s$)
antes de regularizar, todos los predictores entran a la penalización en pie de igualdad.

## Resumen

| Método | Penalización | Solución cerrada | Coeficientes en cero | Cuándo usarlo |
|---|---|---|---|---|
| Ridge | $\lambda\lVert\boldsymbol{\beta}\rVert_2^2$ | Sí | No | Multicolinealidad, sin necesidad de seleccionar variables |
| Lasso | $\lambda\lVert\boldsymbol{\beta}\rVert_1$ | No | Sí | Se sospecha que muchos predictores son irrelevantes |
| Elastic Net | Combinación de ambas | No | Sí | Grupos de variables correlacionadas, todas relevantes |

| Concepto | Dónde reaparece |
|---|---|
| $(\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I})^{-1}$ siempre invertible | Resuelve la inestabilidad numérica de `03-multicolinealidad-polinomica.md` |
| Selección de variables vía $\lambda$ | Alternativa a la selección explícita del módulo 2 (filtro/envoltura/embebidos) |
| $\lambda$ como control de sesgo-varianza | Formalizado y buscado sistemáticamente en la sesión 8 |

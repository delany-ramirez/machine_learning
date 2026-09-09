# 03 · Multicolinealidad, VIF y regresión polinómica

**Módulo 3 · Sesión 7** — Regresión avanzada

## Objetivos

- Entender qué es la multicolinealidad y por qué es el quinto supuesto de
  `01-regresion-lineal.md` que rompe primero en datos reales.
- Diagnosticarla con la matriz de correlación y, mejor, con el **factor de inflación de la
  varianza (VIF)**.
- Distinguir qué daña la multicolinealidad (interpretación) de qué no daña (predicción).
- Extender el modelo lineal a curvas mediante regresión **polinómica**, y ver por qué agrava
  la multicolinealidad casi por construcción.

## 1. Qué es la multicolinealidad

Un modelo tiene multicolinealidad cuando dos o más predictores están fuertemente
correlacionados entre sí. En Ames Housing, `gr_liv_area` (área habitable), `total_bsmt_sf`
(área de sótano) y `garage_area` miden, en el fondo, aspectos parecidos de una misma idea:
"qué tan grande es la casa". No es un error de captura de datos — es que las variables del
mundo real vienen correlacionadas.

Recordando la ecuación normal de `01-regresion-lineal.md`:

$$
\boldsymbol{\beta} = (\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y}
$$

Si dos columnas de $\mathbf{X}$ son casi combinaciones lineales una de la otra,
$\mathbf{X}^{\top}\mathbf{X}$ se acerca a una matriz singular (no invertible). La inversión
sigue siendo posible numéricamente, pero el resultado es **inestable**: pequeños cambios en
los datos —quitar o agregar unas pocas observaciones— pueden producir coeficientes muy
distintos, incluso de signo opuesto al esperado.

## 2. Qué daña la multicolinealidad, y qué no

Esta distinción es la que más se confunde en la práctica:

| | ¿Se ve afectado? | Por qué |
|---|---|---|
| **Predicciones** ($\hat{y}$) | No, o muy poco | El modelo puede repartir el "crédito" de la predicción entre las variables correlacionadas de formas distintas y aun así predecir igual de bien |
| **$R^2$ y RMSE en test** | No, o muy poco | Son función de $\hat{y}$, no de $\boldsymbol{\beta}$ directamente |
| **Coeficientes individuales** $\beta_j$ | **Sí, gravemente** | Se vuelven inestables: cambian mucho entre muestras, pueden tener signo contraintuitivo |
| **Interpretación** ("cada metro² adicional de sótano suma \$X") | **Sí** | Si $\beta_j$ no es estable, esa interpretación no es confiable |
| **Pruebas de hipótesis sobre $\beta_j$** | **Sí** | Los errores estándar de los coeficientes se inflan, y una variable realmente relevante puede aparecer como "no significativa" |

Conclusión práctica: si el objetivo del modelo es **predecir** (el caso más común en este
curso), la multicolinealidad moderada rara vez es motivo de alarma por sí sola. Si el objetivo
es **interpretar** los coeficientes —explicarle a alguien cuánto vale cada metro² adicional—,
sí lo es.

## 3. Diagnóstico: matriz de correlación y VIF

La matriz de correlación es el primer vistazo, pero tiene un punto ciego: solo detecta
relaciones **entre pares** de variables. Una variable puede no estar muy correlacionada con
ninguna otra individualmente, y aun así ser casi una combinación lineal de *varias* combinadas
(p. ej. `total_bsmt_sf` ≈ `1st_flr_sf` cuando el sótano tiene la misma huella que el primer
piso, un patrón que ninguna correlación de a pares por sí sola revela).

El **factor de inflación de la varianza (VIF)** sí lo captura. Para cada predictor $x_j$, se
ajusta una regresión de $x_j$ contra *todos los demás predictores*, se obtiene su $R_j^2$, y:

$$
\text{VIF}_j = \frac{1}{1 - R_j^2}
$$

Interpretación: si $R_j^2 = 0$ (otros predictores no explican nada de $x_j$), $\text{VIF}_j=1$
— sin colinealidad. Si $R_j^2 \to 1$ ($x_j$ es casi predecible a partir de las demás),
$\text{VIF}_j \to \infty$. El nombre viene de que $\text{VIF}_j$ es literalmente el factor por
el que se infla la varianza de $\hat{\beta}_j$ respecto al caso sin colinealidad — de ahí que
los coeficientes se vuelvan inestables.

**Reglas de dedo habituales:** $\text{VIF} > 5$ amerita revisar; $\text{VIF} > 10$ es
colinealidad severa. No son umbrales matemáticos exactos, son convenciones — el criterio real
depende de si el objetivo es interpretar o predecir (sección 2).

## 4. Qué hacer cuando el VIF es alto

En orden de qué tan invasiva es la intervención:

1. **Nada**, si el objetivo es predecir y las métricas de test son buenas. La multicolinealidad
   no es un defecto que siempre haya que corregir.
2. **Eliminar una de las variables redundantes**, si dos miden casi lo mismo (`garage_area` y
   `garage_cars` suelen estarlo). Se pierde poca información porque la otra variable ya la
   captura.
3. **Combinar variables** en una sola (p. ej. área total = `gr_liv_area` + `total_bsmt_sf`).
4. **Regularización** (`04-regularizacion.md`): Ridge estabiliza los coeficientes sin eliminar
   variables.
5. **Reducción de dimensionalidad** (PCA, módulo 5): reemplaza los predictores originales por
   componentes no correlacionados. Es la más invasiva porque sacrifica interpretabilidad
   directa. Recordar el hallazgo del módulo 1 (`ej02`, parte C.4): PCA no ayuda cuando las
   variables ya están poco correlacionadas — solo tiene sentido aplicarlo cuando, como aquí,
   *sí* hay colinealidad real que comprimir.

## 5. Regresión polinómica

El modelo lineal asume que el efecto de cada predictor es una línea recta. Cuando la relación
real es curva —el precio de una casa no sube al mismo ritmo por cada metro² adicional una vez
que ya es muy grande—, se puede seguir usando el marco de regresión lineal agregando potencias
del predictor:

$$
\hat{y} = \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3 + \dots
$$

Esto sigue siendo un modelo **lineal en los parámetros** $\boldsymbol{\beta}$ —la ecuación
normal y el descenso del gradiente de las secciones anteriores se aplican sin cambios—, aunque
ya no es lineal en $x$. Lo mismo aplica a interacciones entre predictores ($x_1 x_2$): otra
columna más para $\mathbf{X}$.

### El costo: multicolinealidad por construcción

$x$ y $x^2$ están, casi siempre, fuertemente correlacionadas en el rango típico de los datos
—elevar al cuadrado no "des-correlaciona" nada—. Agregar términos polinómicos casi garantiza
VIF altos entre esos términos, incluso si el predictor original no tenía colinealidad con
nada más. Centrar $x$ antes de elevarlo al cuadrado (restar la media) reduce esa correlación,
pero no la elimina.

Y un segundo costo, que se retoma en la sesión 8: un grado polinómico alto puede ajustar
perfectamente los datos de entrenamiento y generalizar pésimo — la versión más directa de
sobreajuste que existe en este curso. El grado del polinomio es, en sí mismo, un
hiperparámetro que hay que elegir con validación, no con la vista.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| VIF | Detecta colinealidad multivariable, no solo pares | Se calcula en el notebook 04 sobre Ames Housing |
| Predicción vs. interpretación | La multicolinealidad daña la segunda, no tanto la primera | Guía qué tan preocupante es cada caso |
| Regularización | Estabiliza $\boldsymbol{\beta}$ sin eliminar variables | `04-regularizacion.md`, siguiente documento |
| Grado del polinomio | Hiperparámetro, no una elección visual | Sesgo-varianza y validación (sesión 8) |

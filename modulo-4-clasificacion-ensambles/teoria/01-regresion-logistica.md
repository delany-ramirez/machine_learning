# 01 · Regresión logística: odds, log-odds, verosimilitud y softmax

**Módulo 4 · Sesión 9** — Clasificación

## Objetivos

- Entender por qué la regresión lineal no sirve para predecir una variable 0/1 y qué
  problema exacto resuelve la función sigmoide.
- Leer el modelo logístico como lo que es: **una regresión lineal sobre el logaritmo de los
  momios** (*log-odds*), y por tanto interpretar sus coeficientes como razones de momios.
- Derivar la función de costo desde la **máxima verosimilitud**, y ver que su gradiente
  tiene la misma forma que el de la regresión lineal del módulo 3.
- Extender el modelo a $K$ clases con **softmax**.
- Saber cuándo la máxima verosimilitud no tiene solución y qué hace `scikit-learn` al
  respecto.

## 1. El problema con la recta

Sea $y \in \{0, 1\}$. Ajustar $\hat{y} = \mathbf{x}^\top\boldsymbol{\beta}$ por mínimos
cuadrados es posible, y hasta tiene nombre (*modelo de probabilidad lineal*), pero falla en
dos frentes:

1. **No está acotada.** Para valores extremos de $\mathbf{x}$ predice "probabilidades"
   negativas o mayores que 1. En `01-logistica-intuicion.ipynb`, con un solo predictor, el
   8.7 % de los estudiantes reciben una predicción fuera de $[0, 1]$.
2. **La pérdida es la equivocada.** El MSE penaliza igual un error de 0.3 en un punto
   cercano a la frontera que en uno lejano donde el modelo ya "acertó de sobra", y arrastra
   la recta hacia los puntos bien clasificados que están lejos.

## 2. Sigmoide, momios y log-momios

La solución es modelar la **probabilidad** $p = P(y = 1 \mid \mathbf{x})$ pasando la
combinación lineal por una función que la lleve a $(0, 1)$:

$$
p = \sigma(\mathbf{x}^\top\boldsymbol{\beta}) = \frac{1}{1 + e^{-\mathbf{x}^\top\boldsymbol{\beta}}}
$$

La sigmoide $\sigma$ no es una elección arbitraria. Los **momios** (*odds*) de un evento son
$p / (1-p)$: "3 a 1" significa $p = 0.75$. Su logaritmo, el **logit**, va de $-\infty$ a
$+\infty$ — y la regresión logística es simplemente una regresión lineal sobre él:

$$
\log\frac{p}{1-p} = \beta_0 + \beta_1 x_1 + \dots + \beta_p x_p
$$

Despejar $p$ de esta ecuación da exactamente la sigmoide: $\sigma$ es la inversa del logit.
Esta lectura es la que importa para interpretar:

| Escala | Cambio al subir $x_j$ una unidad | Interpretación |
|---|---|---|
| Log-momios | $+\beta_j$ (aditivo) | Poco intuitivo |
| Momios | $\times e^{\beta_j}$ (multiplicativo) | **Razón de momios** (*odds ratio*) |
| Probabilidad | Depende de dónde se esté en la curva | No es constante: ese es el punto de la sigmoide |

En el notebook 01, subir el promedio anterior una desviación estándar multiplica los momios
de aprobar por 5.7, y trabajar los multiplica por 0.72. Una razón de momios de 1 significa
"no hay efecto"; por eso los coeficientes cercanos a cero de `edad` y `estrato` (razones
1.09 y 1.07) son coherentes con que el proceso generador no las use.

> **El efecto sobre la probabilidad no es constante.** Con $\beta_j = 1.7$, pasar de $z=0$ a
> $z=1.7$ mueve $p$ de 0.50 a 0.85; pasar de $z = 4$ a $z = 5.7$ la mueve de 0.98 a 0.997.
> Mismo coeficiente, efectos muy distintos sobre la probabilidad: es la forma de S de la
> sigmoide. Una consecuencia práctica es que los "efectos marginales" que uno querría reportar
> dependen de en qué individuo se evalúen.

### La frontera es lineal

Con umbral 0.5, el modelo predice 1 cuando $p \geq 0.5$, es decir, cuando
$\mathbf{x}^\top\boldsymbol{\beta} \geq 0$. La frontera de decisión es el hiperplano
$\mathbf{x}^\top\boldsymbol{\beta} = 0$: la regresión logística es un **clasificador
lineal**, por más que su salida sea una curva. Lo que cambia de forma suave a través de la
frontera es la probabilidad, no la forma de la frontera.

## 3. La función de costo: máxima verosimilitud

Si cada $y_i$ es una variable Bernoulli con probabilidad $p_i =
\sigma(\mathbf{x}_i^\top\boldsymbol{\beta})$, la probabilidad de observar los datos que se
observaron —la **verosimilitud**— es

$$
L(\boldsymbol{\beta}) = \prod_{i=1}^n p_i^{y_i}(1 - p_i)^{1 - y_i}
$$

Su logaritmo convierte el producto en suma (y no cambia dónde está el máximo):

$$
\ell(\boldsymbol{\beta}) = \sum_{i=1}^n \left[y_i \log p_i + (1 - y_i)\log(1 - p_i)\right]
$$

**Maximizar** $\ell$ es lo mismo que **minimizar** $-\ell/n$, que es la **entropía
cruzada** binaria (*binary cross-entropy* o *log loss*):

$$
\mathcal{L}(\boldsymbol{\beta}) = -\frac{1}{n}\sum_{i=1}^n \left[y_i \log p_i +
(1 - y_i)\log(1 - p_i)\right]
$$

Dos propiedades la hacen la elección correcta, y no el MSE:

- **Es convexa** en $\boldsymbol{\beta}$: un solo mínimo, el descenso del gradiente siempre
  lo encuentra. El MSE aplicado a la salida de la sigmoide **no** lo es — se aplana lejos del
  óptimo (el notebook 01 lo grafica) y con varias variables produce mínimos locales.
- **Castiga la confianza equivocada sin cota**: predecir $p = 0.01$ para un $y = 1$ cuesta
  $-\log 0.01 \approx 4.6$; predecir $p = 10^{-6}$ cuesta 13.8. El MSE, en cambio, nunca
  cuesta más de 1 por observación.

### El gradiente: el mismo patrón del módulo 3

Derivando con la regla de la cadena —usando que $\sigma'(z) = \sigma(z)(1 - \sigma(z))$, lo
que hace que casi todo se cancele— se llega a

$$
\nabla_{\boldsymbol{\beta}}\mathcal{L} = \frac{1}{n}\mathbf{X}^\top(\hat{\mathbf{p}} - \mathbf{y})
$$

Compárese con el gradiente del MSE en regresión lineal, $-\frac{2}{n}\mathbf{X}^\top
(\mathbf{y} - \mathbf{X}\boldsymbol{\beta})$. Es la **misma estructura** —matriz de diseño
transpuesta por el vector de residuales— con $\hat{\mathbf{y}} = \mathbf{X}\boldsymbol{\beta}$
reemplazado por $\hat{\mathbf{p}} = \sigma(\mathbf{X}\boldsymbol{\beta})$. Por eso el bucle de
descenso del gradiente del módulo 3 sirve **sin cambios**; el notebook 01 lo reutiliza y
valida el resultado contra `scikit-learn` con cuatro decimales.

A diferencia de la regresión lineal, **no hay solución cerrada**: la sigmoide dentro del
gradiente impide despejar $\boldsymbol{\beta}$. Se resuelve iterativamente — descenso del
gradiente, o métodos de segundo orden como Newton-Raphson (*IRLS*), que es lo que
`scikit-learn` usa por defecto con el solucionador `lbfgs`.

## 4. Softmax: más de dos clases

Con $K$ clases se ajusta un vector de coeficientes por clase, $\boldsymbol{\beta}_1, \dots,
\boldsymbol{\beta}_K$, y la sigmoide se generaliza a la función **softmax**:

$$
P(y = k \mid \mathbf{x}) = \frac{e^{\mathbf{x}^\top\boldsymbol{\beta}_k}}
{\sum_{j=1}^K e^{\mathbf{x}^\top\boldsymbol{\beta}_j}}
$$

Las $K$ probabilidades son positivas y suman 1 por construcción. Con $K = 2$, softmax se
reduce exactamente a la sigmoide (basta fijar $\boldsymbol{\beta}_2 = \mathbf{0}$). La
entropía cruzada multiclase es $-\frac{1}{n}\sum_i \log P(y = y_i \mid \mathbf{x}_i)$, y
su gradiente respecto a la matriz de coeficientes vuelve a ser
$\frac{1}{n}\mathbf{X}^\top(\hat{\mathbf{P}} - \mathbf{Y})$, con $\mathbf{Y}$ la matriz
*one-hot* de etiquetas.

Dos detalles prácticos:

- Los coeficientes de softmax **no son únicos**: sumar el mismo vector a todos los
  $\boldsymbol{\beta}_k$ deja las probabilidades intactas. Las implementaciones fijan una
  convención (una clase de referencia, o una penalización que elige la solución de norma
  mínima). Se comparan predicciones, no coeficientes.
- Las fronteras entre cada par de clases siguen siendo **lineales**. Softmax no hace al
  modelo más flexible; solo lo hace multiclase. La alternativa *one-vs-rest* (un clasificador
  binario por clase) da fronteras parecidas y probabilidades que no suman 1.

`LogisticRegression` de `scikit-learn` usa softmax automáticamente cuando el objetivo tiene
más de dos clases. En `02-clasificacion-aplicado.ipynb`, sobre las 7 calidades de Wine
Quality, el modelo alcanza una accuracy de 0.55 y nunca predice las calidades 8 y 9: el
88 % de sus errores están a un punto de la calidad real. Softmax trata las clases como
categorías sin orden; cuando el objetivo es **ordinal**, esa es información que el modelo
desperdicia.

## 5. Cuando la verosimilitud no tiene máximo: separación perfecta

Si existe un hiperplano que separa perfectamente las dos clases, la entropía cruzada puede
hacerse tan pequeña como se quiera **escalando** $\boldsymbol{\beta}$: con $c\boldsymbol{\beta}$
para $c \to \infty$, cada $p_i$ tiende a su etiqueta y el costo tiende a 0 sin alcanzarlo
nunca. El estimador de máxima verosimilitud **no existe**; el descenso del gradiente sigue
avanzando indefinidamente (cada vez más despacio, porque el gradiente se hace diminuto).

Esto ocurre más de lo que parece: con muchas variables y pocos datos, o con una variable que
es casi una copia del objetivo (la fuga `alive` del Titanic, módulo 2), los datos son
separables. La consecuencia práctica:

- `LogisticRegression` **regulariza por defecto** (`penalty='l2'`, `C=1.0`). La penalización
  no es solo protección contra el sobreajuste — es lo que garantiza que exista una solución
  finita. Un `C` muy grande (o `penalty=None`) sobre datos separables produce la advertencia
  "*lbfgs failed to converge*" y coeficientes enormes.
- Los coeficientes de una logística regularizada están **encogidos**. Para interpretarlos
  como razones de momios "puras" hay que ser consciente de cuánta regularización se aplicó, y
  para compararlos con un descenso del gradiente sin penalización (notebook 01) hay que usar
  `penalty=None`.
- La regularización $L_1$/$L_2$ funciona igual que en Ridge y Lasso (`04-regularizacion.md`):
  penaliza $\|\boldsymbol{\beta}\|$, exige variables **estandarizadas**, y $L_1$ produce
  coeficientes exactamente cero. Solo cambia la convención del hiperparámetro: en
  `LogisticRegression`, `C` es el **inverso** de $\lambda$ — más `C`, menos regularización.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Sigmoide = inversa del logit | Regresión lineal sobre log-momios | Última capa de cualquier red neuronal binaria (S13) |
| Razón de momios $e^{\beta_j}$ | Efecto multiplicativo sobre los momios | Interpretación de modelos lineales en el proyecto |
| Entropía cruzada = $-$log-verosimilitud | Convexa; castiga la confianza equivocada | Función de pérdida de gradient boosting para clasificación (S11) y de las redes (S13) |
| Gradiente $\mathbf{X}^\top(\hat{\mathbf{p}} - \mathbf{y})/n$ | Mismo patrón que regresión lineal | El residual $y - \hat{p}$ que boosting ajusta en cada ronda (S11) |
| Softmax | Sigmoide para $K$ clases; fronteras lineales | Capa de salida multiclase (S13) |
| Separación perfecta | La MLE no existe; regularizar es obligatorio | Por qué `C` importa en el proyecto |

**Notebooks:** `01-logistica-intuicion.ipynb` (todo lo anterior a mano, validado contra
`scikit-learn`) · `02-clasificacion-aplicado.ipynb` (la logística en `Pipeline` sobre Wine
Quality, comparada con KNN y SVM).

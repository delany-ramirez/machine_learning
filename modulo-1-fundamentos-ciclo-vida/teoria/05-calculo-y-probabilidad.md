# 05 · Cálculo y probabilidad para Machine Learning

**Módulo 1 · Sesión 3**

> **Objetivos.** Entender la derivada como pendiente y el gradiente como su generalización;
> comprender el descenso del gradiente, el algoritmo que entrena casi todos los modelos, y el
> papel crítico de la tasa de aprendizaje; conectar la regla de la cadena con la
> retropropagación; y repasar las nociones de probabilidad que sostienen la clasificación.

## Parte I — Cálculo

## 1. La derivada es una pendiente

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

Responde a una pregunta muy concreta: si me muevo un poco a la derecha, ¿cuánto sube o baja
la función? Lo que importa para el ML es el **signo**:

- $f'(x) < 0$ → la función baja hacia la derecha → conviene avanzar.
- $f'(x) > 0$ → la función sube hacia la derecha → conviene retroceder.
- $f'(x) = 0$ → punto crítico: mínimo, máximo o punto de silla.

> **La regla que gobierna todo el entrenamiento: para minimizar, muévete en dirección
> contraria a la derivada.**

## 2. Gradiente

Con varias variables, la derivada se convierte en el **gradiente**: el vector de derivadas
parciales, una por parámetro.

$$
\nabla f(\mathbf{x}) = \left[\frac{\partial f}{\partial x_1},\ \frac{\partial f}{\partial x_2},\ \ldots,\ \frac{\partial f}{\partial x_p}\right]
$$

Dos propiedades que se usan constantemente:

1. El gradiente apunta en la dirección de **máximo ascenso**. Por eso se desciende restándolo.
2. El gradiente es **perpendicular a las curvas de nivel** de la función.

## 3. Descenso del gradiente

Es el algoritmo que entrena la regresión lineal, la regresión logística y todas las redes
neuronales. Cabe en una línea:

$$
\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \eta\,\nabla \mathcal{L}(\boldsymbol{\theta})
$$

donde $\boldsymbol{\theta}$ son los parámetros del modelo, $\mathcal{L}$ la función de pérdida
y $\eta$ la **tasa de aprendizaje** (*learning rate*).

El procedimiento: partir de unos parámetros cualesquiera, calcular el gradiente de la
pérdida, dar un paso en contra, repetir hasta que deje de mejorar.

### La tasa de aprendizaje

Es el hiperparámetro más delicado del entrenamiento. Hay tres regímenes:

| $\eta$ | Comportamiento |
|---|---|
| Muy pequeña | Converge, pero puede tardar más de lo aceptable |
| Adecuada | Converge en pocos pasos |
| Grande | Oscila alrededor del mínimo; puede converger igualmente |
| Demasiado grande | **Diverge**: la pérdida crece hasta desbordarse |

Para el caso simple $f(x) = (x-c)^2$, cada paso equivale a
$(x - c) \leftarrow (1 - 2\eta)(x - c)$, de modo que la convergencia exige
$|1 - 2\eta| < 1$, es decir $\eta < 1$. Con modelos reales no hay una fórmula así, pero la
intuición se mantiene: existe un umbral por encima del cual el método explota.

> Cuando en la sesión 13 la pérdida de una red se vuelva `NaN`, la tasa de aprendizaje es el
> primer sospechoso.

### Variantes

| Variante | Cuántos datos usa por paso | Característica |
|---|---|---|
| **Batch** | Todo el conjunto | Estable, costoso |
| **Estocástico (SGD)** | Una observación | Rápido y ruidoso; el ruido ayuda a escapar de mínimos locales |
| **Mini-batch** | Un lote de 32–256 | El equilibrio usado en la práctica |

Optimizadores modernos como **Adam** añaden momento y tasas adaptativas por parámetro. Se
usan en la sesión 13.

### Mínimos locales

En una función **convexa** —como el error cuadrático de la regresión lineal— solo hay un
mínimo, y el descenso siempre llega a él. En una red neuronal la superficie no es convexa y
hay muchos mínimos locales; en la práctica esto resulta menos grave de lo que suena, porque
en dimensiones altas la mayoría de los puntos críticos son puntos de silla y el ruido del
mini-batch ayuda a salir de ellos.

## 4. La regla de la cadena

Para funciones compuestas, la derivada es el **producto** de las derivadas de cada eslabón:

$$
\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)
$$

### Por qué es la clave del deep learning

Una red neuronal es una composición de funciones, una por capa:

$$
\hat{y} = f_L(\cdots f_2(f_1(\mathbf{x})))
$$

Para saber cuánto contribuye un peso de la primera capa al error final hay que multiplicar
las derivadas de todas las capas intermedias, propagando de atrás hacia adelante. **Eso es la
retropropagación** (*backpropagation*): la regla de la cadena aplicada de forma sistemática y
eficiente. La sesión 13 le pone notación, pero la matemática es esta.

## 5. Funciones de pérdida

La pérdida es lo que el entrenamiento minimiza. Las dos básicas:

**Error cuadrático medio** (regresión):

$$
\mathcal{L}_{\text{MSE}} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
$$

Penaliza fuertemente los errores grandes, por el cuadrado. Es diferenciable en todo punto, lo
que la hace cómoda para el descenso del gradiente.

**Entropía cruzada binaria** (clasificación):

$$
\mathcal{L}_{\text{BCE}} = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i\log(\hat{p}_i) + (1-y_i)\log(1-\hat{p}_i)\right]
$$

Castiga con dureza la confianza equivocada: predecir probabilidad 0.99 para algo que era 0
produce una pérdida enorme. Se deduce del principio de máxima verosimilitud (sesión 9).

## Parte II — Probabilidad

## 6. Nociones básicas

- **Variable aleatoria**: cantidad cuyo valor depende del azar.
- **Esperanza** $\mathbb{E}[X]$: el promedio a largo plazo.
- **Varianza** $\text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2]$: cuánto se dispersa.
- **Independencia**: $P(A \cap B) = P(A)P(B)$.

## 7. Distribuciones que hay que reconocer

| Distribución | Modela | Dónde aparece |
|---|---|---|
| **Normal** | Cantidades continuas con dispersión simétrica | Errores de la regresión (S6) |
| **Bernoulli** | Un ensayo con dos resultados | Clasificación binaria (S9) |
| **Binomial** | Número de éxitos en $n$ ensayos | Muestreo, bootstrap (S10) |
| **Uniforme** | Todos los valores igual de probables | Inicialización, búsqueda aleatoria (S8) |

La distribución **normal** aparece por todas partes por el teorema central del límite: la
suma de muchos efectos pequeños e independientes tiende a ser normal. Es la justificación
del supuesto de normalidad de los residuales en la regresión lineal (sesión 6).

## 8. Probabilidad condicional y teorema de Bayes

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}
$$

De ahí se deduce el teorema de Bayes:

$$
P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}
$$

En lenguaje de modelado, con $y$ la clase y $\mathbf{x}$ las características observadas:

$$
\underbrace{P(y \mid \mathbf{x})}_{\text{posterior}} =
\frac{\overbrace{P(\mathbf{x} \mid y)}^{\text{verosimilitud}}\ \overbrace{P(y)}^{\text{prior}}}{P(\mathbf{x})}
$$

Un clasificador responde justamente a $P(y \mid \mathbf{x})$: dada la evidencia, ¿qué tan
probable es cada clase?

### La trampa de la clase rara

El teorema de Bayes explica un fenómeno que sorprende a casi todo el mundo y que es crucial
al evaluar clasificadores.

Supón una condición que afecta al 1 % de la población y una prueba con 99 % de sensibilidad
y 95 % de especificidad. Si la prueba da positivo, ¿cuál es la probabilidad de tener la
condición?

$$
P(\text{condición} \mid +) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.05 \times 0.99} \approx 0.167
$$

**Menos del 17 %.** La intuición dice 99 %, pero la clase es tan rara que los falsos
positivos, aunque proporcionalmente pocos, superan ampliamente a los verdaderos.

> Esta es la razón matemática por la que en la sesión 9 insistiremos en que la *accuracy* es
> una métrica engañosa con clases desbalanceadas, y por la que hará falta mirar precisión y
> recall por separado.

## 9. Máxima verosimilitud

Dado un modelo con parámetros $\boldsymbol{\theta}$ y unos datos observados, la
**verosimilitud** es la probabilidad de haber observado esos datos bajo esos parámetros:

$$
\mathcal{L}(\boldsymbol{\theta}) = \prod_{i=1}^{n} P(y_i \mid \mathbf{x}_i, \boldsymbol{\theta})
$$

Estimar por máxima verosimilitud es elegir los parámetros que hacen más probables los datos
observados. En la práctica se maximiza el **logaritmo** —que convierte el producto en suma y
evita problemas numéricos— o, equivalentemente, se minimiza su negativo.

Dos resultados que unifican buena parte del curso:

- Bajo errores normales, maximizar la verosimilitud **equivale** a minimizar el error
  cuadrático medio. La regresión lineal es estimación de máxima verosimilitud.
- Bajo respuesta Bernoulli, equivale a minimizar la **entropía cruzada**. La regresión
  logística también lo es.

Las funciones de pérdida de la sección 5 no son elecciones arbitrarias: salen de aquí.

## Tabla de correspondencias

| Concepto | Dónde reaparece |
|---|---|
| Derivada y gradiente | Toda optimización |
| Descenso del gradiente | Regresión (S6), redes neuronales (S13) |
| Tasa de aprendizaje | S6, S13 |
| Regla de la cadena | Retropropagación (S13) |
| MSE | Regresión (S6, S7) |
| Entropía cruzada | Clasificación (S9), redes (S13) |
| Distribución normal | Supuestos de la regresión (S6) |
| Teorema de Bayes | Métricas con clases raras (S9), Naive Bayes |
| Máxima verosimilitud | Regresión logística (S9) |

## Para recordar

- Para minimizar, muévete en contra del gradiente.
- La tasa de aprendizaje decide entre converger, tardar demasiado o explotar.
- La regla de la cadena es la retropropagación.
- MSE y entropía cruzada no son arbitrarias: se deducen de la máxima verosimilitud.
- Con clases raras, un positivo de una prueba muy buena puede seguir siendo poco informativo.

## Notebooks relacionados

- [`../notebooks/04-gradientes-intuicion.ipynb`](../notebooks/04-gradientes-intuicion.ipynb)
  — descenso del gradiente implementado a mano, hasta ajustar una regresión sin scikit-learn.

# 04 · Redes neuronales: perceptrón, MLP y retropropagación

**Módulo 5 · Sesión 13** — Deep learning (puente)

## Objetivos

- Situar la red neuronal como continuación directa de la regresión logística (S9) y del
  descenso del gradiente (S3, S6): qué es nuevo y qué no.
- Entender la arquitectura del **perceptrón multicapa** (MLP), el papel de las funciones
  de activación y por qué ReLU desplazó a la sigmoide.
- Derivar la **retropropagación** como la regla de la cadena aplicada en orden, y saber
  cómo se verifica un gradiente.
- Conocer el teorema de aproximación universal y lo que **no** dice.

## 1. De la regresión logística a la red

La regresión logística de la S9 es una neurona: una combinación lineal
$z = \mathbf{w}^\top\mathbf{x} + b$ y una función de activación $\sigma(z)$. Su antecesor,
el **perceptrón** (Rosenblatt, 1958), usaba un escalón en vez de la sigmoide y se
entrenaba con una regla de corrección de errores; la sigmoide lo hace diferenciable y por
tanto entrenable con gradiente. Ambos comparten el límite que señalaron Minsky y Papert
(1969): la frontera de decisión es un **hiperplano**. No pueden resolver XOR, ni separar
las dos medias lunas del módulo 4 (accuracy 0.86, `05-mlp-intuicion.ipynb`, sección 1).

Los módulos anteriores rodearon ese límite de dos formas: transformando las variables
**a mano** (términos polinómicos en la S7, el kernel de la SVM en la S9) o con modelos que
no son lineales de partida (árboles). Una red neuronal toma la tercera vía: **aprende la
transformación**.

## 2. El perceptrón multicapa

Un MLP apila capas. Con una capa oculta de $h$ neuronas y salida binaria:

$$
\mathbf{Z}_1 = \mathbf{X}\mathbf{W}_1 + \mathbf{b}_1, \qquad
\mathbf{H} = \phi(\mathbf{Z}_1), \qquad
\mathbf{z}_2 = \mathbf{H}\mathbf{w}_2 + b_2, \qquad
\hat{\mathbf{p}} = \sigma(\mathbf{z}_2)
$$

con $\mathbf{W}_1 \in \mathbb{R}^{p \times h}$, $\mathbf{b}_1 \in \mathbb{R}^h$,
$\mathbf{w}_2 \in \mathbb{R}^h$, $b_2 \in \mathbb{R}$, y $\phi$ una función no lineal
aplicada elemento a elemento. Tres observaciones:

- La última capa **es** una regresión logística, sobre $\mathbf{H}$ en vez de sobre
  $\mathbf{X}$: las $h$ columnas de $\mathbf{H}$ son variables construidas por la red.
- Sin $\phi$ no hay nada: la composición de dos capas lineales es otra capa lineal,
  $\mathbf{X}\mathbf{W}_1\mathbf{w}_2 = \mathbf{X}\mathbf{w}'$. La **no linealidad** es lo que
  permite que la frontera se curve. Con una neurona oculta la frontera sigue siendo una
  recta (una $\tanh$ es monótona); con dos se quiebra; con cuatro sigue la curva de las
  lunas (accuracy 0.96); con dieciséis la sigue y empieza a ajustar ruido
  (`05-mlp-intuicion.ipynb`, sección 4).
- Más capas = **profundidad** (*deep*). Con $L$ capas ocultas, $\mathbf{H}_l = \phi(\mathbf{H}_{l-1}\mathbf{W}_l + \mathbf{b}_l)$.
  Cada capa construye variables a partir de las de la anterior; en imágenes, eso da
  bordes → texturas → partes → objetos. Para datos tabulares, 1–3 capas es lo habitual.

Para $K$ clases, la salida tiene $K$ neuronas y la activación final es la **softmax** de
la S9; la pérdida, la entropía cruzada multiclase (`CrossEntropyLoss` en PyTorch, que
incluye la softmax). Para regresión, salida lineal y pérdida cuadrática.

## 3. Funciones de activación

| $\phi(z)$ | Fórmula | $\phi'(z)$ | Uso |
|---|---|---|---|
| Sigmoide | $1 / (1 + e^{-z})$ | $\phi(1 - \phi) \leq 0.25$ | Solo en la salida binaria |
| $\tanh$ | $(e^z - e^{-z}) / (e^z + e^{-z})$ | $1 - \tanh^2 \leq 1$ | Capas ocultas en redes pequeñas; recurrentes |
| **ReLU** | $\max(0, z)$ | $\mathbb{1}[z > 0]$ | Capas ocultas, por defecto |
| Leaky ReLU, GELU, … | variantes suaves o con pendiente para $z < 0$ | | Cuando ReLU "mata" neuronas |

La derivada importa tanto como la función, porque es el factor por el que se multiplica
el gradiente al atravesar la capa hacia atrás (§4). La derivada de la sigmoide vale como
máximo 0.25 y es casi cero fuera de $[-4, 4]$: en una red de $L$ capas, el gradiente que
llega a la primera es un producto de $L$ factores así, y se **desvanece**. Medido en una
red de 10 capas ocultas en la inicialización (`05-mlp-intuicion.ipynb`, sección 5): con
sigmoide, la primera capa recibe un gradiente $10^6$ veces menor que la última; con
$\tanh$ y ReLU bien inicializadas, del mismo orden (cociente 0.3–0.4). Ese *vanishing
gradient* es la razón de que las redes profundas no se pudieran entrenar antes de ~2010,
y ReLU (Nair y Hinton, 2010; Glorot et al., 2011) es la solución más simple: derivada
exactamente 1 para $z > 0$. Su defecto —una neurona con $z < 0$ para todos los datos no
recibe gradiente y "muere"— lo suavizan sus variantes.

La **inicialización** de los pesos es parte de la misma historia: demasiado grandes y
las activaciones saturan; demasiado pequeños y las señales se apagan capa a capa. Las
reglas de Glorot/Xavier (para sigmoide y $\tanh$) y He (para ReLU) escalan la varianza
inicial de cada capa según su número de entradas para que la señal y el gradiente
conserven su escala. PyTorch las aplica por defecto (o casi); no es algo que se elija a
diario, pero explica por qué "una red que no aprende" a veces se arregla cambiando la
inicialización.

## 4. Retropropagación

Entrenar es minimizar $\mathcal{L}(\theta)$ sobre todos los pesos con descenso del
gradiente, el mismo bucle de los módulos 1, 3 y 4. Lo único nuevo es calcular
$\partial\mathcal{L}/\partial\theta$ para parámetros que están detrás de varias capas.
La **retropropagación** (Rumelhart, Hinton y Williams, 1986) es la regla de la cadena de
la S3 aplicada **de la salida hacia la entrada**, reutilizando en cada capa lo calculado
en la siguiente. Para la red de §2 con entropía cruzada, $n$ observaciones y
$\boldsymbol{\delta}_2 = \hat{\mathbf{p}} - \mathbf{y}$:

$$
\frac{\partial\mathcal{L}}{\partial\mathbf{w}_2} = \frac{1}{n}\mathbf{H}^\top\boldsymbol{\delta}_2, \qquad
\frac{\partial\mathcal{L}}{\partial b_2} = \frac{1}{n}\sum_i \delta_{2,i}
$$

$$
\boldsymbol{\Delta}_1 = (\boldsymbol{\delta}_2\mathbf{w}_2^\top) \odot \phi'(\mathbf{Z}_1), \qquad
\frac{\partial\mathcal{L}}{\partial\mathbf{W}_1} = \frac{1}{n}\mathbf{X}^\top\boldsymbol{\Delta}_1, \qquad
\frac{\partial\mathcal{L}}{\partial\mathbf{b}_1} = \frac{1}{n}\sum_i \boldsymbol{\Delta}_{1,i}
$$

La primera línea es exactamente el gradiente de la regresión logística (módulo 4,
notebook 01) con $\mathbf{H}$ en lugar de $\mathbf{X}$: el "residual" $\hat p - y$ multiplicado
por la entrada de la capa. La segunda **propaga** el residual hacia atrás: cada neurona
oculta $j$ recibe la parte del error que le corresponde según su peso $w_{2,j}$,
multiplicada por la pendiente de su activación $\phi'(z_{1,j})$ — ahí está el factor que
se desvanece con la sigmoide. Con más capas, la misma línea se repite: $\boldsymbol{\Delta}_{l-1} =
(\boldsymbol{\Delta}_l\mathbf{W}_l^\top) \odot \phi'(\mathbf{Z}_{l-1})$.

Dos cosas que conviene saber:

- **Costo**: una pasada hacia atrás cuesta aproximadamente lo mismo que una hacia
  adelante, y los valores intermedios ($\mathbf{Z}_1$, $\mathbf{H}$) hay que guardarlos. Es
  lo que hace viable entrenar redes con millones de parámetros.
- **Verificación**: un gradiente escrito a mano se comprueba contra diferencias finitas,
  $[\mathcal{L}(\theta + \epsilon) - \mathcal{L}(\theta - \epsilon)] / 2\epsilon$ para cada
  parámetro. `05-mlp-intuicion.ipynb` (sección 3) lo hace y coincide a $10^{-10}$; y
  también coincide con el **autograd** de PyTorch, que registra cada operación de la
  pasada hacia adelante y aplica la regla de la cadena hacia atrás para cualquier grafo
  de cómputo. Cada `loss.backward()` del notebook 06 es esto.

## 5. Aproximación universal, y lo que no dice

**Teorema** (Cybenko, 1989; Hornik, 1991): un MLP con una capa oculta y una activación no
polinómica puede aproximar cualquier función continua sobre un compacto con precisión
arbitraria, si la capa es suficientemente ancha. Se ve en `05-mlp-intuicion.ipynb`
(sección 6): sobre $y = \sin(2\pi x) + \varepsilon$, 10 neuronas $\tanh$ dan el seno.

Lo que el teorema **no** dice:

- Cuántas neuronas hacen falta (puede ser un número enorme), ni que el descenso del
  gradiente vaya a **encontrar** esos pesos. Con 3 neuronas, la optimización del notebook
  se queda en una solución pobre.
- Que aproximar bien los **datos** sea aproximar bien la **función**: el mismo poder de
  aproximación sirve para el ruido. Y aquí hay un matiz medido: con 60 puntos y descenso
  del gradiente desde pesos pequeños, la red de 100 neuronas **no** sobreajusta — ajusta
  la función verdadera mejor que la de 10 (ECM 0.011 frente a 0.079). La
  sobreparametrización con gradiente se comporta mejor de lo que el conteo de parámetros
  sugiere (fenómeno activo en la investigación: *doble descenso*, Belkin et al., 2019).
  No es una garantía: sobre 120 puntos de las lunas con 64 neuronas, la pérdida de
  validación toca fondo en la época ≈120 y sube de 0.22 a 0.29 en la 1500. El
  sobreajuste de una red depende de los datos, las épocas y la inicialización, y se
  vigila con validación (`05-entrenamiento-y-limites.md`).
- Que la red generalice mejor que otro modelo con el mismo poder: los árboles con
  boosting también aproximan cualquier función, y sobre datos tabulares suelen hacerlo
  mejor con menos esfuerzo (`05-entrenamiento-y-limites.md`, §4).

## Referencias

- Rumelhart, D., Hinton, G. y Williams, R. (1986). Learning representations by
  back-propagating errors. *Nature*.
- Glorot, X. y Bengio, Y. (2010). Understanding the difficulty of training deep
  feedforward neural networks. *AISTATS*.
- Cybenko, G. (1989). Approximation by superpositions of a sigmoidal function.
  *Mathematics of Control, Signals and Systems*.
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*, caps. 6 y 8.
  MIT Press (gratis en deeplearningbook.org).
- Nielsen, M. (2015). *Neural Networks and Deep Learning*, caps. 1–2 (retropropagación
  explicada paso a paso).

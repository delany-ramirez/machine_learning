# Solución · Ejercicio 03 · Retropropagación con dos capas, y cuándo la red no gana

> **Material del docente.** Números con semilla 42 en todo (particiones, K-fold repetido,
> `torch.manual_seed`). Los tiempos son orientativos; las AP y los RMSE se reproducen a la
> tercera cifra en CPU.

## Parte A — Dos capas ocultas a mano

**A.1** Con $\mathbf{W}_1 \in \mathbb{R}^{p \times h_1}$, $\mathbf{W}_2 \in \mathbb{R}^{h_1 \times h_2}$,
$\mathbf{w}_3 \in \mathbb{R}^{h_2}$:

$$
\mathbf{Z}_1 = \mathbf{X}\mathbf{W}_1 + \mathbf{b}_1, \quad \mathbf{H}_1 = \tanh(\mathbf{Z}_1), \quad
\mathbf{Z}_2 = \mathbf{H}_1\mathbf{W}_2 + \mathbf{b}_2, \quad \mathbf{H}_2 = \tanh(\mathbf{Z}_2), \quad
\mathbf{z}_3 = \mathbf{H}_2\mathbf{w}_3 + b_3, \quad \hat{\mathbf{p}} = \sigma(\mathbf{z}_3)
$$

**A.2** Con $\boldsymbol{\delta}_3 = \hat{\mathbf{p}} - \mathbf{y}$ ($n$) y $\odot$ elemento a
elemento:

$$
\frac{\partial\mathcal{L}}{\partial\mathbf{w}_3} = \frac{1}{n}\mathbf{H}_2^\top\boldsymbol{\delta}_3, \qquad
\boldsymbol{\Delta}_2 = (\boldsymbol{\delta}_3\mathbf{w}_3^\top) \odot (1 - \mathbf{H}_2^2), \qquad
\frac{\partial\mathcal{L}}{\partial\mathbf{W}_2} = \frac{1}{n}\mathbf{H}_1^\top\boldsymbol{\Delta}_2
$$

$$
\boldsymbol{\Delta}_1 = (\boldsymbol{\Delta}_2\mathbf{W}_2^\top) \odot (1 - \mathbf{H}_1^2), \qquad
\frac{\partial\mathcal{L}}{\partial\mathbf{W}_1} = \frac{1}{n}\mathbf{X}^\top\boldsymbol{\Delta}_1
$$

(y los sesgos, la media por columna de cada $\boldsymbol{\Delta}$). La línea nueva es
$\boldsymbol{\Delta}_1 = (\boldsymbol{\Delta}_2\mathbf{W}_2^\top) \odot \phi'(\mathbf{Z}_1)$:
$\boldsymbol{\Delta}_2$ es $n \times h_2$ (cuánto error llega a cada neurona de la capa 2), y
para repartirlo entre las $h_1$ neuronas de la capa 1 hay que multiplicar por
$\mathbf{W}_2^\top$ ($h_2 \times h_1$): la neurona $j$ de la capa 1 recibe la suma, sobre las
neuronas $k$ de la capa 2, de $\Delta_{2,k} \cdot W_{2,jk}$ — el error de $k$ ponderado por
cuánto contribuyó $j$ a $k$. Es transpuesta porque en la pasada hacia adelante
$\mathbf{W}_2$ lleva de $h_1$ a $h_2$, y hacia atrás hay que ir de $h_2$ a $h_1$. En el
notebook 05, con una sola capa oculta, $\mathbf{w}_2$ era un vector y el producto externo
$\boldsymbol{\delta}_2\mathbf{w}_2^\top$ era el caso particular.

**A.3** Error relativo máximo entre el gradiente analítico y el numérico: $6.9 \times
10^{-9}$ sobre los seis grupos de parámetros. (Un error de signo o una transpuesta
olvidada da errores de orden 1; un error en un solo sesgo, de orden $10^{-1}$ en ese
parámetro.)

**A.4** Hacia adelante: $L + 1$ productos matriz-por-matriz (uno por capa). Hacia atrás:
$2L$, aproximadamente — por cada capa, uno para el gradiente del peso
($\mathbf{H}_{l-1}^\top\boldsymbol{\Delta}_l$) y otro para propagar
($\boldsymbol{\Delta}_l\mathbf{W}_l^\top$). El costo es del mismo orden que la pasada hacia
adelante (unas 2×). Hay que guardar **las activaciones de cada capa**
($\mathbf{H}_1, \dots, \mathbf{H}_L$, o las $\mathbf{Z}_l$): es la memoria que consume el
entrenamiento, proporcional al tamaño del lote por la anchura de la red, y la razón de que
el lote no pueda ser arbitrariamente grande.

## Parte B — Cuando la verdad es lineal

**B.1**

| Modelo | RMSE (10 pliegues) |
|---|---|
| Regresión lineal | **0.342 ± 0.007** |
| Extra-Trees (300) | 0.392 ± 0.007 |
| MLP 32-16 | 0.357 ± 0.010 |

**B.2** MLP − lineal $= +0.015 \pm 0.005$ (cociente 3.3); Extra-Trees − lineal $= +0.050
\pm 0.005$ (cociente 9.9). **Ninguno gana**; ambos pierden de forma detectable. No deberían
poder ganar porque el proceso generador es exactamente lineal: el modelo lineal es el
correcto y el mejor estimador insesgado posible con 400 datos. Y pierden en vez de
empatar porque un modelo flexible **paga varianza** por su flexibilidad (S8): ajusta parte
del ruido de los 320 puntos de entrenamiento de cada pliegue. Extra-Trees lo paga más
(escalones sobre una recta); el MLP con early stopping y weight decay se acerca a la
lineal pero no la alcanza. Cuando la forma verdadera es simple, el modelo simple gana —
y la única forma de saber la forma verdadera es medir.

**B.3** El generador usa $\sigma_{\text{ruido}} = 0.35$. El RMSE del modelo lineal (0.342)
está al nivel del ruido: **todo lo que se puede explicar, lo explica**, y lo que queda
(0.35 de 0.59 de desviación, es decir, $1 - 0.35^2 / 0.59^2 \approx 65\,\%$ de la varianza
explicada) es irreducible por construcción. Ningún modelo puede bajar de 0.35 sobre datos
nuevos; un RMSE de entrenamiento menor que eso es sobreajuste.

## Parte C — Adult Census: ¿más red ayuda?

**C.1**

| Modelo | AP (CV 5) | Segundos por pliegue |
|---|---|---|
| Regresión logística | 0.766 ± 0.002 | 0.2 |
| **LightGBM** (categóricas nativas) | **0.828 ± 0.002** | 0.2 |
| MLP 64, dropout 0.1 | 0.781 ± 0.002 | 1.8 |
| MLP 256-128, dropout 0.3 | 0.779 ± 0.002 | 2.9 |

**C.2** MLP 64 − LightGBM $= -0.046 \pm 0.001$; MLP 256-128 − LightGBM $= -0.049 \pm 0.001$.
La red grande **no** mejora a la pequeña (es incluso una milésima peor, dentro del ruido)
y tarda más. Ninguna se acerca a LightGBM: la distancia es de casi cinco centésimas con
un error estándar de una milésima. Más capacidad no es lo que falta; es el sesgo
inductivo (`05-entrenamiento-y-limites.md`, §3).

**C.3** Con el early stopping sobre el pliegue evaluado, el MLP 256-128 sube a 0.783: la
fuga infla la AP en $+0.004 \pm 0.001$. Es detectable (cociente 4) e irrelevante frente a
los 0.049 que lo separan de LightGBM: aquí corregir la fuga no cambia la conclusión. En
Wine Quality (notebook 06, sección 4) la misma fuga valía 0.017 — con menos datos, elegir
la época sobre el conjunto evaluado se aprovecha más del azar. La regla es la misma en
los dos casos; el tamaño del daño depende de $n$.

**C.4** Épocas de parada del MLP 256-128 en los cinco pliegues: 13, 19, 8, 8, 5. Con
39 000 filas y lotes de 256, una época son ~130 pasos de gradiente; en 5–20 épocas la red
ya recorrió los datos suficientes veces para llegar a su mejor AP de validación, y a
partir de ahí memoriza (dropout 0.3 incluido). Entrenar 100 épocas fijas sin validación
daría un modelo peor —sobreajustado— y tardaría 5–20 veces más. El número de épocas no
es un hiperparámetro que se fija: se **decide con validación**, como el número de rondas
en boosting (S11).

## Recomendación para el proyecto (lo que se espera)

Sobre datos tabulares como los del proyecto, la red neuronal no es el modelo por defecto:
la línea base es la logística/lineal y el modelo fuerte es un ensamble de árboles. Solo
probaría un MLP si (a) hay muchos datos, (b) sobra tiempo después de afinar el ensamble,
y (c) hay interacciones que el ensamble no captura. Y antes de adoptarlo exigiría la
comparación pareada sobre los mismos pliegues, con error estándar, con el early stopping
sobre datos apartados del entrenamiento, y con el tiempo de entrenamiento al lado — y
que la diferencia sea detectable **y** relevante para la decisión del proyecto.

# 04 · Álgebra lineal para Machine Learning

**Módulo 1 · Sesión 3**

> **Objetivos.** Representar datos como vectores y matrices; dominar el producto punto y el
> producto matricial como operaciones centrales de todo modelo lineal; entender normas y
> distancias y su papel en la regularización y en los algoritmos basados en similitud; e
> interpretar la matriz de covarianza, sus vectores propios y la descomposición SVD como
> fundamento de PCA.

Este documento cubre el subconjunto del álgebra lineal que realmente se usa en Machine
Learning. Cada sección termina indicando dónde reaparece el concepto en el curso.

## 1. Los datos como vectores y matrices

La idea que conecta el álgebra lineal con el ML: **cada observación es un punto en un espacio
de tantas dimensiones como variables tenga**.

Un estudiante descrito por su promedio previo, sus horas de estudio y su asistencia es el
vector

$$
\mathbf{x} = (4.2,\ 12,\ 90) \in \mathbb{R}^{3}
$$

Un conjunto de datos con $n$ observaciones y $p$ variables es la **matriz de diseño**

$$
\mathbf{X} \in \mathbb{R}^{n \times p}
$$

con una fila por observación y una columna por variable. Casi toda la notación del curso
descansa sobre esta convención: $\mathbf{X}$ mayúscula para la matriz de características,
$y$ minúscula para el vector objetivo.

## 2. El producto punto

Dados dos vectores $\mathbf{a}, \mathbf{b} \in \mathbb{R}^{p}$:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{p} a_i b_i
$$

### Por qué es la operación central

**Toda predicción lineal es un producto punto.** Un modelo lineal con intercepto $\beta_0$ y
coeficientes $\boldsymbol{\beta}$ predice

$$
\hat{y} = \beta_0 + \boldsymbol{\beta} \cdot \mathbf{x}
$$

y para todo el conjunto de datos a la vez, sin ningún bucle,

$$
\hat{\mathbf{y}} = \beta_0\mathbf{1} + \mathbf{X}\boldsymbol{\beta}
$$

Esta es la razón práctica por la que el ML se escribe en álgebra lineal: una sola operación
matricial reemplaza un bucle sobre millones de filas, y las bibliotecas la ejecutan en código
optimizado (y en GPU cuando hace falta). La diferencia medida en el notebook 03 es de uno a
dos órdenes de magnitud.

### Interpretación geométrica

$$
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

El producto punto mide **alineación**. Despejando el coseno se obtiene la **similitud
coseno**:

$$
\text{sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|} \in [-1, 1]
$$

Vale 1 si los vectores apuntan en la misma dirección, 0 si son perpendiculares, $-1$ si son
opuestos. Es la medida estándar para comparar documentos y representaciones vectoriales de
texto (*embeddings*).

> **Dónde reaparece:** regresión lineal (S6), regresión logística (S9), cada neurona de una
> red (S13).

## 3. Normas: el tamaño de un vector

$$
\|\mathbf{v}\|_1 = \sum_{i} |v_i|
\qquad\qquad
\|\mathbf{v}\|_2 = \sqrt{\sum_{i} v_i^2}
$$

La $L_2$ es la longitud euclidiana de toda la vida. La $L_1$ —llamada *Manhattan*— suma
desplazamientos por ejes, como quien camina por una cuadrícula de calles.

### Por qué importan: la regularización

En la sesión 7 se añade una penalización a la función de error para evitar que los
coeficientes crezcan sin control:

$$
\text{Ridge:}\quad \mathcal{L} + \lambda\|\boldsymbol{\beta}\|_2^2
\qquad\qquad
\text{Lasso:}\quad \mathcal{L} + \lambda\|\boldsymbol{\beta}\|_1
$$

La diferencia de comportamiento entre ambas —Ridge encoge los coeficientes hacia cero, Lasso
lleva algunos **exactamente** a cero, haciendo selección de variables— proviene enteramente de
la geometría de las dos normas. La región $\|\boldsymbol{\beta}\|_1 \leq t$ es un rombo con
vértices sobre los ejes; la región $\|\boldsymbol{\beta}\|_2 \leq t$ es un círculo sin
esquinas. Las esquinas, que están sobre los ejes (donde alguna coordenada vale cero), son las
que anulan coeficientes.

> **Dónde reaparece:** Ridge, Lasso y Elastic Net (S7); regularización de redes (S13).

## 4. Distancias

La distancia entre dos observaciones es la norma de su diferencia:

$$
d(\mathbf{u}, \mathbf{v}) = \|\mathbf{u} - \mathbf{v}\|_2 = \sqrt{\sum_i (u_i - v_i)^2}
$$

Buscar "las observaciones más parecidas a esta" es ordenar por esta distancia. Eso es
literalmente K-Nearest Neighbors, y también el criterio de asignación de K-Means.

### La trampa de las escalas

Si una variable va de 0 a 100 y otra de 0 a 5, la distancia queda **dominada por la primera**,
solo porque sus números son más grandes — no porque sea más informativa.

La solución es **estandarizar**: llevar cada variable a media 0 y desviación 1.

$$
z = \frac{x - \mu}{\sigma}
$$

> **Esta es una de las reglas prácticas más importantes del curso: todo algoritmo basado en
> distancias exige variables estandarizadas.** Aplica a KNN, SVM, K-Means, DBSCAN, PCA y a
> las redes neuronales. Se formaliza en la sesión 5 y no se vuelve a discutir.

> **Dónde reaparece:** KNN y SVM (S9); K-Means y DBSCAN (S12).

## 5. La matriz de covarianza

La covarianza mide cómo varían dos variables conjuntamente. Con las columnas centradas
(media cero) en $\mathbf{X}_c$:

$$
\mathbf{\Sigma} = \frac{1}{n-1}\,\mathbf{X}_c^{\top}\mathbf{X}_c \in \mathbb{R}^{p \times p}
$$

En la diagonal están las varianzas de cada variable; fuera de ella, las covarianzas entre
parejas. Es simétrica por construcción.

Como sus valores dependen de las unidades, suele preferirse la **correlación**, que es la
covarianza estandarizada y siempre está entre $-1$ y $1$:

$$
\rho_{ij} = \frac{\Sigma_{ij}}{\sigma_i \sigma_j}
$$

> **Dónde reaparece:** diagnóstico de multicolinealidad (S7); PCA (S12).

## 6. Vectores y valores propios

Un **vector propio** de una matriz cuadrada $\mathbf{A}$ es un vector al que la matriz no
rota: solo lo escala. El factor de escala es su **valor propio**.

$$
\mathbf{A}\mathbf{v} = \lambda\mathbf{v}
$$

Aplicado a la matriz de covarianza, esto adquiere un significado muy concreto:

- Los **vectores propios** de $\mathbf{\Sigma}$ son las **direcciones de máxima variabilidad**
  de los datos.
- Los **valores propios** dicen **cuánta variabilidad** hay en cada una de esas direcciones.

Eso es exactamente el Análisis de Componentes Principales. Ordenando los valores propios de
mayor a menor, la fracción de varianza explicada por la componente $k$ es

$$
\frac{\lambda_k}{\sum_j \lambda_j}
$$

Como $\mathbf{\Sigma}$ es simétrica, sus vectores propios son **ortogonales entre sí**: las
componentes principales no están correlacionadas, que es justamente lo que las hace útiles.

> **Dónde reaparece:** PCA (S12).

## 7. Descomposición en valores singulares (SVD)

La SVD factoriza **cualquier** matriz, sin exigir que sea cuadrada ni simétrica:

$$
\mathbf{X} = \mathbf{U}\mathbf{S}\mathbf{V}^{\top}
$$

- $\mathbf{V}$ contiene las direcciones principales — las mismas que los vectores propios de
  la covarianza.
- $\mathbf{S}$ es diagonal y contiene los **valores singulares**, que cuantifican la
  importancia de cada dirección.
- $\mathbf{U}$ contiene las coordenadas de las observaciones en ese nuevo sistema.

La relación con la sección anterior es exacta: si $s_k$ es el $k$-ésimo valor singular de la
matriz centrada, entonces

$$
\lambda_k = \frac{s_k^2}{n-1}
$$

**SVD y la descomposición espectral de la covarianza son la misma cosa vista desde dos
ángulos.** scikit-learn calcula PCA vía SVD porque es numéricamente más estable que formar la
covarianza y diagonalizarla.

### Aproximación de rango bajo

Si se conservan solo las $k$ direcciones más importantes,

$$
\mathbf{X} \approx \mathbf{U}_k\mathbf{S}_k\mathbf{V}_k^{\top}
$$

se obtiene la mejor aproximación posible de la matriz con esa cantidad de información
(teorema de Eckart-Young). Esto es comprimir: menos números, casi los mismos datos.

Sobre el dataset del módulo, dos direcciones de cuatro bastan para reconstruir los datos con
menos del 7 % de error. Esa es la idea de fondo de la reducción de dimensionalidad: **la
información real de un conjunto de datos suele vivir en muchas menos dimensiones de las que
tiene la tabla**.

> **Dónde reaparece:** PCA (S12); compresión y reducción de ruido.

## Tabla de correspondencias

| Concepto | Dónde reaparece en el curso |
|---|---|
| Producto punto | Regresión lineal y logística (S6, S9), redes (S13) |
| Producto matricial | Predicción vectorizada, en todo el curso |
| Norma $L_2$ | Ridge (S7), distancias euclidianas |
| Norma $L_1$ | Lasso (S7) |
| Distancia | KNN (S9), K-Means y DBSCAN (S12) |
| Estandarización | S5, y todo algoritmo basado en distancias |
| Covarianza / correlación | Multicolinealidad (S7), PCA (S12) |
| Vectores propios | PCA (S12) |
| SVD | PCA (S12) |

## Para recordar

- Una observación es un vector; un dataset es una matriz $\mathbf{X} \in \mathbb{R}^{n\times p}$.
- Toda predicción lineal es un producto punto; vectorizar no es elegancia, es velocidad.
- $L_1$ y $L_2$ producen Lasso y Ridge, y su diferencia es puramente geométrica.
- Todo lo que use distancias necesita variables estandarizadas.
- Los vectores propios de la covarianza son las direcciones de máxima varianza: eso es PCA.
- SVD generaliza esa idea y es como se calcula PCA en la práctica.

## Notebooks relacionados

- [`../notebooks/03-algebra-lineal-intuicion.ipynb`](../notebooks/03-algebra-lineal-intuicion.ipynb)
  — todo lo anterior implementado a mano con NumPy.

## Documento siguiente

- [`05-calculo-y-probabilidad.md`](05-calculo-y-probabilidad.md) — gradientes y probabilidad.

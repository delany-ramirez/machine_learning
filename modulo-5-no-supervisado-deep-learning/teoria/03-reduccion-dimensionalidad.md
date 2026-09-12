# 03 · Reducción de dimensionalidad: PCA, t-SNE y UMAP

**Módulo 5 · Sesión 12** — Aprendizaje no supervisado

## Objetivos

- Derivar PCA desde la matriz de covarianza y la SVD (S3), y saber leer varianza
  explicada, cargas y *scree plot*.
- Distinguir para qué sirve PCA (comprimir, eliminar redundancia, visualizar) y cuándo
  falla (variables incorreladas) o daña (información en direcciones de poca varianza).
- Entender qué conservan t-SNE y 🔵 UMAP —vecindarios— y qué no —tamaños, distancias,
  y a veces la existencia misma de los grupos—.

## 1. Por qué reducir

Con $p$ variables, hay $p$ ejes; nadie ve más de tres. Pero además de visualizar, reducir
la dimensión sirve para **comprimir** (imágenes, señales), para **eliminar redundancia**
antes de un modelo (la multicolinealidad de S7 es exactamente correlación entre variables),
y para **filtrar ruido** (las direcciones de varianza minúscula suelen ser ruido de medición).
Dos familias:

- **Lineales**: la representación es una proyección $\mathbf{Z} = \mathbf{X}_c \mathbf{V}_q$
  sobre $q$ direcciones. PCA es la principal. Conserva distancias grandes, tiene
  `transform` para puntos nuevos, y sus coordenadas se interpretan.
- **No lineales** (o de *manifold*): buscan una disposición en 2D que conserve las
  relaciones **locales** (quién es vecino de quién). t-SNE, UMAP. Producen mapas mucho más
  legibles cuando la estructura vive en una variedad curva; a cambio, no conservan las
  distancias grandes y sus coordenadas no significan nada.

## 2. Análisis de componentes principales

### Derivación

Sea $\mathbf{X}_c$ la matriz de datos **centrada** (cada columna con media cero) y
$\mathbf{S} = \mathbf{X}_c^\top \mathbf{X}_c / (n - 1)$ su covarianza. La primera
componente principal es la dirección unitaria $\mathbf{v}_1$ que maximiza la varianza de la
proyección:

$$
\mathbf{v}_1 = \arg\max_{\lVert \mathbf{v} \rVert = 1} \operatorname{Var}(\mathbf{X}_c \mathbf{v}) = \arg\max_{\lVert \mathbf{v} \rVert = 1} \mathbf{v}^\top \mathbf{S} \mathbf{v}
$$

Con un multiplicador de Lagrange para la restricción, la condición de óptimo es
$\mathbf{S}\mathbf{v} = \lambda \mathbf{v}$: $\mathbf{v}_1$ es el **autovector** de
$\mathbf{S}$ con mayor autovalor $\lambda_1$, y $\lambda_1$ es la varianza a lo largo de
él. La segunda componente maximiza la varianza entre las direcciones ortogonales a
$\mathbf{v}_1$, y es el segundo autovector; y así hasta $p$. Como $\mathbf{S}$ es simétrica,
los autovectores son ortogonales y la suma de los autovalores es la varianza total
$\operatorname{tr}(\mathbf{S})$, de donde sale la **fracción de varianza explicada**
$\lambda_j / \sum_l \lambda_l$.

La misma respuesta por la **SVD** (S3): $\mathbf{X}_c = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$,
con lo que $\mathbf{S} = \mathbf{V}\boldsymbol{\Sigma}^2\mathbf{V}^\top / (n-1)$. Las columnas
de $\mathbf{V}$ son los componentes, $\lambda_j = \sigma_j^2 / (n-1)$, y las **puntuaciones**
(las coordenadas de cada observación) son $\mathbf{Z} = \mathbf{X}_c\mathbf{V} = \mathbf{U}\boldsymbol{\Sigma}$.
Es lo que hace `scikit-learn`, porque es más estable numéricamente que formar $\mathbf{S}$.
`03-pca-intuicion.ipynb` (sección 1) calcula los componentes de las dos formas y verifica
que coinciden entre sí y con `PCA` — **salvo signo**: $\mathbf{v}$ y $-\mathbf{v}$ son la
misma dirección, y distintas implementaciones devuelven uno u otro.

### Reconstrucción y error

Con los primeros $q$ componentes $\mathbf{V}_q$, cada punto se reconstruye como
$\hat{\mathbf{x}} = \bar{\mathbf{x}} + \mathbf{V}_q\mathbf{V}_q^\top(\mathbf{x} - \bar{\mathbf{x}})$,
y el error cuadrático medio de reconstrucción es exactamente la varianza descartada
$\sum_{j > q} \lambda_j$. PCA es la proyección lineal de rango $q$ con **menor error de
reconstrucción** (teorema de Eckart-Young). Sobre los dígitos de 8 × 8, 10 de 64
componentes (74 % de la varianza) bastan para reconocerlos y 20 (89 %) los reconstruyen
casi sin pérdida (`03-pca-intuicion.ipynb`, sección 4): los píxeles vecinos están muy
correlacionados, y eso es lo que PCA explota.

### Estandarizar

PCA maximiza varianza y la varianza depende de las unidades. Sin estandarizar, sobre las
11 variables de Wine Quality el 95 % de la "varianza" está en un componente que es
`total_sulfur_dioxide` (carga 0.97): PCA no encontró estructura, encontró las unidades.
Estandarizado, cada variable aporta 1 a una varianza total de $p$, y PC1 pasa a ser el
eje tinto/blanco con el 27 %. La excepción: cuando todas las variables están en la misma
unidad y sus varianzas *son* informativas (píxeles, series de tiempo de la misma magnitud).

### Leer un PCA

- ***Scree plot***: la varianza explicada por componente, en orden. Un scree que cae
  bruscamente y se aplana indica pocas direcciones importantes; uno plano (todas las
  varianzas parecidas) indica que **no hay nada que comprimir**. Los seis predictores de
  `rendimiento-estudiantes.csv` se generaron independientes: 24, 18, 17, 15, 14, 11 %; dos
  componentes retienen el 43 %, frente al 50 % de Wine Quality, cuyas variables sí están
  correlacionadas. Antes de PCA, mirar la matriz de correlaciones: si está vacía, PCA no
  tiene qué encontrar.
- **Cuántos componentes**: tres reglas que dan cosas distintas. Varianza acumulada
  (80–90 %: 5–7 en Wine), Kaiser (autovalor $> 1$ con datos estandarizados: 3), codo del
  scree (3–4). La correcta depende de para qué: 2 para visualizar; para comprimir, los que
  den un error aceptable; para preprocesar un modelo, los que no pierdan lo que el modelo
  necesita — y eso se valida con la métrica del modelo, no con la varianza.
- **Cargas** (*loadings*): las coordenadas de cada componente en las variables originales,
  $\mathbf{v}_j$. Dicen qué mide el componente. En Wine Quality, PC1 carga positivo en los
  dióxidos de azufre y el azúcar y negativo en acidez volátil, cloruros y sulfatos (blanco
  ↔ tinto); PC2, positivo en densidad y azúcar y negativo en alcohol (dulce ↔ seco). Las
  mismas dos estructuras que K-Means encontró en `02-clustering-aplicado.ipynb`, porque
  ambos buscan lo mismo: la varianza dominante. El **biplot** superpone las cargas (como
  flechas) sobre las puntuaciones.

### Cuándo PCA daña

PCA **no ve $y$**. Si lo que distingue las clases es una dirección de poca varianza, es la
primera que se descarta. En el ejemplo construido de `03-pca-intuicion.ipynb` (sección 5),
PC1 explica el 91 % de la varianza y da accuracy 0.47 (el azar); PC2, con el 9 %, da 0.93.
"Conservar el 90 %" habría tirado exactamente la información útil. En Wine Quality, con
la calidad como objetivo, ocurre en pequeño: la AP de una regresión logística baja de
0.52 con las 11 variables a 0.50 con 7 componentes (90 %), 0.46 con 5 y 0.40 con 2. Y con
los 11 componentes la AP es idéntica a la del modelo sin PCA: **PCA completo es una
rotación**, y un modelo lineal es invariante a rotaciones. Reducir con PCA antes de un
modelo supervisado es una decisión que se **valida con la métrica del modelo** y, como
cualquier transformación, se ajusta **dentro del `Pipeline`**, solo con datos de
entrenamiento (módulo 2).

## 3. t-SNE

*t-distributed Stochastic Neighbor Embedding* (van der Maaten y Hinton, 2008) busca una
disposición $\mathbf{z}_1, \dots, \mathbf{z}_n \in \mathbb{R}^2$ que conserve **quién es
vecino de quién**, no las distancias.

1. Arriba, define similitudes con un núcleo gaussiano centrado en cada punto,
   $p_{j|i} \propto \exp(-\lVert \mathbf{x}_i - \mathbf{x}_j \rVert^2 / 2\sigma_i^2)$,
   simetrizadas a $p_{ij}$. La anchura $\sigma_i$ se ajusta **por punto** para que el número
   efectivo de vecinos —la **perplejidad**, $2^{H(p_{\cdot|i})}$— sea el que se pide
   (5–50). Así, un punto en una región densa tiene un $\sigma_i$ pequeño y uno en una
   región dispersa, grande: la densidad local se **normaliza**.
2. Abajo, define $q_{ij} \propto (1 + \lVert \mathbf{z}_i - \mathbf{z}_j \rVert^2)^{-1}$,
   un núcleo **t de Student** con un grado de libertad.
3. Minimiza $\text{KL}(P \,\|\, Q) = \sum_{i \neq j} p_{ij} \log (p_{ij} / q_{ij})$ por
   descenso del gradiente sobre las $\mathbf{z}_i$.

La KL es asimétrica a propósito: castiga mucho que dos vecinos ($p_{ij}$ grande) queden
lejos ($q_{ij}$ pequeño), y casi nada que dos no vecinos queden cerca. Y la t de Student
resuelve el problema de **apiñamiento** (*crowding*): en 2D no cabe la misma cantidad de
puntos "medianamente lejanos" que en 64D; con colas pesadas, alejar mucho lo no vecino es
barato (a distancia 3, la t vale 9 veces más que la gaussiana) y los grupos se separan.

### Qué conserva y qué no

Medido en `04-reduccion-dimensionalidad-aplicado.ipynb`:

| Propiedad | Resultado |
|---|---|
| Vecindarios | Sí: *trustworthiness* 0.99 sobre los dígitos; un KNN sobre las 2 coordenadas clasifica con 0.97 (0.96 en 64D; PCA 2D: 0.60) |
| Perplejidad e inicialización | Cambian la apariencia (fragmentación, disposición), no los vecindarios (KNN 0.96–0.98 en todas las configuraciones) |
| Tamaño de los grupos | **No**: un grupo 5× más disperso en los datos aparece del mismo tamaño en el mapa (la perplejidad normaliza la densidad) |
| Distancia entre grupos | **No**: un grupo 3× más lejano aparece a la misma distancia; nada en el costo la optimiza |
| Existencia de grupos | **No garantizada**: una sola gaussiana en 10D da un mapa con grumos, y K-Means sobre ese mapa tiene silueta 0.35–0.38 (0.08 en los datos) |

Las consecuencias prácticas: un mapa t-SNE se lee como "estos puntos son vecinos de estos",
y nada más. El tamaño, la forma y la posición relativa de los grupos no significan nada;
dos corridas dan dos mapas distintos igual de válidos; y cualquier grupo que aparezca hay
que verificarlo en el espacio original (referencia nula, `02-validacion-clusters.md`).
Clusterizar el mapa funciona cuando los grupos existen (dígitos: K-Means sobre el mapa
da ARI 0.89 contra 0.67 en 64D) y fabrica estructura cuando no.

Dos límites más: t-SNE no tiene `transform` —solo puede mapear los puntos con los que se
ajustó, así que no entra en un `Pipeline`— y su costo es $O(n \log n)$ con la aproximación
de Barnes-Hut, pero con una constante alta (segundos para miles de puntos, minutos para
cientos de miles). Con $p$ grande conviene reducir antes a ~50 componentes con PCA.

## 4. 🔵 UMAP

*Uniform Manifold Approximation and Projection* (McInnes, Healy y Melville, 2018)
construye un grafo de $k$ vecinos arriba con pesos que, como en t-SNE, normalizan la
densidad local, y optimiza una disposición abajo minimizando una entropía cruzada entre
los dos grafos. Los mapas se parecen a los de t-SNE; las diferencias que importan:

- Conserva algo más de **estructura global** (grupos lejanos arriba tienden a quedar
  lejos abajo), aunque tampoco hay que leer distancias.
- Tiene **`transform`**: puede colocar puntos nuevos en un mapa ajustado. Un KNN entrenado
  sobre el mapa UMAP de entrenamiento clasifica dígitos de prueba, colocados con
  `transform`, con accuracy 0.98. Es lo que lo hace usable dentro de un flujo de modelado.
- **Escala mejor** con muchos datos (con pocos es más lento por la compilación de `numba`:
  8 s frente a 1 s de t-SNE sobre 1797 dígitos).
- Sus hiperparámetros (`n_neighbors`, `min_dist`) tienen el mismo papel que la perplejidad:
  cambian la apariencia, no los vecindarios.

Sus advertencias son las mismas que las de t-SNE: tamaños, distancias y grumos no se
interpretan.

## 5. Cuál usar

| Para… | Método |
|---|---|
| Comprimir, eliminar redundancia, filtrar ruido, preprocesar un modelo | PCA (validando con la métrica del modelo) |
| Visualizar la estructura global | PCA (2 componentes) |
| Visualizar vecindarios y grupos finos | t-SNE (o UMAP); verificar los grupos en el espacio original |
| Un mapa 2D que reciba puntos nuevos | UMAP |
| Predecir | Ninguno de los tres como sustituto de las variables: sobre Wine Quality, un KNN pierde AP de 0.38 en 11D a 0.28–0.36 en cualquier mapa 2D |

## Referencias

- Jolliffe, I. (2002). *Principal Component Analysis*, 2.ª ed. Springer.
- van der Maaten, L. y Hinton, G. (2008). Visualizing data using t-SNE. *JMLR*.
- Wattenberg, M., Viégas, F. y Johnson, I. (2016). How to use t-SNE effectively. *Distill*.
- McInnes, L., Healy, J. y Melville, J. (2018). UMAP: Uniform Manifold Approximation and
  Projection for dimension reduction. *arXiv:1802.03426*.
- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning*,
  cap. 14.5.

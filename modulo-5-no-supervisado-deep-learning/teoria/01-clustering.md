# 01 · Clustering: K-Means, jerárquico y DBSCAN

**Módulo 5 · Sesión 12** — Aprendizaje no supervisado

## Objetivos

- Entender qué cambia cuando no hay $y$: qué optimiza cada algoritmo y por qué "funciona"
  deja de tener una definición única.
- Conocer los tres algoritmos de clustering de la sesión —K-Means, jerárquico aglomerativo
  y DBSCAN— como tres **definiciones distintas de grupo**, con sus supuestos y sus modos
  de fallo.
- Saber qué preprocesamiento exigen (estandarizar, duplicados, atípicos) y qué
  hiperparámetros decide cada uno.

## 1. Aprender sin etiquetas

Todos los modelos de los módulos 3 y 4 tenían una variable objetivo que definía el error.
En el **aprendizaje no supervisado** solo hay $\mathbf{X} \in \mathbb{R}^{n \times p}$, y
la tarea es encontrar **estructura**: grupos de observaciones parecidas (clustering),
direcciones que resuman las variables (reducción de dimensionalidad,
`03-reduccion-dimensionalidad.md`), u observaciones que no se parecen a nada (detección de
anomalías).

Dos consecuencias que atraviesan toda la sesión:

1. **No hay una respuesta correcta que verificar.** Cada algoritmo optimiza un criterio
   propio, y su resultado es la mejor partición *según ese criterio*. Si el criterio no
   corresponde a la forma de los datos, el algoritmo devuelve una partición igual de
   convencido (`01-clustering-intuicion.ipynb`, sección 4). Validar exige criterios
   externos al algoritmo (`02-validacion-clusters.md`).
2. **El clustering encuentra la estructura dominante, no la que interesa.** Sobre Wine
   Quality, K-Means recupera tinto/blanco con ARI 0.93 sin haber visto la columna `tipo`,
   y no dice nada de la calidad con ningún $k$ (NMI $\leq 0.07$;
   `02-clustering-aplicado.ipynb`, sección 3). Clustering no es "clasificación sin
   etiquetas": si hay una $y$ que predecir, hay que etiquetar.

Qué se puede hacer con un clustering, cuando funciona: segmentar (clientes, productos,
regiones) para tratar cada grupo distinto; resumir un dataset grande por sus centroides;
crear una variable "grupo" para un modelo supervisado; y detectar lo que no encaja en
ningún grupo.

## 2. K-Means

### El criterio

Dados $k$ centroides $\boldsymbol{\mu}_1, \dots, \boldsymbol{\mu}_k \in \mathbb{R}^p$, cada
punto se asigna al más cercano y la calidad de la partición es la **inercia** (suma de
cuadrados intra-grupo):

$$
J(\boldsymbol{\mu}_1, \dots, \boldsymbol{\mu}_k) = \sum_{i=1}^{n} \min_{j} \lVert \mathbf{x}_i - \boldsymbol{\mu}_j \rVert^2
$$

Minimizar $J$ de forma exacta es NP-difícil. El **algoritmo de Lloyd** (1957) alterna dos
pasos, cada uno óptimo dado el otro:

1. **Asignación**: fijos los centroides, cada punto va al más cercano.
2. **Actualización**: fijas las asignaciones, cada centroide pasa a ser la **media** de sus
   puntos — la media es el punto que minimiza la suma de distancias al cuadrado (S6).

Ninguno de los dos pasos puede aumentar $J$, así que el algoritmo converge en un número
finito de iteraciones (en `01-clustering-intuicion.ipynb`, 4 sobre cuatro grupos
gaussianos; en Wine Quality, 8–9). Converge a un **mínimo local**: el resultado
depende de dónde empiece.

### Inicialización

Con $k$ puntos al azar como centroides iniciales, el 30 % de las corridas del notebook 01
termina en un mínimo local claramente peor: dos centroides repartiéndose un mismo grupo y
otro cubriendo dos. Dos remedios que se usan juntos:

- **K-Means++** (Arthur y Vassilvitskii, 2007): el primer centroide al azar; cada siguiente
  se elige entre los puntos con probabilidad proporcional a $D(\mathbf{x})^2$, su distancia
  al cuadrado al centroide más cercano ya elegido. Tiende a poner un centroide por grupo y
  garantiza que la inercia esperada está a un factor $O(\log k)$ del óptimo. Reduce los
  mínimos locales del 30 % al 10 % en el notebook 01.
- **Varias corridas** (`n_init`): repetir con distintas semillas y quedarse con la de menor
  inercia. Con K-Means++ y `n_init=10`, en la práctica se alcanza el óptimo siempre.

### Supuestos

La asignación al centroide más cercano divide el espacio en **celdas de Voronoi**:
regiones convexas separadas por hiperplanos. Y la inercia, por ser una suma de cuadrados,
premia grupos **esféricos** y de **varianza y tamaño parecidos**. Cuando eso no se cumple,
K-Means minimiza la inercia igual de bien y la partición no se parece a los grupos
(notebook 01, sección 4, con $k$ correcto en todos):

| Datos | ARI de K-Means |
|---|---|
| Grupos esféricos del mismo tamaño | 1.00 |
| Grupos alargados uno junto a otro | 0.30 |
| Un grupo 6× más disperso que los otros | 0.73 |
| Un grupo 10× más grande que los otros | 0.29 |
| Dos medias lunas | 0.24 |

En 2D se ve; en 11 dimensiones hay que sospecharlo a partir de los diagnósticos de
`02-validacion-clusters.md`.

### Preprocesamiento y costo

- **Estandarizar es obligatorio.** La inercia es euclídea; sin estandarizar, la variable con
  más varianza domina. En Wine Quality, `total_sulfur_dioxide` tiene varianza 3223 y
  `density` 0.00001; sin estandarizar, el ARI contra `tipo` cae de 0.93 a 0.31.
- **Duplicados**: cada copia cuenta, así que un grupo de duplicados atrae su centroide. Las
  1177 filas idénticas de Wine Quality se quitan, como en el módulo 4.
- **Atípicos**: un punto muy lejano mueve la media de su grupo. K-Means no tiene noción de
  ruido; DBSCAN sí.
- Costo $O(n \cdot k \cdot p)$ por iteración: escala a millones de filas (`MiniBatchKMeans`
  para más). Es el algoritmo por defecto por eso, no porque sus supuestos sean razonables.

## 3. Clustering jerárquico aglomerativo

Otra definición de grupo: una **jerarquía** de fusiones. Se parte de $n$ grupos de un punto
y en cada paso se fusionan los dos grupos más cercanos, hasta que queda uno. El resultado
es un **dendrograma**: un árbol donde cada fusión está a la altura de la distancia a la que
ocurrió. Cortarlo a una altura da una partición; no hay que fijar $k$ antes de mirar.

Lo único que hay que definir es la distancia **entre grupos**, el *linkage*:

| Linkage | $d(A, B)$ | Tiende a | Problema típico |
|---|---|---|---|
| *single* | $\min_{a \in A, b \in B} d(a, b)$ | seguir formas alargadas o curvas (separa las medias lunas: ARI 1.0) | **encadenamiento**: un puente de ruido une dos grupos; aísla atípicos |
| *complete* | $\max_{a \in A, b \in B} d(a, b)$ | grupos compactos de diámetro parecido | rompe grupos grandes; aísla atípicos |
| *average* | media de $d(a, b)$ sobre todos los pares | compromiso entre los dos | aísla atípicos |
| *Ward* | aumento de inercia al fusionar $A \cup B$ | grupos esféricos de tamaño parecido | los mismos supuestos que K-Means |

Ward es el K-Means jerárquico: sobre Wine Quality llega a casi la misma partición
(ARI 0.90 con K-Means, `02-clustering-aplicado.ipynb`, sección 5). Los otros tres, sobre
los mismos datos, cortan **un solo vino** y dejan los 5319 restantes juntos: el punto más
lejano se fusiona el último con cualquier criterio basado en distancias entre puntos. Con
datos reales, que siempre tienen atípicos, *single*, *complete* y *average* exigen limpiar
antes o cortar mucho más abajo.

Costo: $O(n^2)$ de memoria (la matriz de distancias; 5320 filas son 226 MB) y $O(n^2 \log n)$
de tiempo. No escala a cientos de miles de filas; a cambio, da la jerarquía completa y el
dendrograma, que es una herramienta de exploración que K-Means no ofrece. La
implementación directa de `01-clustering-intuicion.ipynb` (sección 5), $O(n^3)$, reproduce
exactamente las alturas de fusión de `scipy.cluster.hierarchy.linkage`.

## 4. DBSCAN

Tercera definición: un grupo es una **región densa** separada de otras por regiones poco
densas (Ester et al., 1996). Dos parámetros, un radio $\varepsilon$ (`eps`) y un mínimo de
puntos $m$ (`min_samples`), y tres tipos de punto:

- **núcleo**: tiene al menos $m$ puntos (contándose) a distancia $\leq \varepsilon$;
- **borde**: no es núcleo, pero está a distancia $\leq \varepsilon$ de uno;
- **ruido**: ninguna de las dos.

Los grupos son las componentes conexas del grafo de núcleos (dos núcleos a distancia
$\leq \varepsilon$ están conectados); los bordes se adhieren al grupo de un núcleo vecino;
el ruido queda con etiqueta $-1$. Tres propiedades que K-Means y Ward no tienen:

- Encuentra grupos de **cualquier forma** (las medias lunas: ARI 0.99).
- **No pide $k$**: el número de grupos sale de la densidad.
- Tiene una noción explícita de **ruido**: puntos que no pertenecen a ningún grupo. Por
  eso es también un detector de anomalías.

Y sus límites:

- $\varepsilon$ **decide todo** y no tiene un valor razonable a priori (depende de la escala:
  estandarizar, otra vez). La heurística estándar es el **gráfico de k-distancias**: la
  distancia de cada punto a su $m$-ésimo vecino, ordenada de mayor a menor; el codo sugiere
  $\varepsilon$. En 2D el codo es claro; en 11 dimensiones no lo hay.
- Supone una **densidad uniforme**: un $\varepsilon$ que separa dos grupos densos funde
  dos grupos dispersos, o los declara ruido.
- En **alta dimensión** las distancias se concentran (la distancia al vecino más cercano y
  al más lejano se parecen cada vez más) y no hay ventana de $\varepsilon$ que separe
  "denso" de "vacío". Sobre las 11 variables de Wine Quality, DBSCAN solo separa
  tinto/blanco entre los vinos que no declara ruido (ARI 0.98 con $\varepsilon = 1.25$), a
  costa de dejar fuera a un tercio; con $\varepsilon = 1.5$ los dos núcleos ya se tocan.
  Lo que sí hace bien en 11-D es señalar los 191 vinos (3.6 %) que no tienen 10 vecinos a
  distancia 2: todos con alguna variable extrema (`02-clustering-aplicado.ipynb`,
  sección 6).

Costo $O(n \log n)$ con un índice espacial, $O(n^2)$ sin él. Escala mejor que el jerárquico
y peor que K-Means.

## 5. Cuál usar

| Situación | Algoritmo |
|---|---|
| Muchos datos, grupos aproximadamente convexos, se sabe más o menos $k$ | K-Means (K-Means++, `n_init` ≥ 10) |
| Pocos datos ($n < 10^4$), se quiere explorar la jerarquía y decidir $k$ mirando | Jerárquico con Ward (o *average* tras quitar atípicos) |
| Grupos de forma arbitraria, densidad parecida, ruido que conviene aislar | DBSCAN (o HDBSCAN, que relaja el supuesto de densidad uniforme) |
| Detectar observaciones raras | DBSCAN como filtro de ruido; Isolation Forest (🔵, `02-clustering-aplicado.ipynb`) |

Y en todos los casos: **estandarizar**, quitar duplicados, sospechar de los atípicos, y
validar con `02-validacion-clusters.md` antes de interpretar nada.

## Referencias

- Lloyd, S. (1982). Least squares quantization in PCM. *IEEE Trans. Information Theory*.
- Arthur, D. y Vassilvitskii, S. (2007). k-means++: the advantages of careful seeding. *SODA*.
- Ester, M., Kriegel, H.-P., Sander, J. y Xu, X. (1996). A density-based algorithm for
  discovering clusters in large spatial databases with noise. *KDD*.
- Hastie, T., Tibshirani, R. y Friedman, J. (2009). *The Elements of Statistical Learning*,
  cap. 14.3.

# 02 · Validar un clustering: cuántos grupos, y si existen

**Módulo 5 · Sesión 12** — Aprendizaje no supervisado

## Objetivos

- Conocer los criterios internos para elegir $k$ —codo, silueta, Davies-Bouldin— y qué
  mide cada uno.
- Entender por qué **todos proponen un $k$ aunque no haya grupos**, y cómo comprobar que
  la estructura encontrada es real (referencia nula, estabilidad).
- Saber validar *a posteriori* con etiquetas externas (ARI, NMI) e **interpretar** los
  grupos en unidades originales.

## 1. El problema

Sin $y$ no hay error de prueba. La inercia de K-Means baja siempre al subir $k$ (con
$k = n$ vale cero), así que no sirve para elegir $k$ por sí sola; y cualquier criterio que
compare particiones entre sí elige una ganadora aunque los datos sean ruido uniforme. Hay
que separar tres preguntas que suelen mezclarse:

1. Dado que hay grupos, ¿cuántos? — criterios **internos** (§2).
2. ¿**Hay** grupos? — referencia nula y estabilidad (§3).
3. ¿Los grupos son los que **interesan**? — validación **externa** e interpretación (§4).

## 2. Criterios internos

Todos se calculan solo con $\mathbf{X}$ y la partición. Con $C_j$ el grupo $j$,
$\boldsymbol{\mu}_j$ su centroide y $n_j$ su tamaño:

### Método del codo

Graficar la inercia $J(k)$ y buscar el punto donde deja de bajar "mucho". Si hay $k^*$
grupos bien separados, $J$ cae bruscamente hasta $k^*$ y poco después. En datos sintéticos
con cuatro grupos el codo está en 4 sin ambigüedad (`01-clustering-intuicion.ipynb`,
sección 7); en Wine Quality no hay codo, solo una curva que se aplana poco a poco
(`02-clustering-aplicado.ipynb`, sección 2). Es un criterio visual y subjetivo, útil como
primera mirada.

### Coeficiente de silueta

Para cada punto $i$ (Rousseeuw, 1987), con $a_i$ la distancia media a los puntos de **su**
grupo y $b_i$ la distancia media al grupo **vecino** más cercano (el que minimiza esa
media):

$$
s_i = \frac{b_i - a_i}{\max(a_i, b_i)} \in [-1, 1]
$$

$s_i \approx 1$: mucho más cerca de su grupo que del vecino. $s_i \approx 0$: en la frontera.
$s_i < 0$: probablemente mal asignado. La **silueta media** $\bar{s}$ resume la partición
y se elige el $k$ que la maximiza. Dos ventajas sobre el codo: da un máximo, no un quiebre
que interpretar, y el valor **absoluto** informa. La escala orientativa de Kaufman y
Rousseeuw (1990):

| $\bar{s}$ | Lectura |
|---|---|
| $> 0.70$ | estructura fuerte |
| $0.50 - 0.70$ | estructura razonable |
| $0.25 - 0.50$ | estructura débil, puede ser artificial |
| $< 0.25$ | sin estructura sustancial |

Cuatro grupos gaussianos: 0.77. Wine Quality con $k=2$: 0.27 — grupos que se tocan. Y su
límite: mide compacidad y separación **euclídeas**, así que hereda los supuestos de
K-Means. Sobre las medias lunas, la partición correcta de DBSCAN tiene silueta $-0.02$ y la
incorrecta de K-Means, 0.49. Costo $O(n^2)$: sobre datasets grandes se calcula sobre una
muestra (`sample_size`).

### Índice de Davies-Bouldin

Con $\sigma_j$ la distancia media de los puntos de $C_j$ a su centroide (dispersión) y
$d_{jl} = \lVert \boldsymbol{\mu}_j - \boldsymbol{\mu}_l \rVert$:

$$
DB = \frac{1}{k} \sum_{j=1}^{k} \max_{l \neq j} \frac{\sigma_j + \sigma_l}{d_{jl}}
$$

Para cada grupo, el peor cociente "dispersión sobre separación" con otro grupo; se
promedia; **menor es mejor**. Es más barato que la silueta ($O(n \cdot k)$) y mide algo
parecido pero a nivel de centroides, no de puntos. Por eso puede discrepar: en Wine
Quality, la silueta prefiere $k=2$ (0.27 frente a 0.24 en $k=4$) y Davies-Bouldin prefiere
$k=4$ (1.48 frente a 1.63). Ninguno está "equivocado": los $k=4$ son la jerarquía
tinto / blanco seco / blanco dulce aplanada, y ambos son resúmenes razonables de los
mismos datos a distinta resolución.

### Otros

Calinski-Harabasz (cociente entre dispersión entre grupos e intra grupo, ponderado por
$n - k$ y $k - 1$; mayor es mejor) y el criterio BIC de un modelo de mezcla gaussiana
(`GaussianMixture`, que es K-Means con covarianzas y probabilidades de pertenencia). En
la práctica se miran dos o tres y se reporta el desacuerdo, no se elige el que dé la
respuesta que uno quería.

## 3. ¿Hay grupos?

### Referencia nula

Lo más importante de la sesión, y lo que casi nunca se hace. Sobre puntos **uniformes** en
un cuadrado, la silueta de K-Means tiene un máximo en $k = 4$ con valor 0.41
(`01-clustering-intuicion.ipynb`, sección 7): un valor que, leído solo, sugeriría
"estructura débil". No hay ninguna. Los criterios internos comparan particiones entre sí;
no comprueban que exista algo que particionar.

La solución es construir datos **sin grupos por construcción** que se parezcan a los
reales en todo lo demás, y comparar. Dos referencias habituales:

- **Columnas permutadas**: cada variable se permuta de forma independiente. Conserva la
  distribución marginal de cada una y destruye toda relación entre ellas. Es la que usa
  `02-clustering-aplicado.ipynb`: la silueta de Wine Quality (0.27) casi triplica la de la
  referencia (0.10) → hay estructura.
- **Uniforme en la caja** de los datos (o en la caja de los componentes principales, para
  respetar la forma): es la referencia del **estadístico de brecha** (*gap statistic*,
  Tibshirani et al., 2001), que compara $\log J(k)$ real contra el esperado bajo la
  referencia y elige el $k$ con mayor brecha.

Con cualquiera de las dos, la pregunta pasa de "¿qué $k$?" a "¿la partición real se separa
de lo que K-Means impone a datos sin grupos?". Si no se separa, no hay clustering que
reportar.

### Estabilidad

Si los grupos son reales, deben reaparecer con otros datos. El diagnóstico más barato:
submuestrear el 50 % varias veces, agrupar cada submuestra, y medir el acuerdo (ARI, §4)
con la partición del conjunto completo restringida a la submuestra. En Wine Quality
(`02-clustering-aplicado.ipynb`, sección 7), $k = 2$, 3 y 4 dan ARI $> 0.97$; a partir de
$k = 5$ cae (0.93, 0.89, 0.79): las particiones adicionales dependen de qué vinos entran,
la firma de estar cortando un continuo por donde caiga. Es el "detectable frente a ruido"
del módulo 3, sin $y$.

## 4. Validación externa e interpretación

### Contra etiquetas que el algoritmo no vio

Cuando existe una etiqueta —que no se usó para agrupar—, se mide el acuerdo entre la
partición y la etiqueta. Dos medidas invariantes al **nombre** de los grupos (el grupo
"0" de K-Means puede ser cualquiera):

- **Índice de Rand ajustado** (ARI): fracción de pares de puntos en los que las dos
  particiones coinciden (juntos en ambas o separados en ambas), corregida por lo que daría
  el azar. 1 = idénticas; 0 = azar; puede ser negativo.
- **Información mutua normalizada** (NMI): cuánta información da una partición sobre la
  otra, en $[0, 1]$. Menos sensible que el ARI al número de grupos.

Sirve para dos cosas: comprobar que un algoritmo recupera grupos conocidos (Wine
Quality: ARI 0.93 contra `tipo`), y descubrir que **no** recupera la etiqueta que
interesa (NMI 0.01–0.07 contra `quality`). Lo segundo es la lección: la validación externa
no dice si el clustering es bueno, dice **qué** encontró.

### Interpretar

Un grupo no se interpreta por sus centroides estandarizados sino por su **perfil en
unidades originales**: la media (o mediana) de cada variable en el grupo comparada con la
global, o el cociente entre grupos. En Wine Quality, el grupo 1 de $k = 2$ tiene el doble
de acidez volátil y cloruros y un tercio del dióxido de azufre: es un tinto. Y luego se
vuelve a preguntar si esa estructura era la de interés: aquí, el clustering descubrió lo
que ya decía una columna, y la calidad —lo que importaba— no aparece. Es un resultado
honesto y frecuente.

Tres preguntas al interpretar cualquier grupo:

1. ¿Qué variables lo distinguen? (perfil)
2. ¿Corresponde a algo conocido? (validación externa, conocimiento del dominio)
3. ¿Es estable y se separa de la referencia nula? (§3)

Si la respuesta a la 3 es no, las dos primeras no importan.

## 5. Protocolo

1. Quitar duplicados y decidir qué hacer con los atípicos. Estandarizar.
2. Correr K-Means para $k = 2, \dots, 10$ con K-Means++ y `n_init` ≥ 10. Codo, silueta,
   Davies-Bouldin. Reportar los desacuerdos.
3. Referencia nula: ¿la silueta real se separa? Si no, parar aquí.
4. Estabilidad por submuestreo para los $k$ candidatos.
5. Perfil en unidades originales; validación externa si hay etiquetas.
6. Si hay una jerarquía (grupo dominante que aplasta el resto), repetir dentro de cada
   grupo (Wine Quality: dulces/secos dentro de los blancos).
7. Comparar con otro algoritmo (Ward, DBSCAN). Si coinciden, más confianza; si no, la
   discrepancia es información sobre la forma de los grupos.

## Referencias

- Rousseeuw, P. (1987). Silhouettes: a graphical aid to the interpretation and validation
  of cluster analysis. *J. Computational and Applied Mathematics*.
- Kaufman, L. y Rousseeuw, P. (1990). *Finding Groups in Data*. Wiley.
- Davies, D. y Bouldin, D. (1979). A cluster separation measure. *IEEE TPAMI*.
- Tibshirani, R., Walther, G. y Hastie, T. (2001). Estimating the number of clusters in a
  data set via the gap statistic. *JRSS B*.
- Hubert, L. y Arabie, P. (1985). Comparing partitions. *J. Classification* (ARI).

# Ejercicio 02 · PCA, clustering y t-SNE sobre los dígitos

**Módulo 5 · Sesión 12** · Tiempo estimado: **60 min** · Con código

> **Objetivo.** Usar PCA como preprocesamiento **validado por la métrica de un modelo**
> (no por la varianza explicada), agrupar los dígitos sin etiquetas y medir qué recupera
> K-Means, y comprobar sobre un caso concreto —los dígitos "1"— si los grupos que dibuja
> t-SNE existen en el espacio original.

## Contexto

`load_digits` de `scikit-learn`: 1797 imágenes de 8 × 8 (64 píxeles con valores 0–16),
etiqueta `target` (0–9). Los notebooks 03 y 04 ya usaron estos datos; aquí se hacen
preguntas que ellos no hicieron.

```python
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
```

Semilla 42; CV estratificada de 5 pliegues donde haga falta. Entrega un notebook
`ej02-<tu-apellido>.ipynb`.

## Parte A — PCA validado por el modelo (20 min)

**A.1** Ajusta un PCA completo sobre los 64 píxeles (sin estandarizar: todos están en la
misma escala, 0–16; explica por qué en este caso **no** conviene estandarizar, mirando la
varianza mínima y máxima por píxel). Reporta la varianza acumulada con 2, 5, 10, 20 y 30
componentes, el número de componentes para llegar al 90 %, y cuántos superan el autovalor
medio (la regla de Kaiser para datos sin estandarizar).

**A.2** Para $q \in \{2, 5, 10, 20, 30, 64\}$, evalúa en CV un `Pipeline` de
`PCA(n_components=q)` + `KNeighborsClassifier(5)`. Grafica accuracy contra $q$ y
superpón la varianza acumulada. ¿A partir de qué $q$ la accuracy deja de mejorar? ¿Coincide
con el 90 % de varianza? ¿Qué regla usarías para elegir $q$ aquí?

**A.3** En Wine Quality (notebook 03, sección 5.3) reducir componentes **bajaba** la AP de
la regresión logística. Aquí con 20 componentes el KNN iguala al de 64. ¿Qué tienen los
dígitos que Wine Quality no, que hace que PCA funcione como preprocesamiento? Piensa en
la correlación entre variables y en dónde vive la información sobre la clase.

## Parte B — Agrupar dígitos sin etiquetas (25 min)

**B.1** K-Means sobre los 64 píxeles para $k \in \{5, 8, 10, 12, 15\}$, con la silueta de los
datos y la de una referencia nula (píxeles permutados). ¿Propone la silueta $k = 10$? ¿Se
separa de la referencia?

**B.2** Con $k = 10$, tabla cruzada entre el dígito real y el grupo, y la **pureza**
(fracción de imágenes en el dígito mayoritario de su grupo). ¿Qué dígitos se recuperan
limpios? ¿Cuáles se mezclan entre sí, y cuál queda repartido en dos grupos? Mira las
imágenes de un grupo mezclado y propón una explicación.

**B.3** Repite K-Means ($k = 10$) sobre (a) las 10 primeras componentes de PCA y (b) las dos
coordenadas de un t-SNE (`init="pca"`, perplejidad 30). ARI contra el dígito real en los
tres casos (64D, PCA-10, t-SNE-2). Para la partición obtenida sobre t-SNE, calcula su
silueta **en el mapa** y **en los 64 píxeles originales**. Explica la diferencia entre
esas dos siluetas.

## Parte C — ¿Los grupos del mapa existen? (15 min)

**C.1** Toma solo las imágenes del dígito **1** (182). Ajusta t-SNE (perplejidad 30) y
grafica el mapa. ¿Ves grupos?

**C.2** Para $k \in \{2, 3, 4\}$: K-Means sobre el mapa, y silueta de esa partición (i) en el
mapa y (ii) en los 64 píxeles. Y como control: (iii) silueta de K-Means aplicado
directamente en 64D, y (iv) silueta de K-Means sobre la referencia nula (píxeles del "1"
permutados).

**C.3** Con esos cuatro números, responde: ¿los grupos que dibuja t-SNE entre los "1"
existen en los datos, o los fabricó el mapa? ¿Qué distingue a los subgrupos? (Muestra
algunas imágenes de cada uno.)

## Entrega

Notebook, y una tabla de una fila por método (PCA, K-Means, t-SNE) con dos columnas:
"para qué lo usaría" y "qué no le pediría".

# Ejercicio 01 · ¿Hay grupos dentro de los tintos?

**Módulo 5 · Sesión 12** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Repetir el flujo completo de `02-clustering-aplicado.ipynb` sobre un
> subconjunto que el notebook **no** analizó —los 1359 vinos tintos— y llegar a una
> conclusión defendible sobre si tienen estructura de grupos, cuál es, y si dice algo de
> la calidad. Los blancos tenían un segundo nivel claro (dulces/secos); los tintos no
> tienen por qué.

## Contexto

`../datos/wine-quality.csv`, sin duplicados, solo `tipo == "tinto"`. Las 11 variables
fisicoquímicas son la entrada; `quality` queda apartada para validar al final.

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score
from sklearn.preprocessing import StandardScaler
```

Semilla 42 en todo. Entrega un notebook `ej01-<tu-apellido>.ipynb` que corra de principio
a fin.

## Parte A — Preparación (10 min)

**A.1** Carga, quita duplicados, filtra los tintos. Reporta cuántos son y qué fracción
tiene `quality ≥ 7`.

**A.2** Ejecuta K-Means con $k = 3$ **sin estandarizar** y calcula la media de
`total_sulfur_dioxide` en cada grupo. ¿Qué encontró K-Means? Estandariza y sigue con
`X_esc` en el resto del ejercicio.

## Parte B — ¿Cuántos grupos, y hay grupos? (20 min)

**B.1** Para $k = 2, \dots, 8$ (K-Means++, `n_init=10`): inercia, silueta media e índice de
Davies-Bouldin. Grafica las tres curvas. ¿Coinciden en un $k$?

**B.2** Construye la **referencia nula** permutando cada columna de `X_esc` de forma
independiente, y calcula la silueta de K-Means sobre ella para los mismos $k$. Añádela a la
gráfica de la silueta. ¿La estructura de los tintos se separa de la referencia? ¿Cómo la
clasificarías en la escala de Kaufman y Rousseeuw?

**B.3** Compara con los blancos (`02-clustering-aplicado.ipynb`, sección 4: silueta 0.21 en
$k=2$ frente a 0.08 de la referencia). ¿Los tintos tienen más o menos estructura que los
blancos?

## Parte C — Interpretar (20 min)

**C.1** Con $k = 2$, calcula el perfil de cada grupo en **unidades originales** (media por
variable) y el cociente entre grupos. Describe cada grupo en una frase, en términos de
vino, no de números.

**C.2** Repite con $k = 3$. ¿El tercer grupo es una subdivisión de uno de los dos anteriores
o una estructura nueva? Usa `pd.crosstab` entre las dos particiones.

**C.3** Para $k = 2$ y $k = 3$: calidad media y fracción de vinos buenos por grupo, e
información mutua normalizada (NMI) con `quality`. ¿Los grupos dicen algo de la calidad?
Compara con lo que encontró el notebook 02 sobre el conjunto completo (NMI $\leq 0.07$).

## Parte D — Estabilidad y otro algoritmo (15 min)

**D.1** Estabilidad por submuestreo (función `estabilidad` del notebook 02, sección 7)
para $k = 2, \dots, 6$. ¿Qué $k$ son estables? Compara con los valores del conjunto
completo (ARI $> 0.97$ para $k \leq 4$).

**D.2** Clustering jerárquico con Ward y con *average*, $k = 2$. Tamaños de los grupos y
ARI contra la partición de K-Means. En el conjunto completo Ward coincidía con K-Means
(ARI 0.90). ¿Aquí? ¿Qué te dice sobre la forma de la estructura?

## Parte E — Anomalías (10 min)

**E.1** Gráfico de k-distancias con `min_samples=10` y barrido de `eps` en
$\{1.5, 2, 2.5, 3\}$: número de grupos y % de ruido.

**E.2** Con `eps = 2`: cuántos tintos son ruido, mediana del $|z|$ máximo por vino en el
ruido y en el resto, y en cuántas de las 11 variables el máximo global cae entre los
vinos-ruido. ¿Los tintos anómalos son mejores o peores que el resto?

**E.3** *(opcional 🔵)* Isolation Forest con la misma fracción de contaminación: cuántos
coinciden con DBSCAN (índice de Jaccard).

## Entrega

Además del notebook, un párrafo final (5–8 líneas) que responda: ¿hay grupos dentro de los
tintos? ¿Qué son? ¿Se lo recomendarías a alguien que quiera predecir la calidad?

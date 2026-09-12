# Solución · Ejercicio 02 · PCA, clustering y t-SNE sobre los dígitos

> **Material del docente.** Números con `random_state=42` (K-Means, t-SNE con
> `init="pca"`, permutaciones). t-SNE con otra semilla cambia el dibujo, no los ARI ni las
> siluetas a la segunda cifra.

## Parte A — PCA validado por el modelo

**A.1** Los píxeles ya están en la misma escala (0–16) y sus varianzas **son**
informativas: tres píxeles de las esquinas tienen varianza 0 (siempre son fondo) y el
máximo es 42.7. Estandarizar los inflaría a varianza 1 (o dividiría por cero) y daría al
fondo el mismo peso que a los trazos. Sin estandarizar:

| $q$ | 2 | 5 | 10 | 20 | 30 | 64 |
|---|---|---|---|---|---|---|
| Varianza acumulada | 0.285 | 0.545 | 0.738 | 0.894 | 0.959 | 1.0 |

Para el 90 % hacen falta **21** componentes; **14** superan el autovalor medio.

**A.2**

| $q$ | 2 | 5 | 10 | 20 | 30 | 64 |
|---|---|---|---|---|---|---|
| Accuracy KNN (CV) | 0.622 | 0.919 | 0.978 | **0.987** | 0.987 | 0.987 |

La accuracy deja de mejorar en $q = 20$ (el 89 % de la varianza): coincide, por una vez,
con la regla del 90 %, pero eso es una coincidencia que hay que comprobar, no una regla.
Con 10 componentes (74 %) ya se pierde menos de un punto. La regla correcta es la que se
acaba de usar: **la métrica del modelo contra $q$**, en CV, con el PCA dentro del
`Pipeline`.

**A.3** Dos razones. (1) Los píxeles están **muy correlacionados** (los trazos son
continuos; notebook 03, sección 4), así que las direcciones de poca varianza son ruido
píxel a píxel: descartarlas no quita información y a veces la limpia. En Wine Quality
las 11 variables están poco correlacionadas entre sí y cada componente menor aún lleva
señal. (2) La información sobre **la clase** vive, en los dígitos, en la forma global del
trazo, que es de gran varianza (es lo que distingue un 0 de un 1); en Wine, la calidad
vive en combinaciones sutiles que PCA no ve (notebook 03, sección 5). Ninguna de las dos
cosas se sabe a priori: se mide.

## Parte B — Agrupar dígitos sin etiquetas

**B.1**

| $k$ | Silueta | Silueta (nulo) | ARI con el dígito |
|---|---|---|---|
| 5 | 0.136 | 0.023 | 0.358 |
| 8 | 0.179 | 0.023 | 0.578 |
| 10 | 0.182 | 0.023 | 0.667 |
| 12 | 0.183 | 0.022 | **0.714** |
| 15 | 0.186 | 0.023 | 0.695 |

La silueta se separa mucho de la referencia (8×: hay estructura) pero **no propone
$k = 10$**: es casi plana de 10 a 15 y máxima en 15. En 64 dimensiones, con clases que
se solapan (los "1" tienen varias formas, C), la silueta no distingue entre 10 y 15
grupos. Que el ARI sea máximo en 12 sugiere lo mismo: algunos dígitos son dos grupos
naturales.

**B.2** Pureza 0.794. Tabla cruzada (filas: dígito real; columnas: grupo), resumida:

| Se recuperan limpios | Se mezclan | Se parten |
|---|---|---|
| 0 (177/178), 6 (177/181), 4 (166/181), 7 (170/179), 2 (148/177), 3 (155/183) | **1 y 8** en un mismo grupo (99 + 102); **5 y 8** (137 + 41); **9 y 8** (139 + 48); 9 y 1 (20 + 55) | el **1** en tres grupos (99, 55, 24) |

El 8 es el dígito problemático: no tiene grupo propio y se reparte entre los del 1, el 5
y el 9, porque su trazo se parece a todos (dos lazos que, aplastados en 8 × 8, se
confunden con un 1 grueso, un 5 o un 9). Y el 1 se escribe de varias formas (C.3), así que
K-Means le da varios grupos. La pureza de 0.79 con $k = 10$ significa que el 21 % de las
imágenes caen en un grupo cuyo dígito mayoritario no es el suyo.

**B.3**

| Espacio | ARI de K-Means ($k = 10$) |
|---|---|
| 64 píxeles | 0.667 |
| PCA, 10 componentes | 0.654 |
| t-SNE, 2 coordenadas | **0.889** |

PCA-10 da lo mismo que 64D (es casi la misma geometría, sin el ruido). t-SNE sube el ARI
a 0.89 porque su mapa ya separó los vecindarios que en 64D se solapaban. La partición
sobre t-SNE tiene silueta **0.64 en el mapa** y **0.16 en los 64 píxeles**: en el mapa
los grupos parecen islas; en los datos, siguen siendo las mismas nubes solapadas de
siempre. La silueta del mapa no dice nada sobre los datos; la de 64D sí, y es la que se
reporta.

## Parte C — ¿Los grupos del mapa existen?

**C.1** El mapa de los 182 "1" muestra dos o tres grupos claros.

**C.2**

| $k$ | (i) silueta en el mapa | (ii) esa partición en 64D | (iii) K-Means directo en 64D | (iv) nulo |
|---|---|---|---|---|
| 2 | 0.566 | 0.296 | 0.313 | 0.043 |
| 3 | 0.657 | 0.352 | 0.353 | 0.043 |
| 4 | 0.613 | 0.254 | 0.267 | — |

**C.3** Los grupos **existen**: en los 64 píxeles, la partición de t-SNE tiene silueta
0.30–0.35, ocho veces la de la referencia nula (0.04) y prácticamente igual a la que
K-Means encuentra directamente en 64D. Lo que fabricó t-SNE es la **apariencia**: 0.66
en el mapa frente a 0.35 en los datos — una "estructura razonable" convertida en
"estructura fuerte". Los tres subgrupos ($k = 3$) son tres formas de escribir el 1: un
palo vertical (99 imágenes), un palo con **base** horizontal (27), y un palo con
**gancho** superior (56). Es una estructura real que las etiquetas no muestran, y el tipo
de hallazgo para el que un mapa t-SNE sí sirve — siempre que después se verifique en el
espacio original, como aquí.

## Tabla de cierre (lo que se espera)

| Método | Para qué lo usaría | Qué no le pediría |
|---|---|---|
| PCA | Comprimir, quitar ruido y redundancia; preprocesar un modelo **validando con su métrica**; ver la estructura global | Que conserve la información de la clase; que la varianza explicada diga cuántos componentes hacen falta |
| K-Means | Segmentar cuando hay grupos convexos; resumir; con la silueta y una referencia nula al lado | Que recupere las etiquetas que a mí me interesan (el 8 no tiene grupo); que el $k$ que propone la silueta sea el "verdadero" |
| t-SNE | Mirar vecindarios y descubrir subestructura (las tres formas del 1); explorar | Que las distancias, los tamaños o la silueta del mapa signifiquen algo; usar sus coordenadas como variables; concluir grupos sin verificarlos en el espacio original |

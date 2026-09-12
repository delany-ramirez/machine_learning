# Solución · Ejercicio 01 · ¿Hay grupos dentro de los tintos?

> **Material del docente.** Números obtenidos con `random_state=42` en todo (K-Means,
> permutaciones de la referencia nula, submuestreo). Las siluetas y los ARI son estables a
> la segunda cifra decimal entre corridas; los perfiles, exactos.

## Parte A — Preparación

**A.1** 1359 tintos sin duplicados; el 13.5 % tiene `quality ≥ 7` (frente al 19.7 % del
conjunto completo: los tintos de este dataset son peores en promedio).

**A.2** Sin estandarizar, la variable con más varianza es `total_sulfur_dioxide`, y los tres
grupos de K-Means tienen medias de 109, 55 y 22 mg/L en esa variable: K-Means partió los
vinos **por dióxido de azufre** y nada más, porque es la única variable que cuenta en la
distancia euclídea sin estandarizar (notebook 02, sección 1).

## Parte B — ¿Cuántos grupos, y hay grupos?

**B.1**

| $k$ | Inercia | Silueta | Davies-Bouldin | Silueta (nulo) |
|---|---|---|---|---|
| 2 | 12 182 | **0.205** | 1.90 | 0.094 |
| 3 | 10 722 | 0.188 | 1.75 | 0.105 |
| 4 | 9 734 | 0.169 | 1.67 | 0.087 |
| 5 | 8 602 | 0.189 | 1.46 | 0.090 |
| 6 | 7 953 | 0.191 | **1.41** | 0.088 |
| 7 | 7 314 | 0.192 | 1.41 | 0.089 |
| 8 | 7 015 | 0.185 | 1.47 | 0.090 |

No coinciden: la silueta prefiere $k = 2$ (0.205) y es casi plana a partir de 5 (0.19);
Davies-Bouldin prefiere $k = 6$–7; la inercia no tiene codo. Es el caso general con datos
reales (notebook 02, sección 2), aquí más marcado que en el conjunto completo.

**B.2** La silueta de la referencia nula es 0.09–0.10 para todos los $k$. La de los tintos
en $k = 2$ (0.205) la duplica: **hay algo**, pero 0.205 está por debajo del umbral de
0.25 de Kaufman y Rousseeuw ("sin estructura sustancial"). Es una estructura real y muy
débil: un gradiente cortado en dos, no dos grupos.

**B.3** Menos que los blancos: 0.205 frente a 0.21 en la silueta absoluta, parecidos, pero
la separación respecto a la referencia es menor (2.2× frente a 2.6×) y, sobre todo, la
estabilidad (D.1) es mucho menor. Los blancos tenían un eje claro (azúcar residual, 3×
entre grupos); en los tintos ninguna variable cambia tanto.

## Parte C — Interpretar

**C.1** Perfil con $k = 2$ (unidades originales):

| Variable | Grupo 0 (n = 813) | Grupo 1 (n = 546) | Cociente 1/0 |
|---|---|---|---|
| fixed_acidity | 7.32 | 9.79 | 1.34 |
| volatile_acidity | 0.606 | 0.416 | 0.69 |
| citric_acid | 0.149 | 0.456 | **3.06** |
| residual_sugar | 2.39 | 2.72 | 1.14 |
| chlorides | 0.080 | 0.100 | 1.25 |
| free_sulfur_dioxide | 16.6 | 14.8 | 0.89 |
| total_sulfur_dioxide | 49.0 | 43.6 | 0.89 |
| density | 0.996 | 0.998 | 1.00 |
| ph | 3.38 | 3.21 | 0.95 |
| sulphates | 0.600 | 0.747 | 1.25 |
| alcohol | 10.3 | 10.6 | 1.03 |

Grupo 1: tintos **más ácidos** (acidez fija alta, pH bajo), con tres veces más ácido
cítrico, más sulfatos y menos acidez volátil — el perfil de un vino más "estructurado" y
mejor conservado. Grupo 0: menos ácido, más acidez volátil (la que da olor a vinagre), más
pH. Ninguna variable cambia tanto como el azúcar en los blancos.

**C.2** Con $k = 3$, el grupo nuevo (n = 319) se caracteriza por **mucho más dióxido de
azufre** (total 91 frente a 31–35 mg/L, libre 27 frente a 11–13) y menos alcohol (9.8); los
otros dos son, aproximadamente, los dos grupos de $k = 2$ (605 y 430 vinos se quedan
donde estaban). La tabla cruzada muestra que el grupo "sulfitado" toma vinos de **ambos**
grupos anteriores (206 del grupo 0 y 113 del 1): es una estructura nueva, un eje distinto
(conservante, no acidez) que cruza al anterior, lo que explica por qué la silueta no cae
mucho de 2 a 3.

**C.3**

| Partición | Calidad media por grupo | % buenos por grupo | NMI con `quality` |
|---|---|---|---|
| $k = 2$ | 5.46 · 5.86 | 7.3 % · **22.9 %** | 0.034 |
| $k = 3$ | 5.32 · 5.54 · 5.97 | 3.4 % · 9.5 % · **26.6 %** | 0.064 |

La NMI es tan baja como en el conjunto completo: los grupos **no predicen** la calidad.
Pero la fracción de buenos sí varía: en el grupo ácido/cítrico/sulfatado hay tres veces
más vinos buenos que en el otro, y el grupo sulfitado casi no tiene. Es información débil
y correlacional (sulfatos, ácido cítrico y alcohol correlacionan con la calidad; módulo 4),
no un clasificador: un 27 % de buenos en el mejor grupo sigue siendo un 73 % de no buenos.

## Parte D — Estabilidad y otro algoritmo

**D.1**

| $k$ | ARI submuestra vs. completo |
|---|---|
| 2 | 0.90 ± 0.01 |
| 3 | 0.84 ± 0.06 |
| 4 | 0.62 ± 0.04 |
| 5 | 0.85 ± 0.02 |
| 6 | 0.77 ± 0.05 |

Solo $k = 2$ es razonablemente estable, y bastante menos que en el conjunto completo
(0.99). $k = 4$ es inestable (0.62): depende de qué vinos entran. Que $k = 5$ sea más
estable que 4 es una señal de que el "paisaje" de particiones es plano: hay varias formas
casi igual de buenas de cortar un continuo.

**D.2**

| Linkage | Tamaños | ARI con K-Means ($k=2$) |
|---|---|---|
| Ward | 1098 / 261 | **0.32** |
| average | 1351 / 8 | 0.00 |

Ward **no** coincide con K-Means (0.32, frente a 0.90 en el conjunto completo): corta un
grupo pequeño de 261 vinos en vez de partir por la mitad. Cuando dos algoritmos que
buscan lo mismo (inercia) dan particiones distintas, es porque no hay una partición
claramente mejor que las demás — la misma lectura que la estabilidad. *Average* aísla 8
atípicos, como en el notebook 02.

## Parte E — Anomalías

**E.1** El gráfico de k-distancias baja suavemente sin codo (mediana 1.55, percentil 90 de
2.5, percentil 99 de 4.7). Barrido:

| `eps` | Grupos | % ruido |
|---|---|---|
| 1.5 | 1 | 31.0 |
| 2.0 | 3 | 10.4 |
| 2.5 | 2 | 5.2 |
| 3.0 | 2 | 2.1 |

**E.2** Con `eps = 2`, 141 tintos (10.4 %) son ruido. Mediana del $|z|$ máximo: 3.3 en el
ruido frente a 1.5 en el resto. El máximo global de **las 11 variables** está entre los
vinos-ruido. En calidad no se distinguen (14.9 % de buenos frente a 13.4 %): a diferencia
del conjunto completo (6.8 % frente a 19.4 %), aquí los raros no son peores. Un tinto con
una variable extrema puede ser un error de medición o un estilo de vino, no necesariamente
un mal vino.

**E.3** Isolation Forest con la misma contaminación coincide en 94 de 141 (Jaccard 0.50):
más acuerdo que en el conjunto completo (0.33), porque en los tintos los atípicos son
más extremos y ambos métodos los ven.

## Párrafo final (lo que se espera)

Hay una estructura real pero muy débil en los tintos: la silueta (0.205) duplica la de la
referencia nula pero no llega al umbral de "estructura sustancial", solo $k = 2$ es
razonablemente estable, y Ward no reproduce la partición de K-Means. El eje que aparece
es acidez / ácido cítrico / sulfatos (y, con $k = 3$, la sulfitación), no un grupo
discreto. La partición correlaciona algo con la calidad (7 % frente a 23 % de buenos) pero
no la predice (NMI 0.03). Para predecir la calidad, etiquetas y un modelo supervisado
(módulo 4); el clustering aquí sirve para describir el espacio de los tintos y para
señalar los 141 vinos extremos que conviene revisar.

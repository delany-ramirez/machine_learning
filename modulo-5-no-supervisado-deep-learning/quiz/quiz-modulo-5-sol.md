# Clave · Quiz Módulo 5 — No supervisado y deep learning

> **Material del docente.** Se indica lo mínimo exigible y, cuando aplica, el error típico
> que conviene comentar en la retroalimentación.

---

**1. Estandarizar**

**a)** Tres tramos de **ingreso**. Con varianza $10^{14}$ frente a $\sim 10^2$ de la edad, la
distancia euclídea es, a todos los efectos, la diferencia de ingresos; K-Means partió una
variable en tres intervalos (`01-clustering.md`, §2; en Wine Quality sin estandarizar,
`total_sulfur_dioxide` lo decide todo y el ARI contra `tipo` cae de 0.93 a 0.31).

**b)** Estandarizar (o escalar de otra forma justificada) antes de agrupar. Afecta a
DBSCAN y al jerárquico porque los tres se basan en **distancias**, que cambian con las
unidades. Un árbol compara cada variable con un umbral, una a la vez, y es invariante a
transformaciones monótonas de cada variable (S10). Error típico: decir que estandarizar
"siempre" es necesario; para árboles no lo es.

---

**2. Convergencia de Lloyd**

Converge porque cada uno de sus dos pasos —asignar al centroide más cercano, mover el
centroide a la media— **no puede aumentar** la inercia (cada uno es óptimo dado el otro),
y hay un número finito de particiones posibles: la inercia baja o se queda igual en cada
iteración y en algún momento se estanca. No garantiza nada bueno porque el punto de
llegada es un **mínimo local** que depende de la inicialización: con $k$ puntos al azar,
el 30 % de las corridas del notebook 01 terminan en una partición claramente peor. Las dos
medidas: **K-Means++** (elegir los centroides iniciales con probabilidad proporcional a
$D^2$) y **varias inicializaciones** (`n_init`), quedándose con la de menor inercia.

---

**3. Un $k$ siempre**

**a)** Porque ambos criterios **comparan particiones entre sí**: la inercia siempre baja
con $k$ y la silueta siempre tiene un máximo en algún $k$. Ninguno comprueba que exista
algo que particionar; K-Means impone una partición a cualquier nube de puntos, y sobre
datos uniformes la silueta de esa partición es 0.41, no cero (`02-validacion-clusters.md`,
§3).

**b)** Una **referencia nula**: construir datos sin grupos por construcción que se
parezcan a los reales en todo lo demás (columnas permutadas de forma independiente, o
uniforme en la caja de los datos, como en el *gap statistic*), agruparlos igual, y
comparar la silueta. Si la real no se separa de la nula, no hay estructura que reportar.
También sirve la **estabilidad** por submuestreo (los grupos reales reaparecen con la
mitad de los datos). Vale cualquiera de las dos bien explicada.

---

**4. Qué encuentra un clustering**

La conclusión correcta es la contraria: el clustering **funcionó** — encontró la
estructura dominante de los datos (tinto/blanco, la dirección de mayor varianza) sin
haber visto la etiqueta. Lo que no hizo es encontrar la estructura que al gerente le
interesa (la calidad), y no tenía por qué: un algoritmo no supervisado no sabe qué
pregunta se le hace; agrupa por lo que más varía. Clustering **no es clasificación sin
etiquetas**. Si lo que se quiere es predecir la calidad, hay que etiquetar y usar un
modelo supervisado (el módulo 4 lo hizo). El clustering sirve para describir, segmentar
y detectar lo raro (`01-clustering.md`, §1; notebook 02, sección 3).

---

**5. Qué algoritmo**

- **a)** DBSCAN (separa formas arbitrarias por densidad; ARI 0.99 sobre las lunas) o
  jerárquico con *single linkage* (sigue cadenas; ARI 1.0). K-Means no (fronteras rectas,
  ARI 0.24).
- **b)** K-Means: escala a millones de filas ($O(nkp)$ por iteración) y sus supuestos
  (convexos) se cumplen. El jerárquico necesita la matriz $n^2$ de distancias (imposible
  con $2 \times 10^5$).
- **c)** DBSCAN: es el único que tiene una noción explícita de **ruido** (puntos que no
  pertenecen a ningún grupo). Alternativa aceptable: Isolation Forest. K-Means asigna
  todo a algún grupo y los atípicos mueven los centroides.
- **d)** Jerárquico (Ward, o *average* tras quitar atípicos): da la jerarquía completa y
  el dendrograma, y con 500 filas el costo es trivial.

---

**6. La información en la dirección de poca varianza**

**a)** PCA **no ve $y$**: elige direcciones por varianza de $\mathbf{X}$, y nada obliga a que
la dirección que separa las clases sea de gran varianza. Aquí las clases se separan a lo
largo de una variable de poca varianza (notebook 03, sección 5.2). El supuesto que falla
es "varianza = información": es cierto para reconstruir $\mathbf{X}$ (PCA es óptimo para
eso), falso para predecir $y$.

**b)** Con la **métrica del modelo supervisado** en validación cruzada, con el PCA dentro
del `Pipeline`, para distintos $q$ — y aceptando que la respuesta puede ser "todos" (en
Wine Quality, quitar componentes baja la AP de 0.52 a 0.40; en los dígitos, 20 de 64
bastan). Nunca con la varianza explicada sola. Error típico: la regla del 90 % como si
fuera un teorema.

---

**7. Leer un mapa t-SNE**

- (i) **No lo respalda por sí solo.** t-SNE dibuja grumos incluso sobre una gaussiana sin
  grupos (notebook 04, sección 3: silueta 0.35–0.38 en el mapa, 0.08 en los datos). Hay
  que verificar en el espacio original (referencia nula, silueta en $p$ dimensiones).
- (ii) **No.** La perplejidad normaliza la densidad local: un grupo 5× más disperso
  aparece del mismo tamaño en el mapa. Los tamaños no significan nada.
- (iii) **No.** Nada en el costo de t-SNE optimiza la distancia entre grupos: un grupo 3×
  más lejano aparece a la misma distancia. Las distancias entre grupos no significan nada.
- (iv) **Sí, con matices.** Es lo único que t-SNE conserva: los vecindarios
  (*trustworthiness* 0.99). Dos puntos juntos en el mapa muy probablemente eran vecinos
  en el espacio original.

---

**8. Activaciones y gradiente**

Sin activación, cada capa es una transformación lineal y la composición de
transformaciones lineales es lineal: $\mathbf{X}\mathbf{W}_1\mathbf{W}_2\cdots\mathbf{W}_L =
\mathbf{X}\mathbf{W}'$. Por muchas capas que haya, el modelo es una regresión lineal (o
logística, con la sigmoide final). La no linealidad $\phi$ es lo que permite que las capas
construyan variables nuevas y la frontera se curve.

En la retropropagación, el error que llega a una capa se multiplica elemento a elemento
por $\phi'(\mathbf{Z}_l)$ antes de seguir hacia atrás: $\boldsymbol{\Delta}_{l-1} =
(\boldsymbol{\Delta}_l\mathbf{W}_l^\top) \odot \phi'(\mathbf{Z}_{l-1})$. La derivada de la
sigmoide vale como máximo 0.25 y casi cero fuera de $[-4, 4]$; tras $L$ capas el gradiente
de la primera lleva un factor $\leq 0.25^L$: **se desvanece** (en 10 capas, $10^6$ veces
menor que en la última; notebook 05, sección 5). ReLU tiene derivada exactamente 1 para
$z > 0$, y el gradiente atraviesa las capas sin atenuarse. Error típico: atribuir la
ventaja de ReLU a "ser más rápida de calcular" — es cierto pero secundario.

---

**9. Tres reportes de AP**

De más a menos optimista: **el segundo** (early stopping sobre el mismo conjunto en el
que reporta: eligió la época con la mejor AP *de esos datos*; en Wine Quality infla 0.017,
en Adult 0.004), luego **el tercero** (correcto), y **el primero** puede quedar en
cualquier lugar: no es optimista por selección, pero 100 épocas fijas suelen ser
demasiadas (el MLP sobre Adult para en 5–19) y la última época es un modelo
sobreajustado — es un reporte honesto de un modelo peor. Se debe usar el **tercero**: el
conjunto que decide cuándo parar forma parte del entrenamiento, no de la evaluación;
es la fuga de selección de la S8 (CV anidada) aplicada a las épocas. Lo mínimo exigible:
identificar al segundo como el más optimista y al tercero como el correcto, con la razón.

---

**10. Sesgo inductivo**

La explicación común: **gana el modelo cuya arquitectura codifica la estructura de los
datos**. Los árboles con boosting manejan de fábrica escalas heterogéneas, umbrales,
categóricas e interacciones abruptas —la estructura típica de una tabla—, y aproximan
funciones irregulares; un MLP tiene que aprender todo eso desde pesos aleatorios y sus
funciones son suaves por construcción, así que en tabular pequeño y mediano pierde, como
en los *benchmarks* de Grinsztajn et al. (2022). Una CNN codifica que la entrada es una
imagen: el mismo filtro en todas las posiciones (pesos compartidos, localidad), y por eso
detecta el mismo trazo desplazado un píxel donde la logística y el MLP, con cada peso
atado a una posición, se desploman (0.62 frente a 0.42–0.51). No es cuestión de "más
parámetros": el MLP tiene diez veces más que la logística y no la mejora sobre los
dígitos; la CNN gana por **dónde** pone los suyos, no por cuántos tiene.

La comparación exigible: **pareada sobre los mismos pliegues**, contra la línea base
lineal y el mejor ensamble de árboles, con error estándar y cociente, con el early
stopping sobre datos apartados del entrenamiento (pregunta 9), y con el tiempo de
entrenamiento al lado; adoptar la red solo si la diferencia es detectable **y** relevante
para la decisión del proyecto. Error típico: proponer "probar la red y ver si mejora" sin
la comparación pareada ni la corrección de la fuga.

# 04 · Árboles de decisión, bagging y Random Forest

**Módulo 4 · Sesión 10** — Árboles de decisión y bagging

## Objetivos

- Entender cómo crece un árbol: medidas de impureza, búsqueda de la mejor partición y
  recursión; y por qué sus fronteras son rectángulos alineados con los ejes.
- Situar la profundidad y la poda como la perilla sesgo-varianza del árbol.
- Entender por qué un árbol es **inestable** y cómo el **bagging** convierte esa
  inestabilidad en una ventaja.
- Entender qué añade **Random Forest** sobre bagging, cuándo ayuda y cuándo no.
- Conocer el error *out-of-bag* y la importancia de variables por impureza, con sus límites.

## 1. Cómo crece un árbol

Un árbol de decisión parte el espacio de las variables con preguntas binarias de la forma
"¿$x_j \leq t$?", una en cada nodo, hasta llegar a hojas donde predice la clase mayoritaria
(o la media, en regresión). Tres decisiones lo definen: **qué** medir en cada nodo, **cómo**
elegir la partición, y **cuándo** parar.

### Impureza

Con $p_k$ la fracción de la clase $k$ en un nodo:

$$
\text{Gini} = 1 - \sum_k p_k^2 \qquad\qquad
\text{Entropía} = -\sum_k p_k \log_2 p_k
$$

Ambas valen 0 en un nodo puro y son máximas con las clases a partes iguales. Son
estrictamente **cóncavas**, y eso importa: una partición que lleva un nodo 50/50 a dos
nodos 70/30 reduce Gini y entropía, pero **no** reduce el error de clasificación
(lineal por tramos). Por eso los árboles crecen con Gini o entropía —que premian el
progreso— y se evalúan con las métricas de `03-metricas-clasificacion.md`. En la práctica
las dos medidas eligen casi siempre la misma partición; `scikit-learn` usa Gini por
defecto porque no requiere logaritmos.

### La mejor partición

Para una variable $x_j$, la calidad de partir en $t$ es la **reducción de impureza**
ponderada por el tamaño de cada hijo:

$$
\Delta(j, t) = I(\text{nodo}) - \frac{n_I}{n} I(\text{izq}) - \frac{n_D}{n} I(\text{der})
$$

Como solo importa qué puntos caen a cada lado, basta probar los umbrales entre valores
consecutivos de $x_j$ ordenados: $O(n \log n)$ por variable, y el mejor $(j, t)$ es una
búsqueda exhaustiva sobre todas las variables. Es un algoritmo **voraz** (*greedy*): elige
la mejor partición *ahora*, sin mirar si otra abriría mejores particiones después. El árbol
óptimo global es un problema NP-completo; el voraz funciona bien en la práctica.

Después se **repite recursivamente** en cada hijo hasta que el nodo sea puro, tenga menos de
`min_samples_split` filas, o se alcance `max_depth`. `03-arboles-intuicion.ipynb` lo
implementa en ~40 líneas y verifica que reproduce exactamente las particiones de
`DecisionTreeClassifier`.

### Propiedades que salen de esta construcción

- Las fronteras son **rectángulos alineados con los ejes**. Un árbol no puede trazar una
  diagonal: la aproxima con escalones. Por eso un árbol solo se queda corto en relaciones
  suaves —en Wine Quality, el mejor árbol podado tiene AP 0.42 frente a 0.53 de la
  logística (`04-arboles-bagging-aplicado.ipynb`)— y por eso, promediados, los escalones
  se convierten en curvas.
- **No necesitan escalado**: cada partición compara una variable con un umbral, y el
  orden no cambia al transformar monótonamente. Tampoco necesitan codificación *one-hot*
  en implementaciones que manejan categóricas de forma nativa (LightGBM, S11).
- Capturan **interacciones** de forma natural: la pregunta del nodo hijo depende de la
  respuesta del padre. Un modelo lineal necesita términos explícitos $x_1 x_2$ para eso.
- Son **interpretables** mientras son pequeños: un árbol de profundidad 3 se lee como una
  lista de reglas. A partir de cierta profundidad, deja de serlo — y los ensambles nunca lo
  son directamente (S11 resuelve eso).

## 2. Profundidad, poda y sobreajuste

Sin límite, el árbol parte hasta que cada hoja es pura: memoriza el conjunto de
entrenamiento, ruido incluido. En `03-arboles-intuicion.ipynb`, el árbol sin límite tiene
accuracy 1.0 en entrenamiento y 0.867 en prueba, frente a 0.887 del árbol de profundidad 2;
en Wine Quality, AP 0.29 frente a 0.42 — apenas por encima de la prevalencia de 0.19. La
profundidad es la perilla sesgo-varianza del árbol, y la curva en U de
`05-sesgo-varianza-validacion.md` reaparece intacta con `max_depth` en el eje $x$.

Dos formas de controlarla:

- **Poda a priori**: `max_depth`, `min_samples_leaf`, `min_samples_split`. Simples, y
  suficientes casi siempre.
- **Poda por costo-complejidad** (Breiman, 1984): dejar crecer el árbol completo $T_0$ y
  elegir el subárbol $T$ que minimiza $R_\alpha(T)$, definido abajo.

$$
R_\alpha(T) = R(T) + \alpha \cdot |\text{hojas}(T)|
$$

donde $R(T)$ es la impureza total de las hojas. Cada $\alpha$ define un subárbol anidado;
$\alpha$ se elige por validación (`ccp_alpha` en `scikit-learn`). Es Lasso para árboles:
$\alpha$ penaliza el número de hojas como $\lambda$ penalizaba la norma de los
coeficientes.

## 3. Inestabilidad, y por qué es una oportunidad

Un árbol tiene **alta varianza** en un sentido muy concreto: cambiar unos pocos puntos de
entrenamiento puede cambiar la partición de la raíz y, con ella, todo el árbol. Cuatro
remuestras bootstrap de los mismos datos dan cuatro fronteras muy distintas
(`03-arboles-intuicion.ipynb`, sección 4). La descomposición de
`05-sesgo-varianza-validacion.md` lo dice de otra forma: un árbol profundo tiene sesgo bajo
y varianza alta.

Pero los errores de esos cuatro árboles están en **lugares distintos**. Si se promedian
sus predicciones, los errores que no comparten tienden a cancelarse. Esa es la idea de
todos los ensambles por promedio.

## 4. Bagging

**Bootstrap aggregating** (Breiman, 1996): entrenar $B$ árboles, cada uno sobre una
remuestra bootstrap (con reemplazo, del mismo tamaño $n$) del conjunto de entrenamiento, y
promediar sus predicciones — las probabilidades, mejor que los votos.

Si los $B$ árboles fueran independientes con varianza $\sigma^2$, el promedio tendría
varianza $\sigma^2 / B$. No son independientes (comparten la mayoría de los datos), pero la
reducción es grande de todos modos: en `03-arboles-intuicion.ipynb`, la desviación típica
de $P(y=1)$ entre repeticiones del experimento baja de 0.139 para un árbol solo a 0.023
para bagging con 50 árboles. El **sesgo no cambia**: el promedio de árboles profundos sigue
siendo tan flexible como cada uno. Por eso bagging usa árboles **sin podar** —sesgo mínimo—
y deja que el promedio se ocupe de la varianza: en Wine Quality, `min_samples_leaf=1` es la
mejor opción en toda la rejilla.

Tres propiedades prácticas:

- Bagging **no sobreajusta con $B$**. Más árboles nunca empeoran; solo cuestan más. La
  curva de AP contra $B$ se aplana (en Wine Quality, alrededor de $B = 100$; de 300 a 1000 la
  ganancia es de 0.002).
- Es **paralelizable** trivialmente: cada árbol es independiente (`n_jobs=-1`).
- **Error out-of-bag (OOB)**: cada remuestra deja fuera, en promedio, el
  $(1 - 1/n)^n \approx e^{-1} \approx 37\,\%$ de las filas. Promediando, para cada fila, solo
  los árboles que no la vieron, se obtiene una estimación del error de generalización sin
  partir los datos ni hacer validación cruzada. En Wine Quality, la AP OOB sigue a la de CV
  a una o dos centésimas desde $B = 100$; con pocos árboles la **subestima**, porque cada fila
  la predicen apenas $0.37 B$ árboles.

## 5. Random Forest

El límite de bagging es que sus árboles se **parecen**. Si una variable es claramente la
mejor para la raíz, casi todas las remuestras la eligen, y los árboles quedan
correlacionados. Con correlación $\rho$ entre árboles, la varianza del promedio es

$$
\rho\,\sigma^2 + \frac{1 - \rho}{B}\,\sigma^2
$$

El segundo término desaparece con $B$; el primero **no**. Random Forest (Breiman, 2001)
ataca $\rho$: en cada nodo, en vez de buscar la mejor partición entre todas las variables,
la busca entre un subconjunto aleatorio de `max_features`. Los árboles individuales son
peores, pero menos parecidos entre sí — y el promedio gana. `max_features="sqrt"` (la
recomendación original para clasificación) es el valor por defecto de `scikit-learn`;
`max_features=p` **es** bagging.

### Cuándo ayuda y cuándo no: dos mediciones

- En `03-arboles-intuicion.ipynb`, con 2 variables informativas y 18 de ruido, Random Forest
  **no** supera a bagging (0.877 frente a 0.887), y con `max_features=1` es claramente peor
  (0.830). Un subconjunto de 4 variables entre 20 no contiene ninguna de las dos reales en el
  63 % de los nodos: esos nodos parten por ruido. Decorrelacionar no sirve de nada si hace
  que los árboles no vean la señal.
- En `04-arboles-bagging-aplicado.ipynb`, con 12 variables que casi todas llevan señal,
  la fila `max_features=12` (bagging) es la **peor** de la rejilla y `max_features=1` la
  mejor (AP 0.58 frente a 0.55). La comparación pareada da RF − bagging = 0.016 ± 0.003.

La lección es que `max_features` es un hiperparámetro que se **afina**, no una mejora
automática. Su valor óptimo depende de la fracción de variables relevantes.

### Extra-Trees

*Extremely randomized trees* (Geurts et al., 2006) llevan la idea un paso más: además de
muestrear variables, eligen el **umbral** de cada partición al azar en vez de buscar el
óptimo. Árboles aún peores individualmente, aún menos correlacionados, y más rápidos de
construir (no hay búsqueda de umbral). En Wine Quality supera a Random Forest por
0.018 ± 0.003 de AP, y es el mejor modelo de la sesión 10 (AP 0.59).

## 6. Importancia de variables por impureza

Un bosque no es interpretable árbol por árbol, pero sí ofrece un resumen: la **importancia
por reducción media de impureza** (*mean decrease in impurity*, MDI) de cada variable es la
suma, sobre todos los nodos de todos los árboles que parten por ella, de $\Delta$ ponderada
por el tamaño del nodo. Es gratis (se acumula durante el entrenamiento) y por eso es la
primera gráfica que todo el mundo hace.

Tiene dos sesgos conocidos, que `04-pipeline-caracteristicas-aplicado.ipynb` (módulo 2) ya
sufrió y que `06-interpretabilidad.md` resuelve:

1. **Favorece a las variables con muchos valores distintos** (continuas, o categóricas de
   alta cardinalidad): ofrecen más umbrales candidatos, y por puro azar alguno reduce la
   impureza. Una columna de ruido continuo puede aparecer con importancia no trivial.
2. **Se calcula sobre entrenamiento**: mide cuánto usó el bosque cada variable para ajustar,
   no cuánto le sirve para generalizar. Con árboles sin podar, parte de esa "importancia"
   es memorización.

Por eso la MDI sirve para una primera mirada, no para descartar variables ni para explicar
un modelo a terceros. La sesión 11 introduce la importancia por permutación y SHAP, que
miden sobre datos no vistos y no tienen el sesgo de cardinalidad.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Impureza (Gini, entropía) | Cóncavas: premian el progreso parcial; el error de clasificación no | Ganancia por partición en boosting (S11) |
| Partición voraz | Mejor $(j, t)$ ahora, sin mirar adelante; $O(n \log n)$ por variable | Histogramas de LightGBM aceleran justo esto (S11) |
| Profundidad y poda | La perilla sesgo-varianza del árbol; $\alpha$ es Lasso para hojas | `max_depth` / `num_leaves` en boosting (S11) |
| Bagging | Promedio de árboles profundos sobre remuestras; reduce varianza, no sesgo; no sobreajusta con $B$ | Contraste con boosting, que sí sobreajusta con $B$ (S11) |
| OOB | Validación gratis con el 37 % que cada remuestra deja fuera | — |
| Random Forest | Bagging + `max_features` por nodo para bajar $\rho$; se afina, no es gratis | Línea base fuerte del proyecto integrador |
| MDI | Importancia gratis, sesgada hacia alta cardinalidad y calculada en entrenamiento | Reemplazada por permutación y SHAP (S11) |

**Notebooks:** `03-arboles-intuicion.ipynb` (todo a mano, en 2D) ·
`04-arboles-bagging-aplicado.ipynb` (Wine Quality: árbol, bagging, OOB, rejilla de Random
Forest, Extra-Trees, comparación pareada y conjunto de prueba).

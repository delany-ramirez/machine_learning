# 05 · Boosting: AdaBoost, gradient boosting, XGBoost, LightGBM y stacking

**Módulo 4 · Sesión 11** — Boosting e interpretabilidad

## Objetivos

- Entender la diferencia estructural entre bagging (árboles independientes, en paralelo) y
  boosting (árboles secuenciales, cada uno corrige al anterior), y qué implica para el
  sesgo, la varianza y el sobreajuste.
- Seguir el algoritmo de **AdaBoost** y su reformulación general como **gradient boosting**:
  ajustar cada árbol al gradiente negativo de la pérdida.
- Ver que, para clasificación, ese gradiente es $y - \hat{p}$ — el mismo de la regresión
  logística.
- Conocer los hiperparámetros que importan (rondas, tasa de aprendizaje, tamaño del árbol,
  submuestreo, regularización) y la receta de **early stopping**.
- Saber qué añaden **XGBoost** y **LightGBM**, y qué es el **stacking**.

## 1. Dos formas de combinar modelos

| | Bagging / Random Forest (S10) | Boosting |
|---|---|---|
| Cómo se entrenan los árboles | Independientes, en paralelo, sobre remuestras | En secuencia; cada uno depende de los anteriores |
| Modelo base | Árboles **profundos** (sesgo bajo, varianza alta) | Árboles **pequeños** (sesgo alto, varianza baja) |
| Qué reduce el ensamble | La **varianza** | El **sesgo** (y algo la varianza, con submuestreo) |
| Más árboles | Nunca empeora; la curva se aplana | **Sobreajusta**: hay un número óptimo |
| Paralelizable | Trivialmente | Solo dentro de cada árbol |
| Hiperparámetros críticos | `max_features`; casi funciona sin afinar | Rondas × tasa de aprendizaje × tamaño del árbol; hay que afinar |

Ambas familias promedian árboles, pero con lógicas opuestas: bagging toma modelos que
sobreajustan y los estabiliza; boosting toma modelos que subajustan y los va corrigiendo.

## 2. AdaBoost

*Adaptive Boosting* (Freund y Schapire, 1997). Con etiquetas $y_i \in \{-1, +1\}$ y un
modelo base débil —típicamente un **tocón** (*stump*), un árbol de profundidad 1—, se
mantiene un peso $w_i$ por observación, inicialmente $1/n$, y en cada ronda
$m = 1, \dots, M$:

1. Se ajusta el modelo base $h_m$ **ponderando** cada observación por $w_i$.
2. Se calcula su error ponderado $\varepsilon_m = \sum_i w_i \,[h_m(x_i) \neq y_i]$.
3. Se le asigna un peso en el ensamble:

$$
\alpha_m = \frac{1}{2}\log\frac{1 - \varepsilon_m}{\varepsilon_m}
$$

4. Se actualizan los pesos, subiendo los de las observaciones falladas:
   $w_i \leftarrow w_i \exp(-\alpha_m y_i h_m(x_i))$, y se normalizan.

La predicción es el voto ponderado $\text{signo}\left(\sum_m \alpha_m h_m(x)\right)$. Un
tocón con $\varepsilon_m = 0.5$ (aleatorio) recibe $\alpha_m = 0$; uno con $\varepsilon_m$
cerca de 0, mucho peso. Las observaciones difíciles acumulan peso ronda tras ronda, y los
tocones siguientes se ven obligados a atenderlas.

`05-boosting-intuicion.ipynb` lo implementa en 15 líneas: 200 tocones —cada uno una línea
vertical u horizontal— dibujan las dos medias lunas del notebook 03, con el mismo error de
prueba (0.12) que bagging con árboles profundos. `AdaBoostClassifier` (algoritmo SAMME, su
generalización multiclase) produce predicciones idénticas.

AdaBoost se puede reescribir como la minimización de la **pérdida exponencial**
$\sum_i \exp(-y_i F(x_i))$ por descenso en el espacio de funciones — y esa reescritura
(Friedman, Hastie y Tibshirani, 2000) es la puerta a la generalización siguiente.

## 3. Gradient boosting

Friedman (2001) reformula la idea para **cualquier pérdida diferenciable**. El ensamble
$F(x)$ se construye por etapas:

$$
F_0(x) = \arg\min_c \sum_i \mathcal{L}(y_i, c), \qquad
F_m(x) = F_{m-1}(x) + \nu \cdot h_m(x)
$$

donde cada árbol $h_m$ se ajusta (como regresión) al **gradiente negativo de la pérdida
respecto a la predicción actual**, evaluado en cada observación:

$$
r_{im} = -\left.\frac{\partial \mathcal{L}(y_i, F(x_i))}{\partial F(x_i)}\right|_{F = F_{m-1}}
$$

Es descenso del gradiente, pero en vez de mover un vector de parámetros, se añade una
función (un árbol) que apunta en la dirección de máximo descenso. $\nu \in (0, 1]$ es la
**tasa de aprendizaje** (*shrinkage*): cada árbol corrige solo una fracción del gradiente.

### Los dos casos que importan

| Pérdida | $\mathcal{L}(y, F)$ | Gradiente negativo $r_i$ | Qué ajusta cada árbol |
|---|---|---|---|
| Cuadrática (regresión) | $\frac{1}{2}(y - F)^2$ | $y - F$ | El **residual** ordinario |
| Entropía cruzada (clasificación) | $-y\log\sigma(F) - (1-y)\log(1-\sigma(F))$ | $y - \sigma(F)$ | $y - \hat{p}$ |

El segundo caso conecta con `01-regresion-logistica.md`: el gradiente de la entropía cruzada
respecto al log-momio es $y - \hat{p}$, exactamente el residual que la regresión logística
usaba en $\mathbf{X}^\top(\hat{\mathbf{p}} - \mathbf{y})$. Gradient boosting para
clasificación es una regresión logística **en la que los árboles hacen el papel de**
$\mathbf{X}\boldsymbol{\beta}$: $F(x)$ son log-momios, $\hat{p} = \sigma(F(x))$, y por eso sus
probabilidades salen razonablemente calibradas, a diferencia de las de Random Forest.

`05-boosting-intuicion.ipynb` implementa ambos casos en ~12 líneas. La versión de regresión
coincide con `GradientBoostingRegressor` hasta la precisión numérica ($10^{-15}$). La de
clasificación no coincide dígito a dígito por un detalle instructivo: `scikit-learn` da en
cada hoja un paso de **Newton** (divide el residual medio por la curvatura
$\sum \hat{p}_i(1-\hat{p}_i)$), que converge más rápido que el paso de gradiente puro.

### Lo que boosting hace distinto: sobreajusta con las rondas

En `05-boosting-intuicion.ipynb`, sobre $y = \sin(2\pi x) + \varepsilon$, el MSE de prueba
alcanza su mínimo en la ronda 45 y a partir de ahí **sube**: cada árbol adicional ajusta
residuales que ya son puro ruido. El número de rondas es un hiperparámetro de complejidad —
al contrario que en bagging— y se elige por validación.

La tasa de aprendizaje modula esa curva. Con $\nu = 1$ el mínimo llega en tres rondas y es
el peor; con $\nu \leq 0.3$ los mínimos son casi iguales, pero la curva es **mucho más plana**
alrededor del mínimo cuanto menor es $\nu$: en la ronda 1000, $\nu = 0.3$ ya ha subido a un
MSE de 0.19 y $\nu = 0.03$ solo a 0.135. De ahí la receta que todas las implementaciones
modernas heredan:

> **Tasa baja, muchas rondas, y parar por validación** (*early stopping*): se entrena con un
> número grande de rondas, se evalúa la métrica sobre un conjunto de validación cada ronda,
> y se conserva la ronda en la que fue mejor (`06-boosting-aplicado.ipynb`, sección 3).

### Hiperparámetros que importan

| Hiperparámetro | Qué controla | Efecto |
|---|---|---|
| Rondas (`n_estimators`) | Cuántos árboles | Complejidad; se elige por early stopping |
| Tasa de aprendizaje (`learning_rate`) | Cuánto corrige cada árbol | Menor → más rondas, curva más plana |
| Tamaño del árbol (`max_depth`, `num_leaves`) | Orden de las interacciones que puede capturar | Profundidad 1: sin interacciones; 3–8 es lo habitual |
| `min_child_samples` / `min_samples_leaf` | Filas mínimas por hoja | Regulariza; evita hojas que memorizan |
| Submuestreo de filas (`subsample`) | Fracción de filas por árbol | Regulariza y acelera (*stochastic gradient boosting*) |
| Submuestreo de columnas (`colsample_bytree`) | Fracción de variables por árbol | La idea de Random Forest, importada |
| Regularización de hojas (`reg_lambda`, `reg_alpha`) | Penaliza el valor de las hojas | $L_2$ / $L_1$, como Ridge / Lasso |

Con tantas perillas interdependientes, boosting es el caso natural para la optimización
bayesiana de `06-seleccion-hiperparametros.md`. `06-boosting-aplicado.ipynb` afina LightGBM
con 40 trials de Optuna sobre siete de ellas.

## 4. XGBoost y LightGBM

Las dos implementaciones dominantes (Chen y Guestrin, 2016; Ke et al., 2017) son gradient
boosting con árboles más una serie de mejoras de ingeniería y de regularización:

| Idea | XGBoost | LightGBM |
|---|---|---|
| Paso de **Newton** en las hojas (usa la segunda derivada de la pérdida) | Sí | Sí |
| **Regularización** explícita del valor de las hojas y del número de hojas | Sí ($\lambda$, $\alpha$, $\gamma$) | Sí |
| Submuestreo de filas y columnas | Sí | Sí |
| **Histogramas**: discretizar cada variable en ≈256 cubetas antes de buscar el umbral | Opcional (`tree_method="hist"`) | Siempre |
| Crecimiento **por hoja** (*leaf-wise*): expande la hoja con más ganancia, en vez de nivel a nivel | No (por nivel) | Sí; `num_leaves` en vez de `max_depth` |
| Variables categóricas sin *one-hot* | Experimental | Nativo |
| Valores faltantes | Aprende hacia qué lado enviarlos | Aprende hacia qué lado enviarlos |

La aceleración viene sobre todo de los histogramas: la búsqueda del mejor umbral, que en
`03-arboles-intuicion.ipynb` era $O(n \log n)$ por variable, pasa a ser $O(n)$ para construir
el histograma y $O(256)$ para recorrerlo. Sobre 30 000 filas y 200 árboles de profundidad 6,
`05-boosting-intuicion.ipynb` mide 53 s para `GradientBoostingClassifier` (exacto) frente a
1.7 s para `HistGradientBoostingClassifier`, 0.4 s para XGBoost y 0.2 s para LightGBM, con la
misma AP. Esa diferencia de dos órdenes de magnitud es lo que hace viable afinarlos.

### Lo que dice la medición sobre Wine Quality

`06-boosting-aplicado.ipynb` compara todos sobre los mismos pliegues que la sesión 10:

| Modelo | AP (CV) |
|---|---|
| Random Forest, sin afinar | 0.570 |
| Extra-Trees, sin afinar | 0.589 |
| XGBoost / LightGBM, valores por defecto | 0.543 |
| LightGBM afinado con Optuna (40 trials) | 0.572 |
| Stacking (logística + Extra-Trees + LightGBM) | 0.600 (sobre la CV repetida, donde Extra-Trees da 0.594) |

Con valores por defecto, **ningún boosting alcanza a Random Forest**; afinado, LightGBM lo
iguala pero Extra-Trees sigue 0.022 ± 0.004 por encima (comparación pareada, cociente 5, y
con el sesgo de selección a favor de LightGBM). Sobre un dataset pequeño y ruidoso, un bosque
aleatorio sin afinar puede ganar. Boosting tiende a imponerse con más datos y variables
heterogéneas —los ejercicios del módulo sobre Adult Census (49 000 filas, categóricas de alta
cardinalidad) son ese caso—, pero "XGBoost gana siempre" no es una ley: hay que medir.

### `scale_pos_weight`

El equivalente de `class_weight="balanced"` para boosting: multiplica el gradiente de los
positivos por un factor, típicamente $n_{\text{neg}} / n_{\text{pos}}$. Igual que en
`03-metricas-clasificacion.md` para la logística: sube el recall en 0.5 y reescala las
probabilidades, y **no cambia** AUC-ROC, AP ni el mejor $F_1$ alcanzable. Es mover el umbral
con otro nombre.

## 5. Stacking

*Stacked generalization* (Wolpert, 1992): entrenar un **meta-modelo** sobre las predicciones
de varios modelos base. Dos reglas:

1. Las predicciones con las que se entrena el meta-modelo deben ser **fuera de muestra**
   (validación cruzada interna, `cv=5` en `StackingClassifier`), o el meta-modelo aprende de
   predicciones sobreajustadas y confía de más en el modelo base que más memoriza.
2. El meta-modelo debe ser **simple** (una regresión logística sobre las probabilidades);
   su trabajo es ponderar, no volver a aprender el problema.

La apuesta es que modelos con **sesgos distintos** se equivoquen en sitios distintos. En
Wine Quality, apilar la logística, Extra-Trees y LightGBM gana a Extra-Trees solo por
0.006 ± 0.003 de AP —detectable por los pelos, un 1 % relativo— y el meta-modelo casi
ignora a LightGBM, que se equivoca en los mismos vinos que Extra-Trees. Es lo habitual con
modelos de la misma familia; el stacking rinde cuando los modelos base son de verdad
distintos (texto + tabular, o vistas distintas de los datos), y cuesta tiempo y una capa más
que explicar.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Boosting vs. bagging | Secuencial, reduce sesgo, sobreajusta con las rondas | — |
| AdaBoost | Repesar fallos; voto ponderado de tocones | Caso particular de gradient boosting con pérdida exponencial |
| Gradient boosting | Cada árbol ajusta el gradiente negativo de la pérdida | Cualquier pérdida diferenciable: cuantiles, Poisson, *ranking* |
| $y - \hat{p}$ | El gradiente de la entropía cruzada, otra vez | Conecta S9 (logística) con S11 y con las redes (S13) |
| Tasa baja + early stopping | La receta para el número de rondas | Todo boosting del proyecto integrador |
| XGBoost / LightGBM | Newton, regularización, histogramas, *leaf-wise*: ~100× más rápido | Modelo por defecto para tabulares grandes; se registra en MLflow (S14) |
| Stacking | Meta-modelo sobre predicciones fuera de muestra | Rinde con modelos base distintos entre sí |

**Notebooks:** `05-boosting-intuicion.ipynb` (AdaBoost y gradient boosting a mano, validados)
· `06-boosting-aplicado.ipynb` (XGBoost, LightGBM, early stopping, Optuna, `scale_pos_weight`,
stacking y conjunto de prueba sobre Wine Quality).

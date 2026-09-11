# 02 · K vecinos más cercanos y máquinas de vectores de soporte

**Módulo 4 · Sesión 9** — Clasificación

## Objetivos

- Entender KNN como el clasificador más simple posible —no aprende parámetros, memoriza— y
  qué implica eso para su sesgo, su varianza y su costo en predicción.
- Formular la SVM como el problema de **maximizar el margen**, entender el papel de los
  vectores de soporte y del hiperparámetro $C$.
- Comprender el **truco del kernel**: cómo una frontera no lineal sale de un clasificador
  lineal en un espacio que nunca se construye.
- Saber qué tienen en común los tres clasificadores de la sesión (exigen escalado) y en qué
  se diferencian (forma de la frontera, costo, probabilidades).

## 1. K vecinos más cercanos (KNN)

### La idea

Para clasificar un punto nuevo $\mathbf{x}$: buscar los $k$ puntos de entrenamiento más
cercanos y devolver la clase mayoritaria entre ellos (o, para probabilidades, la fracción de
cada clase). No hay fase de entrenamiento: el "modelo" **es** el conjunto de datos. Es el
caso extremo de un método *no paramétrico*.

La distancia habitual es la euclidiana, $d(\mathbf{x}, \mathbf{x}') = \|\mathbf{x} - \mathbf{x}'\|_2$,
aunque cualquier distancia sirve (Manhattan, coseno para texto). Lo que **siempre** hace
falta es que las variables estén en la misma escala: sin estandarizar, `total_sulfur_dioxide`
(rango 6–440) domina la distancia y `density` (rango 0.99–1.04) no participa.

### $k$ es la perilla sesgo-varianza

| $k$ | Frontera | Sesgo | Varianza |
|---|---|---|---|
| $k = 1$ | Sigue cada punto; memoriza el ruido | Mínimo | Máxima |
| $k$ moderado (15–50) | Suave, local | Moderado | Moderada |
| $k = n$ | Predice siempre la clase mayoritaria | Máximo | Nula |

Es exactamente la curva en U de `05-sesgo-varianza-validacion.md`, con $k$ en el eje de
complejidad (al revés: $k$ pequeño = modelo complejo). Se elige con validación cruzada, como
cualquier hiperparámetro.

### Por qué KNN con $k=1$ es el detector de fugas por duplicados

Si una fila de entrenamiento aparece también en validación, su vecino más cercano está a
distancia **cero** y KNN con $k=1$ acierta gratis. `02-clasificacion-aplicado.ipynb` lo mide
sobre Wine Quality: con las 1177 filas duplicadas dentro, KNN ($k=1$) obtiene un F1 de 0.66 —
mejor que la logística y que la SVM—; al quitarlas, 0.47. La fuga no solo inflaba un número,
**elegía al modelo equivocado**, y favorecía sistemáticamente al que memoriza. Cualquier
modelo con capacidad de memorizar (árboles profundos, boosting con muchas rondas) sufre la
misma fuga en menor grado.

### Costos

- **Entrenar**: nada (guardar los datos).
- **Predecir**: calcular $n$ distancias en $p$ dimensiones por cada punto nuevo, $O(np)$.
  Con estructuras como KD-tree o Ball-tree mejora en dimensiones bajas, pero en alta
  dimensión degenera a fuerza bruta.
- **Maldición de la dimensionalidad**: en muchas dimensiones, todos los puntos están a
  distancias parecidas y "el vecino más cercano" deja de ser informativo. KNN funciona bien
  con pocas variables relevantes y muchos datos; mal al revés.

## 2. Máquinas de vectores de soporte (SVM)

### El margen

Para dos clases linealmente separables hay infinitos hiperplanos que las separan. La SVM
elige el que está **más lejos de los puntos más cercanos de cada clase**: el que maximiza el
**margen**. La intuición es que un hiperplano con margen amplio es más robusto a pequeñas
perturbaciones de los datos —tiene menos varianza— que uno que pasa rozando.

Con etiquetas $y_i \in \{-1, +1\}$ y frontera $\mathbf{w}^\top\mathbf{x} + b = 0$, el margen
es $2/\|\mathbf{w}\|$, y maximizarlo equivale a

$$
\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2
\quad \text{sujeto a} \quad y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1 \;\; \forall i
$$

La solución depende **solo** de los puntos que quedan exactamente sobre el margen: los
**vectores de soporte**. Mover o quitar cualquier otro punto no cambia la frontera. Esa es
la diferencia estructural con la regresión logística, donde todos los puntos contribuyen al
gradiente (menos los que ya están muy bien clasificados, que contribuyen poco).

### Margen blando y el hiperparámetro $C$

Con datos no separables (todos los reales), se permite que algunos puntos violen el margen,
pagando una penalización $\xi_i \geq 0$ por cada uno:

$$
\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^n \xi_i
\quad \text{sujeto a} \quad y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1 - \xi_i
$$

$C$ controla el compromiso:

- $C$ **grande**: violar el margen es caro → margen estrecho que intenta clasificar bien todos
  los puntos de entrenamiento → **baja regularización, alta varianza**.
- $C$ **pequeño**: se toleran violaciones → margen amplio, frontera más suave → **alta
  regularización, alto sesgo**.

Es decir, $C$ juega el papel de $1/\lambda$, igual que en `LogisticRegression`. La función
de pérdida implícita es la *hinge loss* $\max(0, 1 - y_i f(\mathbf{x}_i))$: cero para los
puntos correctamente clasificados y fuera del margen, lineal para los demás.

### Kernels: fronteras no lineales sin construir el espacio

Si las clases no son separables por un hiperplano, se pueden mapear los datos a un espacio
de mayor dimensión $\phi(\mathbf{x})$ donde sí lo sean (por ejemplo, añadiendo $x_1^2, x_2^2,
x_1 x_2$ — la regresión polinómica de `03-multicolinealidad-polinomica.md` hacía lo mismo).
El **truco del kernel** es que la solución de la SVM solo necesita **productos punto**
$\phi(\mathbf{x}_i)^\top\phi(\mathbf{x}_j)$, nunca $\phi$ explícitamente. Una función kernel
$K(\mathbf{x}_i, \mathbf{x}_j)$ los calcula directamente:

| Kernel | $K(\mathbf{x}, \mathbf{x}')$ | Espacio implícito |
|---|---|---|
| Lineal | $\mathbf{x}^\top\mathbf{x}'$ | El original |
| Polinómico | $(\gamma\,\mathbf{x}^\top\mathbf{x}' + r)^d$ | Todos los monomios hasta grado $d$ |
| RBF (gaussiano) | $\exp(-\gamma\|\mathbf{x} - \mathbf{x}'\|^2)$ | Dimensión **infinita** |

El kernel RBF es el habitual por defecto. Su hiperparámetro $\gamma$ controla el alcance de
cada punto: $\gamma$ grande → cada vector de soporte influye solo en su vecindad inmediata →
frontera muy irregular (alta varianza); $\gamma$ pequeño → influencia amplia → frontera casi
lineal. **$C$ y $\gamma$ se afinan juntos**, típicamente en una rejilla logarítmica, y son
un caso natural para random search u Optuna (`06-seleccion-hiperparametros.md`).

### Probabilidades

La SVM no produce probabilidades: produce la **distancia con signo al hiperplano**
(`decision_function`). Para curvas ROC y PR basta con eso — solo hace falta un orden. Para
comparar umbrales en la misma escala que la logística, `SVC(probability=True)` ajusta una
regresión logística sobre esa distancia (calibración de Platt) con una validación cruzada
interna, lo que multiplica el tiempo de entrenamiento. La calibración de probabilidades en
general es un tema 🔵 opcional del módulo.

### Costos

Entrenar una SVM con kernel escala entre $O(n^2)$ y $O(n^3)$: es la más lenta de los tres
clasificadores de la sesión, y con más de unas decenas de miles de filas se vuelve poco
práctica (en `02-clasificacion-aplicado.ipynb`, con 4256 filas, tarda unos segundos por
ajuste frente a milisegundos de la logística). Para datos grandes, `LinearSVC` (sin kernel)
o directamente boosting (S11).

## 3. Los tres clasificadores de la sesión, lado a lado

| | Logística | KNN | SVM (RBF) |
|---|---|---|---|
| Frontera | Lineal | Local, arbitraria | No lineal, suave |
| Parámetros aprendidos | $p+1$ coeficientes | Ninguno (memoriza) | Vectores de soporte y sus pesos |
| Hiperparámetros | $C$ (regularización) | $k$, distancia | $C$, $\gamma$, kernel |
| Probabilidades | Sí, nativas | Sí (fracción de vecinos, granular) | No; Platt opcional |
| Interpretación | Razones de momios | Ninguna directa | Ninguna directa |
| Exige escalado | Sí (por la regularización) | Sí (por la distancia) | Sí (por la distancia) |
| Costo de predicción | $O(p)$ | $O(np)$ | $O(\#\text{soporte} \cdot p)$ |
| Costo de entrenamiento | Bajo | Nulo | Alto ($O(n^2)$–$O(n^3)$) |

Sobre Wine Quality (`02-clasificacion-aplicado.ipynb`), con validación cruzada estratificada,
los tres quedan en un AUC-ROC de 0.80–0.83 y una AP de 0.50–0.53. **Ninguno de los tres
domina**; la frontera no lineal de la SVM apenas se nota sobre la logística. La sesión 10
mostrará que los ensambles de árboles sí mueven esa cifra, y `06-interpretabilidad.md`
explicará qué encuentran en las variables que estos tres no.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| KNN | Memorizar y votar; $k$ es la perilla sesgo-varianza | Detector de duplicados; base de DBSCAN y de UMAP (S12) |
| Margen máximo | El hiperplano más robusto es el más lejano a las clases | — |
| Vectores de soporte | Solo los puntos del margen definen la frontera | — |
| $C$ y $\gamma$ | Regularización y alcance; se afinan juntos | Búsqueda de hiperparámetros del proyecto |
| Truco del kernel | Frontera no lineal sin construir el espacio | PCA con kernel (S12, 🔵) |

**Notebook:** `02-clasificacion-aplicado.ipynb`.

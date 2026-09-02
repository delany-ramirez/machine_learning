# 04 · Ingeniería de características

**Módulo 2 · Sesión 5**

> **Objetivos.** Escalar variables numéricas y saber cuándo hace falta; codificar variables
> categóricas con el método adecuado a cada caso; transformar distribuciones problemáticas;
> crear variables nuevas con criterio; y —lo más difícil— demostrar que las nuevas variables
> aportan algo.

## 1. Qué es

La ingeniería de características es el trabajo de **representar los datos de forma que el
modelo pueda aprovecharlos**. El mismo dataset, representado de dos maneras, produce modelos
muy distintos.

Es la parte del proceso donde más pesa el conocimiento del dominio y menos el algoritmo. Y
tiene una fama que conviene matizar desde el principio: se dice que es donde se gana la
partida, y a veces lo es — pero con frecuencia las variables que uno inventa **no mejoran
nada**, y demostrarlo requiere validación cruzada. La afirmación "esta variable ayuda"
necesita evidencia igual que cualquier otra.

## 2. Escalado

Muchos algoritmos son sensibles a la escala de las variables.

### Estandarización (*z-score*)

$$
z = \frac{x - \mu}{\sigma}
$$

Media 0 y desviación 1. Es la opción por defecto. `StandardScaler`.

### Normalización min-max

$$
x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
$$

Lleva al rango $[0, 1]$. Útil cuando se necesita un rango acotado, pero **muy sensible a los
extremos**: un solo valor atípico comprime todo lo demás. `MinMaxScaler`.

### Escalado robusto

Usa la mediana y el rango intercuartílico en vez de la media y la desviación. Resistente a
valores extremos. `RobustScaler`.

### ¿Qué modelos lo necesitan?

| Necesitan escalado | No lo necesitan |
|---|---|
| KNN, K-Means, DBSCAN (usan distancias) | Árboles de decisión |
| SVM (usa distancias y márgenes) | Random Forest, Gradient Boosting |
| Regresión con regularización (Ridge, Lasso) | Regresión lineal **sin** regularización |
| PCA | Naive Bayes |
| Redes neuronales (convergencia) | |

La razón es la misma en todos los casos de la izquierda: la escala distorsiona la geometría
del espacio o el efecto de la penalización. Los árboles, en cambio, solo comparan valores
dentro de cada variable, así que la escala les da igual.

> Ante la duda, escala. Nunca perjudica, y evita errores silenciosos.

## 3. Codificación de variables categóricas

Los modelos trabajan con números. Hay que convertir las categorías, y **el método importa**.

### One-hot

Una columna binaria por categoría. Es la opción por defecto para variables **nominales** (sin
orden).

| ciudad | ciudad_Cali | ciudad_Pereira |
|---|---|---|
| Bogotá | 0 | 0 |
| Cali | 1 | 0 |
| Pereira | 0 | 1 |

Dos parámetros que importan en producción:

- **`handle_unknown="ignore"`**: si aparece una categoría no vista en entrenamiento, la
  codifica como ceros en vez de fallar. Sin esto, tu API se cae el día que llegue un valor
  nuevo.
- **`drop="first"`**: elimina una categoría por variable. Evita la colinealidad perfecta entre
  las columnas generadas, que afecta a los modelos lineales. En árboles es indiferente.

Su límite es la **cardinalidad**: con 500 categorías genera 500 columnas, casi todas ceros.

### Ordinal

Asigna un entero a cada categoría. Solo es correcto cuando existe un **orden real**:
`bajo < medio < alto`. Aplicarlo a variables nominales le dice al modelo que Bogotá está
"entre" Cali y Pereira, lo cual es falso y produce errores sutiles.

### Otras codificaciones

- **Codificación por frecuencia.** Sustituye cada categoría por su frecuencia. Simple y útil
  con alta cardinalidad.
- **Codificación por objetivo (*target encoding*).** Sustituye cada categoría por la media del
  objetivo en esa categoría. Potente y **peligrosa**: usa la variable objetivo, así que
  produce fuga de datos si no se calcula dentro de la validación cruzada y con suavizado. Solo
  con `TargetEncoder` y dentro de un `Pipeline`.

### Alta cardinalidad

Con muchas categorías: agrupar las raras en "otros", usar codificación por frecuencia, o —si
el modelo lo soporta nativamente, como LightGBM— dejarlas como categóricas.

## 4. Transformaciones de distribución

| Transformación | Para qué | Nota |
|---|---|---|
| **Logaritmo** `np.log1p` | Comprimir colas derechas largas | `log1p` admite ceros |
| **Raíz cuadrada** | Asimetría moderada, conteos | Menos agresiva que el log |
| **Box-Cox / Yeo-Johnson** | Buscar automáticamente la mejor potencia | Yeo-Johnson admite negativos |
| **Discretización** (*binning*) | Convertir continua en rangos | Pierde información; captura no linealidad |

La transformación logarítmica es la más usada, para precios, ingresos, tiempos y tarifas.
Reduce la influencia de los extremos **sin perder ninguna observación**, que es su ventaja
frente a eliminarlos.

Un detalle de interpretación: tras aplicar un logaritmo, los coeficientes del modelo ya no se
leen en las unidades originales, sino en términos relativos.

## 5. Crear variables nuevas

Las fuentes habituales de ideas:

### Combinar

Sumas, diferencias, razones y productos de variables existentes.

- `tamano_familia = sibsp + parch + 1`
- `tarifa_por_persona = fare / tamano_familia`
- `densidad = poblacion / area`

Las **razones** suelen ser especialmente útiles, porque normalizan por tamaño. Y son
justamente las que un modelo lineal **no puede** construir por sí solo: sabe sumar variables,
no dividirlas.

> Al revés: `tamano_familia` es una suma, y una regresión lineal ya podía formarla con sus
> coeficientes. Crear variables que el modelo puede derivar solo rara vez ayuda.

### Descomponer

Extraer partes de una variable compleja:

- De una fecha: año, mes, día de la semana, si es festivo, días desde un evento.
- De un texto: longitud, número de palabras, presencia de un término.
- De una dirección: ciudad, barrio, coordenadas.

Las fechas son el caso más rentable: `2026-09-02` es casi inútil como número, pero
"miércoles", "septiembre" y "día 2 del semestre" pueden ser muy informativos.

### Indicadores

Variables binarias que marcan una condición: `es_menor_de_edad`, `tiene_camarote`,
`falta_edad`, `primera_compra`. Baratas y a menudo más útiles de lo que parecen.

### Agregaciones

Cuando hay varias filas por entidad: media, máximo, conteo, tendencia por grupo. **Cuidado**:
si la agregación usa el objetivo o incluye datos posteriores al momento de predecir, es fuga.

### Términos de interacción

Producto de dos variables, para que un modelo lineal capture que el efecto de una depende de
la otra: `sexo × clase` en el Titanic. `PolynomialFeatures` los genera automáticamente, con el
riesgo de generar demasiados.

## 6. La regla de seguridad

No todas las transformaciones son igual de peligrosas:

| Tipo | Ejemplo | ¿Puede aplicarse antes de partir? |
|---|---|---|
| **Fila a fila** | `log(fare)`, `sibsp + parch`, extraer el mes | **Sí**: solo mira la propia fila |
| **Aprende del dataset** | Media para imputar, $\mu$ y $\sigma$ del escalado, categorías del codificador | **No**: va dentro del `Pipeline` |

La pregunta que decide: **¿esta transformación necesita mirar otras filas?** Si la respuesta
es sí, va en el `Pipeline`. Si dudas, va en el `Pipeline` igualmente — no cuesta nada.

## 7. Demostrar que una variable ayuda

Este es el paso que se salta casi siempre.

1. Establecer una **línea base** con las variables originales.
2. Añadir la variable nueva.
3. Comparar con **validación cruzada**, no con una sola partición.
4. Mirar la mejora **frente a la variabilidad entre pliegues**.

Si la diferencia es menor que la desviación entre pliegues, **no hay mejora demostrada**. Es
ruido, y reportarlo como mejora es una forma sutil de engañarse.

En el notebook 04, cuatro variables nuevas sobre el Titanic —construidas con buen criterio a
partir del EDA— no producen ninguna mejora medible. No es un fracaso del método: es el
resultado honesto, y saber reconocerlo es parte del oficio.

## Para recordar

- La representación de los datos importa tanto como el algoritmo.
- Escala siempre que uses distancias, márgenes o regularización; los árboles no lo necesitan.
- One-hot para nominales (con `handle_unknown="ignore"`), ordinal solo si hay orden real.
- El *target encoding* usa el objetivo: solo dentro del `Pipeline`.
- El logaritmo domestica colas largas sin perder observaciones.
- Las razones aportan lo que un modelo lineal no puede construir solo; las sumas, poco.
- Transformación fila a fila: segura. Transformación que aprende del dataset: al `Pipeline`.
- Una variable nueva no vale nada hasta que la validación cruzada demuestra que aporta.

## Notebooks relacionados

- [`../notebooks/04-pipeline-caracteristicas-aplicado.ipynb`](../notebooks/04-pipeline-caracteristicas-aplicado.ipynb)
  — todo lo anterior implementado, incluida la comparación honesta que sale negativa.

## Documento siguiente

- [`05-seleccion-y-pipelines.md`](05-seleccion-y-pipelines.md) — selección y fuga de datos.

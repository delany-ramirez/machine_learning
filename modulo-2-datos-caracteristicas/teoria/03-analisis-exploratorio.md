# 03 · Análisis exploratorio de datos (EDA)

**Módulo 2 · Sesión 4**

> **Objetivos.** Entender el EDA como una fase de decisiones, no de gráficas; saber qué mirar
> en el análisis univariante, bivariante y multivariante; interpretar correlaciones sin caer
> en las trampas habituales; y terminar el EDA con una lista de acciones concretas.

## 1. Qué es y qué no es

El análisis exploratorio busca **entender los datos antes de modelarlos**. Su producto no es
un cuaderno lleno de gráficas: es una lista de decisiones justificadas sobre cómo tratar cada
variable y qué esperar del problema.

Tres preguntas lo guían:

1. **¿Qué hay?** Distribuciones, rangos, categorías, calidad.
2. **¿Qué se relaciona con qué?** En particular, con la variable objetivo.
3. **¿Qué problemas hay?** Faltantes, extremos, redundancias, fugas.

> El EDA es también donde se detecta que el proyecto no es viable. Si ninguna variable se
> relaciona con el objetivo, mejor saberlo ahora que después de tres semanas de modelado.

## 2. Análisis univariante

Una variable a la vez.

### Numéricas

Estadísticos: media, mediana, desviación, cuartiles, mínimo y máximo (`describe()`).
Visualización: histograma para la forma, diagrama de caja para los extremos.

Qué buscar:

- **Forma de la distribución.** ¿Simétrica, asimétrica, bimodal? Una distribución bimodal
  suele indicar dos poblaciones mezcladas — y a menudo revela una variable de agrupación que
  faltaba.
- **Asimetría.** Ingresos, precios y tiempos suelen tener cola derecha larga. Candidatos a
  transformación logarítmica.
- **Valores imposibles.** Negativos donde no puede haberlos, porcentajes mayores que 100.
- **Concentraciones sospechosas.** Un pico en un valor concreto (0, 999) suele delatar
  faltantes disfrazados.

La **media y la mediana** juntas dicen mucho: si difieren bastante, hay asimetría o extremos.

### Categóricas

Frecuencias absolutas y relativas (`value_counts()`). Visualización: gráfico de barras.

Qué buscar:

- **Cardinalidad.** Una variable con 500 categorías distintas necesita un tratamiento especial
  (agrupar, o codificaciones distintas de one-hot).
- **Categorías raras.** Un nivel con 2 observaciones no permite aprender nada y complica la
  validación cruzada. Suelen agruparse en "otros".
- **Inconsistencias.** `"Pereira"`, `"pereira"` y `" PEREIRA "` son la misma ciudad y tres
  categorías.
- **Desbalance** en la variable objetivo, si es categórica: condiciona la métrica y la
  estrategia de modelado (sesión 9).

## 3. Análisis bivariante

Dos variables, y sobre todo **cada variable frente al objetivo**. Es la parte más informativa
del EDA.

| Tipo de par | Herramienta |
|---|---|
| Numérica vs. numérica | Diagrama de dispersión; correlación |
| Numérica vs. categórica | Diagramas de caja por categoría; medias por grupo |
| Categórica vs. categórica | Tabla de contingencia; barras agrupadas |
| Cualquiera vs. objetivo | Tasa del objetivo por grupo o por rango |

La operación más útil del EDA en un problema de clasificación es simple:

```python
df.groupby("variable")["objetivo"].agg(["mean", "count"])
```

La tasa del objetivo por grupo, con el número de observaciones al lado. **Siempre con el
conteo**: una tasa del 100 % sobre 3 observaciones no significa nada.

## 4. Correlación: cuatro trampas

Para dos variables numéricas, el coeficiente de Pearson mide la **asociación lineal**:

$$
\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1]
$$

Cuatro errores frecuentes al interpretarlo:

1. **Correlación no implica causalidad.** El caso más citado del curso: en el Titanic, la
   tarifa correlaciona con la supervivencia, pero pagar más no salvaba a nadie — la clase
   determinaba la ubicación en el barco y el acceso a los botes.
2. **Pearson solo ve relaciones lineales.** Una relación en forma de U da correlación cercana
   a cero. La edad y la supervivencia en el Titanic son un ejemplo: sobrevivieron más los
   niños y, en menor medida, los mayores, y la correlación global es apenas $-0.077$. **Hay
   que mirar la gráfica, no solo el número.** Para relaciones monótonas no lineales,
   Spearman es preferible.
3. **Es sensible a los extremos.** Unos pocos puntos alejados pueden crear o destruir una
   correlación.
4. **Correlación entre predictoras es un problema aparte.** No dice nada sobre la utilidad de
   las variables, sino que anticipa **multicolinealidad**: coeficientes inestables en modelos
   lineales (sesión 7).

Un mapa de calor de correlaciones sirve para dos cosas distintas: ver qué se relaciona con el
objetivo (última fila) y detectar redundancia entre predictoras (el resto de la matriz).

## 5. Análisis multivariante: las interacciones

Aquí es donde el EDA aporta lo que ningún resumen automático da.

Una **interacción** ocurre cuando el efecto de una variable depende del valor de otra. En el
Titanic:

| | 1.ª clase | 2.ª clase | 3.ª clase |
|---|---|---|---|
| **Mujeres** | 96.8 % | 92.1 % | 50.0 % |
| **Hombres** | 36.9 % | 15.7 % | 13.5 % |

Ser mujer aumentaba la supervivencia en todas las clases, pero **la magnitud del efecto
cambia radicalmente**: de 60 puntos en primera a 36 en tercera. El efecto del sexo no es
independiente de la clase.

Esto tiene consecuencias directas de modelado:

- Un modelo **aditivo** (regresión lineal o logística sin términos de interacción) no puede
  representar esto. Hay que añadir el término de interacción explícitamente (sesión 7).
- Los **árboles y ensambles** capturan interacciones de forma automática, porque cada rama
  condiciona sobre las anteriores. Es una de las razones por las que dominan en datos
  tabulares (sesiones 10 y 11).

Detectar interacciones en el EDA es lo que informa la elección del modelo.

## 6. Visualización: unas pocas reglas

- **Una gráfica debe responder una pregunta.** Si no sabes cuál, no la hagas.
- **Elige el tipo según los datos**, no según lo que se ve bonito: histograma para
  distribuciones, dispersión para relaciones, barras para categorías, líneas solo para
  series temporales.
- **Etiqueta los ejes**, con unidades. Una gráfica sin etiquetas no es interpretable.
- **Evita los gráficos de torta** con más de tres categorías: comparar ángulos es más difícil
  que comparar longitudes.
- **No empieces el eje Y en un valor arbitrario** para exagerar diferencias.
- **Muestra el tamaño de los grupos** cuando compares tasas.

## 7. El resultado del EDA

Un EDA termina en una tabla de decisiones. Del notebook 01 sobre el Titanic:

| Decisión | Justificación |
|---|---|
| Eliminar `alive` | Fuga de datos: es el objetivo en texto |
| Eliminar `class`, `embark_town`, `adult_male` | Redundantes |
| Imputar `age` por mediana de la clase | Faltante MAR |
| Añadir indicador `falta_edad` | La ausencia es informativa |
| Convertir `deck` en binaria | 77 % faltante, MNAR |
| **No** eliminar duplicados | Sin ID, filas iguales ≠ registros repetidos |
| **No** eliminar extremos de `fare` | Valores legítimos |
| Transformar `fare` con logaritmo | Asimetría fuerte |
| Considerar interacción sexo × clase | Detectada en el análisis multivariante |

Ese es el entregable. Las gráficas son el medio.

## Para recordar

- El EDA produce decisiones, no gráficas.
- Univariante: forma, extremos, cardinalidad, faltantes disfrazados.
- Bivariante: la tasa del objetivo por grupo, siempre con el conteo al lado.
- La correlación de Pearson solo ve lo lineal, y no implica causalidad.
- Las interacciones detectadas en el EDA determinan qué familia de modelos conviene.
- Si ninguna variable se relaciona con el objetivo, el EDA acaba de ahorrarte semanas.

## Notebooks relacionados

- [`../notebooks/01-limpieza-eda-aplicado.ipynb`](../notebooks/01-limpieza-eda-aplicado.ipynb)
  — EDA completo del Titanic, incluida la interacción sexo × clase.

## Documento siguiente

- [`04-ingenieria-caracteristicas.md`](04-ingenieria-caracteristicas.md) — construir variables.

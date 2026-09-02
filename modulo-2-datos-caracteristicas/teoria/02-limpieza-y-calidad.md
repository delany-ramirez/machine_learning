# 02 · Limpieza y calidad de datos

**Módulo 2 · Sesión 4**

> **Objetivos.** Diagnosticar la calidad de un dataset; entender los tres mecanismos de datos
> faltantes y elegir la imputación adecuada a cada uno; decidir con criterio sobre duplicados
> y valores extremos; y —sobre todo— dejar de aplicar recetas automáticas.

## 1. El principio que gobierna todo el documento

> **La limpieza de datos no es un procedimiento, es una serie de decisiones justificadas.**

`df.dropna()` y `df.drop_duplicates()` son dos líneas que pueden destruir un dataset en
silencio. No fallan, no avisan: simplemente hacen que el resultado sea otro. Cada decisión de
limpieza debe poder explicarse, y algunas veces la decisión correcta es **no hacer nada**.

## 2. Valores faltantes

### Los tres mecanismos

La clasificación es de Rubin (1976) y determina qué imputación es válida.

| Mecanismo | Significa | Ejemplo |
|---|---|---|
| **MCAR** (*Missing Completely At Random*) | La ausencia no depende de nada | Un sensor falló al azar |
| **MAR** (*Missing At Random*) | Depende de **otras variables observadas** | La edad falta más en tercera clase, y la clase se conoce |
| **MNAR** (*Missing Not At Random*) | Depende del **propio valor ausente** | Los pasajeros sin camarote no tienen cubierta registrada |

La distinción no es académica:

- Con **MCAR**, cualquier imputación razonable funciona y eliminar filas no sesga (aunque
  pierde información).
- Con **MAR**, hay que imputar **condicionando** a las variables de las que depende la
  ausencia. Imputar con la media global sesga.
- Con **MNAR**, ninguna imputación es realmente válida. Lo correcto suele ser **modelar la
  ausencia** como información en sí misma.

### Cómo saber cuál es

MCAR y MAR se distinguen empíricamente: se crea un indicador binario de ausencia y se examina
si se relaciona con las demás variables o con el objetivo.

```python
falta = df["age"].isna()
df.groupby("pclass")[["age"]].apply(lambda g: g.isna().mean())
df.groupby(falta)["survived"].mean()
```

Si la tasa de ausencia varía entre grupos, no es MCAR. MNAR no se puede demostrar con los
datos —por definición, depende de lo que no observamos— y se argumenta desde el conocimiento
del dominio.

### Estrategias

| Estrategia | Cuándo | Riesgo |
|---|---|---|
| **Eliminar filas** | Muy pocos faltantes, MCAR | Perder información; sesgar si no es MCAR |
| **Eliminar la columna** | Altísimo % faltante y poca señal | Perder una variable útil |
| Imputar con **media/mediana** | Numéricas, MCAR | Reduce la varianza; distorsiona la distribución |
| Imputar con la **moda** | Categóricas con pocos faltantes | Refuerza artificialmente la categoría dominante |
| Imputar **por grupo** | MAR | Requiere identificar la variable de agrupación |
| Imputar con un **modelo** (KNN, iterativa) | MAR, relaciones fuertes | Costoso; puede propagar errores |
| **Categoría "desconocido"** | Categóricas, MNAR | — |
| **Indicador de ausencia** | Cuando faltar es informativo | Ninguno relevante; casi siempre vale la pena |

> **El indicador de ausencia.** Añadir una columna binaria `falta_x` conserva la señal
> contenida en el hecho de que falte, que de otro modo se pierde al imputar. Es barato y a
> menudo más informativo que el valor imputado. `SimpleImputer(add_indicator=True)` lo hace
> automáticamente.

### El error que hay que evitar

Calcular la media, mediana o moda de imputación **sobre todo el dataset**. Esas estadísticas
deben aprenderse solo del conjunto de entrenamiento, dentro de un `Pipeline`. Es fuga de
datos, aunque —como se mide en el notebook 03— su efecto sea pequeño comparado con otras.

## 3. Duplicados

La reacción refleja ante filas idénticas es eliminarlas. Antes hay que preguntarse algo:

> ¿Son **registros repetidos** o son **observaciones distintas que coinciden en todos los
> valores**?

No es lo mismo, y la respuesta depende de si existe un identificador:

| Situación | Interpretación | Acción |
|---|---|---|
| Hay ID y se repite | Registro duplicado | Eliminar |
| Hay ID y no se repite | Coincidencia de valores | **Conservar** |
| No hay ID | Indeterminado | Investigar el origen antes de decidir |

En el dataset del Titanic aparecen 107 filas idénticas. No hay columna de nombre ni de
identificador: dos hombres de tercera clase, ambos de 25 años, que viajaban solos y pagaron la
misma tarifa producen filas iguales **siendo personas distintas**. Eliminarlas descartaría 107
pasajeros reales y sesgaría el dataset justo hacia el perfil más frecuente.

Además hay duplicados que no son exactos: la misma entidad escrita de dos formas
(`"Universidad Tecnológica de Pereira"` y `"UTP"`). Detectarlos requiere normalizar el texto y,
a veces, comparación difusa.

## 4. Valores extremos (outliers)

### Cómo se detectan

**Regla del rango intercuartílico (IQR).** Se considera extremo lo que cae fuera de

$$
[\,Q_1 - 1.5\,\text{IQR},\ \ Q_3 + 1.5\,\text{IQR}\,]
$$

Es robusta y no supone normalidad.

**Puntuación $z$.** Se marca lo que se aleja más de 3 desviaciones estándar:

$$
z = \frac{x - \mu}{\sigma}
$$

Supone distribución aproximadamente normal, y tiene un problema circular: los propios outliers
inflan $\sigma$ y se enmascaran entre sí. Existe una versión robusta basada en la mediana y la
desviación absoluta mediana (MAD).

También hay métodos multivariantes (distancia de Mahalanobis, Isolation Forest), que detectan
observaciones extrañas por la **combinación** de sus valores aunque ninguno lo sea por
separado.

### Los tres tipos, y qué hacer con cada uno

| Tipo | Qué es | Acción |
|---|---|---|
| **Error de medición o registro** | Edad de 200 años, precio negativo | Corregir si se puede; si no, tratar como faltante |
| **Valor legítimo extremo** | Una tarifa de primera clase 35 veces mayor que la mediana | **Conservar**: suele ser señal, no ruido |
| **Observación de otra población** | Un tripulante en un dataset de pasajeros | Documentar y decidir si pertenece al problema |

> **La detección de outliers es estadística; la decisión sobre ellos es del dominio.** Un
> algoritmo señala candidatos; solo quien entiende el problema sabe si son errores o son la
> parte más interesante de los datos.

En el Titanic, la regla del IQR marca como outlier a un bebé de cinco meses. Eliminarlo sería
borrar a los bebés del dataset — precisamente el grupo con mayor prioridad de rescate.

### Alternativas a eliminar

- **Transformar.** El logaritmo comprime colas largas sin perder observaciones. Es lo indicado
  para variables con asimetría fuerte como precios o ingresos.
- **Winsorizar.** Recortar los valores extremos al percentil 1 y 99. Conserva la fila y limita
  la influencia.
- **Usar modelos robustos.** Los árboles y los ensambles son insensibles a los valores
  extremos; la regresión lineal no.

## 5. Otros problemas de calidad

| Problema | Ejemplo | Detección |
|---|---|---|
| Inconsistencia de formato | `"Pereira"`, `"pereira"`, `" PEREIRA "` | `value_counts()` tras normalizar |
| Unidades mezcladas | Precios en pesos y en dólares en la misma columna | Distribución bimodal sospechosa |
| Valores imposibles | Edad negativa, porcentaje > 100 | Comprobación de rango |
| Faltantes disfrazados | `"N/D"`, `-999`, `0` como "sin dato" | `value_counts()` sobre valores raros |
| Categorías raras | Un nivel con 2 observaciones de 900 | `value_counts()`; agrupar en "otros" |
| Tipos incorrectos | Fechas como texto, códigos como enteros | `df.info()` |

El caso de **`0` como faltante** merece atención: no lo detecta ningún `isna()`, y arrastra
todas las medias hacia abajo sin que nada avise.

## 6. Un procedimiento razonable

1. **Perfilar.** `shape`, `info()`, `describe()`, `isna().sum()`, `value_counts()` de cada
   categórica.
2. **Documentar** el diccionario de datos, incluida la disponibilidad temporal.
3. **Buscar redundancia y fugas** entre columnas (correlaciones perfectas, tablas cruzadas).
4. **Diagnosticar los faltantes**: cuántos, dónde y de qué dependen.
5. **Revisar duplicados**, preguntando si hay identificador.
6. **Examinar los extremos** uno por uno, no en bloque.
7. **Decidir y justificar** cada acción, por escrito.
8. **Aplicar dentro de un `Pipeline`** todo lo que aprenda algo de los datos.

El paso 8 es el que separa un análisis honesto de uno que se engaña a sí mismo.

## Para recordar

- La limpieza es una serie de decisiones justificadas, no una receta.
- MCAR, MAR y MNAR determinan qué imputación es válida; identificar el mecanismo es parte del
  trabajo.
- Que un dato falte suele ser informativo: guarda el indicador.
- Filas iguales no son necesariamente registros duplicados.
- Un valor extremo puede ser un error, una observación legítima o de otra población; solo el
  dominio lo distingue.
- Todo lo que se aprende de los datos se aprende **solo del entrenamiento**.

## Notebooks relacionados

- [`../notebooks/01-limpieza-eda-aplicado.ipynb`](../notebooks/01-limpieza-eda-aplicado.ipynb)
  — diagnóstico completo del Titanic y las decisiones que se derivan.

## Documento siguiente

- [`03-analisis-exploratorio.md`](03-analisis-exploratorio.md) — EDA.

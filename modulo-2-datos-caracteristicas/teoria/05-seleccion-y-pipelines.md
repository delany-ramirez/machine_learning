# 05 · Selección de características, `Pipeline` y fuga de datos

**Módulo 2 · Sesión 5**

> **Objetivos.** Conocer los tres enfoques de selección de características y cuándo hace falta
> alguno; construir pipelines con `ColumnTransformer`; y entender la fuga de datos con sentido
> de la proporción: cuáles son graves de verdad y cuáles no.

## 1. Selección de características

### Por qué seleccionar

- **Reducir la dimensionalidad.** Con muchas variables y pocas observaciones, el modelo
  encuentra patrones espurios.
- **Mejorar la interpretabilidad.** Un modelo con 8 variables se explica; uno con 800, no.
- **Reducir el coste** de cómputo, almacenamiento y recolección. En producción, cada variable
  es un dato que hay que conseguir cada vez.
- **Eliminar ruido** y redundancia.

Conviene decirlo pronto: **la selección de características resuelve un problema de
dimensionalidad**. Si tienes 15 variables y 900 observaciones, probablemente no tienes ese
problema, y seleccionar no mejorará nada. Es una herramienta para cuando $p$ se acerca a $n$ o
lo supera.

### Los tres enfoques

| Enfoque | Cómo decide | Coste | Ventaja | Inconveniente |
|---|---|---|---|---|
| **Filtro** | Estadístico por variable, ignora el modelo | Bajo | Rápido, independiente del modelo | Ignora interacciones entre variables |
| **Envoltura** (*wrapper*) | Entrena el modelo repetidamente | Alto | Considera al modelo real | Costoso; riesgo de sobreajuste |
| **Embebido** | La selección forma parte del entrenamiento | Medio | Eficiente y natural | Atado a un tipo de modelo |

### Filtro

Se evalúa cada variable por separado con un estadístico y se conservan las mejores.

`SelectKBest` con distintas funciones de puntuación:

| Función | Para |
|---|---|
| `f_classif` | Clasificación, variables numéricas (ANOVA F) |
| `f_regression` | Regresión, variables numéricas |
| `chi2` | Clasificación, variables no negativas |
| `mutual_info_classif` | Captura relaciones **no lineales** |

Su limitación es estructural: evalúa cada variable **aislada**. Dos variables inútiles por
separado pueden ser muy informativas juntas, y un filtro las descartará. También conserva
variables redundantes entre sí, porque cada una puntúa bien.

### Envoltura

**RFE** (*Recursive Feature Elimination*): entrena el modelo, elimina la variable menos
importante, y repite hasta llegar al número deseado.

Considera el modelo real y las interacciones, pero exige entrenar muchas veces. `RFECV` elige
además el número óptimo de variables por validación cruzada.

### Embebido

La selección ocurre durante el entrenamiento:

- **Lasso** ($L_1$) lleva coeficientes exactamente a cero (sesión 7). La geometría de la norma
  $L_1$ —sus esquinas sobre los ejes— es la razón; se vio en el módulo 1.
- **Importancia de árboles**: los ensambles asignan una importancia a cada variable.

> **Advertencia sobre la importancia de árboles.** Está sesgada hacia variables con muchos
> valores distintos, y reparte el crédito de forma arbitraria entre variables correlacionadas.
> En el notebook 04, el sexo —la variable más determinante del Titanic— aparece dividido en
> tres columnas y por debajo de `age`. **No la uses para descartar variables.** La sesión 11
> presenta alternativas fiables (*permutation importance*, SHAP).

## 2. `Pipeline` y `ColumnTransformer`

### El problema

Un flujo típico tiene varios pasos: imputar, escalar, codificar, seleccionar, modelar. Hechos
por separado, hay que recordar aplicar exactamente lo mismo —con los mismos parámetros
aprendidos— al conjunto de prueba y, después, en producción. Es fácil equivocarse, y el error
no avisa.

### La solución

`Pipeline` encadena los pasos en un solo objeto:

```python
flujo = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),
    ("escalar", StandardScaler()),
    ("modelo", LogisticRegression()),
])
flujo.fit(X_entrena, y_entrena)
flujo.predict(X_prueba)
```

Lo que garantiza:

- `.fit()` ejecuta `fit_transform` en cada paso, **solo con los datos de entrenamiento**.
- `.predict()` ejecuta únicamente `transform`, con lo aprendido antes.
- Dentro de `cross_val_score`, todo eso ocurre **por separado en cada pliegue**.

Es decir: el `Pipeline` no es una cuestión de elegancia, es **lo que hace honesta la
evaluación**.

### `ColumnTransformer`

Las numéricas y las categóricas necesitan tratamientos distintos. `ColumnTransformer` aplica
un pipeline a cada grupo de columnas y concatena el resultado:

```python
preprocesador = ColumnTransformer([
    ("num", flujo_numerico,   ["age", "fare"]),
    ("cat", flujo_categorico, ["sex", "embarked"]),
], remainder="drop")
```

`remainder="drop"` descarta lo no listado. Es preferible a `"passthrough"` porque obliga a
decidir explícitamente sobre cada columna.

### El artefacto que se despliega

Lo que se guarda con `joblib` y se expone como API **no es el modelo: es el pipeline
completo**. Contiene las medianas de imputación, las medias y desviaciones del escalado, las
categorías del codificador y los coeficientes. Sin eso, en producción no se puede reproducir
el preprocesamiento. Es lo que haremos en la sesión 14.

## 3. Fuga de datos

**Fuga de datos** (*data leakage*) es que información no disponible en el momento de predecir
se cuele en el entrenamiento. El síntoma es siempre el mismo: métricas excelentes en el
experimento, fracaso en producción.

Es difícil de detectar porque **no produce errores, produce buenas noticias**.

### Los tipos, ordenados por gravedad real

La ordenación no es una opinión: en el notebook 03 se mide el sobreoptimismo de cada uno
promediando sobre 100 particiones.

| Tipo | Cómo se cuela | Sobreoptimismo | Solución |
|---|---|---|---|
| **Variable derivada del objetivo** | Columna que codifica la respuesta | Hasta accuracy = 1.000 | Diccionario de datos |
| **Variable del futuro** | Datos posteriores al hecho a predecir | Muy alto | ¿Qué se sabe al predecir? |
| **Selección de características** | Seleccionar mirando todo el dataset | **+0.09 a +0.13** medido | Selección dentro del `Pipeline` |
| **Temporal** | Partición aleatoria con datos ordenados | Alto | `TimeSeriesSplit` |
| **Por grupos** | Un mismo sujeto en entrenamiento y prueba | Alto | `GroupKFold` |
| **Imputación** | Estadísticos sobre todo el dataset | No medible en el experimento | `SimpleImputer` en el `Pipeline` |
| **Escalado** | $\mu$ y $\sigma$ sobre todo el dataset | No medible en el experimento | `StandardScaler` en el `Pipeline` |

### La lección de las magnitudes

Suele enseñarse que estandarizar antes de partir es un pecado grave. Medido, el sesgo es
indistinguible de cero. Lo que sí es devastador es la selección de características fuera de la
validación: en un experimento con **ruido puro** —donde no hay absolutamente nada que
aprender— seleccionar 20 de 10.000 variables aleatorias mirando todo el dataset produce un 81 %
de accuracy en validación cruzada. Hecho correctamente, da 46 %, que es lo que corresponde.

La explicación está en **cuánta información sobre el objetivo se filtra**. El escalado filtra
dos números por variable, que además no dicen nada sobre $y$. La selección filtra *qué
variables se parecen a la respuesta*: información directamente sobre el objetivo.

> Esto **no** autoriza a escalar fuera del pipeline —sigue siendo incorrecto y corregirlo es
> gratis— pero sí da sentido de la proporción. Si un modelo funcionó en el experimento y
> fracasó en producción, el culpable casi nunca es el escalador.

Y una advertencia sobre esa medición: vale para el escenario medido. Con muestras muy
pequeñas, extremos en el conjunto de prueba o transformaciones más agresivas
(`PowerTransformer`, PCA, discretización por cuantiles), el sesgo del preprocesamiento crece.
La conclusión robusta no es "el escalado da igual", sino que **la gravedad depende de cuánta
información sobre el objetivo se filtra**.

## 4. Lista de verificación

Antes de creerte cualquier resultado:

- [ ] ¿Se partieron los datos **antes** de cualquier transformación que aprenda algo?
- [ ] ¿Está todo el preprocesamiento dentro de un `Pipeline`?
- [ ] ¿La selección de características ocurre **dentro** de la validación cruzada?
- [ ] ¿Cada variable predictora existirá en el momento real de predecir?
- [ ] ¿Alguna variable se calcula a partir del objetivo, aunque sea indirectamente?
- [ ] Si hay tiempo, ¿la partición respeta el orden cronológico?
- [ ] Si hay sujetos repetidos, ¿se agruparon con `GroupKFold`?
- [ ] ¿Hay alguna variable con una asociación desmedida con el objetivo?
- [ ] Si el resultado parece demasiado bueno, **¿lo investigaste?**

> **La regla que resume el módulo.** Cuando una métrica sale sospechosamente buena, la
> explicación más probable no es que tu modelo sea excelente: es que hay una fuga. Un resultado
> demasiado bueno merece más escrutinio que uno malo, no menos.

## Para recordar

- La selección de características resuelve un problema de dimensionalidad; si no lo tienes, no
  la necesitas.
- Filtro, envoltura y embebido: rápido e ingenuo, caro y fiel, o integrado en el modelo.
- La importancia de árboles no sirve para descartar variables.
- El `Pipeline` es lo que hace honesta la evaluación, y es el artefacto que se despliega.
- No todas las fugas pesan igual: selección, variables del futuro y variables derivadas del
  objetivo son las graves.
- Un resultado demasiado bueno es una alarma, no un logro.

## Notebooks relacionados

- [`../notebooks/03-fuga-de-datos-intuicion.ipynb`](../notebooks/03-fuga-de-datos-intuicion.ipynb)
  — la medición del sobreoptimismo de cada tipo de fuga.
- [`../notebooks/04-pipeline-caracteristicas-aplicado.ipynb`](../notebooks/04-pipeline-caracteristicas-aplicado.ipynb)
  — `ColumnTransformer`, selección y despliegue del artefacto.

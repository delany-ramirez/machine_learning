# Solución · Ejercicio 02 · Pipeline, características y fuga

> **Material del docente.** Números obtenidos ejecutando la solución de referencia sobre
> `matriculas-sucio.csv` (`SEMILLA = 7` en la generación, `random_state = 42` en el modelado).
> Pequeñas variaciones son esperables si el estudiante define las características de otra
> forma; lo evaluable es el razonamiento.

## Datos tras la limpieza estructural

| Medida | Valor |
|---|---|
| Filas tras eliminar duplicados reales | **608** (de 620) |
| Variables predictoras | 10 |
| Tasa de admisión | 0.720 |

## Parte A — El pipeline

**A.1** Se eliminan:

- `admitido_texto`: **fuga de datos**, es el objetivo en texto.
- `id_solicitud`: identificador sin contenido informativo. Si el modelo le encontrara señal
  sería memorización.

**A.2** Partición estratificada del 20 %, **antes de todo lo demás**.

**A.3** La función es segura porque **cada variable se calcula mirando únicamente la propia
fila**: `notna()`, `isna()`, un logaritmo y extraer el mes. No interviene ningún estadístico
del conjunto (media, mediana, conteo global). Por eso no puede filtrar información del
conjunto de prueba.

Contraejemplo útil para clase: `ingresos_relativos = ingresos / ingresos.mean()` **sí** sería
fuga, porque la media se calcula sobre todas las filas.

**A.5 — Resultado**

| Modelo | Accuracy CV |
|---|---|
| Pipeline completo | **0.7881** (±0.0310) |
| Referencia trivial (clase mayoritaria) | 0.7202 |

El modelo supera a la referencia en ~6.8 puntos. Es una mejora real pero modesta, y conviene
señalarlo: con una tasa de admisión del 72 %, la accuracy es una métrica poco exigente.

## Parte B — La fuga evidente

**B.1–B.2**

| | Accuracy CV |
|---|---|
| Sin `admitido_texto` | 0.7881 |
| **Con `admitido_texto`** | **1.0000** |

Accuracy perfecta. Sin conocer el significado de la columna, la conclusión sería que el modelo
es extraordinario. En realidad es inútil: para predecir si alguien será admitido necesita saber
si fue admitido.

**B.3**

```python
def detectar_sospechosas(X, y, umbral=0.95):
    numericas = X.select_dtypes(include=[np.number])
    correlaciones = numericas.apply(lambda c: c.corr(y)).abs()
    return correlaciones[correlaciones > umbral].sort_values(ascending=False)
```

Detecta `admitido_texto_num` con correlación 1.000.

**Por qué debe ser rutinaria:** cuesta una línea y detecta el tipo de fuga más grave.

**Cuál es su límite** — esto es lo evaluable:

- Solo ve relaciones **lineales** y solo en variables **numéricas**.
- Una fuga puede estar repartida entre varias variables, sin que ninguna destaque.
- Una fuga temporal o por grupos **no produce ninguna correlación alta**: el problema está en
  cómo se parten los datos, no en una columna.

Es un filtro barato, no una garantía. La garantía es el diccionario de datos con la
disponibilidad temporal.

## Parte C — Cuánto importa el orden

**C.1–C.2 — Preprocesamiento fuera del pipeline**

| | Accuracy CV |
|---|---|
| Imputar y escalar dentro del `Pipeline` | 0.7881 |
| Imputar y escalar **fuera** | 0.7881 |

**Diferencia: +0.0000.** Ninguna.

Es el mismo resultado del notebook 03: el sesgo por escalado e imputación es indistinguible de
cero. Con 608 observaciones, las medianas y desviaciones calculadas sobre el total son
prácticamente idénticas a las del entrenamiento.

**C.3 — Selección de características**

| | Accuracy CV |
|---|---|
| `SelectKBest(k=5)` **fuera** del pipeline | 0.7901 |
| `SelectKBest(k=5)` **dentro** del pipeline | 0.7798 |

**Diferencia: +0.0103.** Un punto de sobreoptimismo.

**C.4 — La ordenación y, sobre todo, la explicación**

Orden por gravedad medida:

1. Variable derivada del objetivo (`admitido_texto`): **+0.21**, hasta accuracy = 1.
2. Selección de características fuera del pipeline: **+0.01**.
3. Escalado e imputación fuera del pipeline: **0.00**.

Coincide con el notebook 03 en el orden. Pero el efecto de la selección aquí es de 1 punto,
frente a los 9–13 del notebook. **La explicación es la clave del apartado:**

> El sobreoptimismo de la selección depende de **cuántas variables candidatas hay**. En el
> notebook 03 se elegían 20 de 10.000 variables aleatorias: con tantas candidatas, por puro
> azar algunas se parecen a la etiqueta y el selector las encuentra. Aquí se eligen 5 de unas
> 15 variables **reales, con señal genuina**: hay poco margen para que el azar produzca falsos
> hallazgos, y las que el selector elige son las que de verdad importan tanto dentro como
> fuera del pliegue.

La regla general que debe quedar: **el riesgo de esta fuga crece con la relación $p/n$**. Con
pocas variables y muchas observaciones, es menor; con más variables que observaciones —datos
genómicos, texto, sensores— es devastador.

> Sigue siendo obligatorio meter la selección en el `Pipeline`: no cuesta nada y el día que el
> dataset tenga 2.000 columnas, el código ya está bien.

## Parte D — ¿Aportan las variables nuevas?

**D.1–D.2** Las diferencias entre la versión con y sin variables nuevas son del orden de la
desviación entre pliegues (±0.031). **No se puede afirmar que ayuden.**

Respuesta correcta esperada: *"la diferencia observada es menor que la variabilidad entre
pliegues, así que no hay evidencia de mejora"*. Se penaliza afirmar una mejora a partir de una
diferencia en la tercera cifra decimal.

De las cuatro variables:

- `fue_entrevistado` es la que más aporta (aparece con coeficiente alto en E.2).
- `log_ingresos` es una transformación monótona de `ingresos_hogar`, que ya estaba: poco que
  añadir.
- `falta_ingresos` y `mes_solicitud` capturan poco en este dataset.

**D.3** Se acepta cualquier propuesta con justificación de dominio. Ejemplos razonables:
`experiencia_por_edad` (razón, que un modelo lineal no puede construir), `dias_hasta_cierre`
(solicitar sobre la fecha límite como indicador), o un indicador de promedio alto combinado con
puntaje alto.

**Lo que se evalúa es que reporte el resultado aunque sea negativo.** En este dataset el
proceso generador es aditivo en `promedio_pregrado`, `puntaje_examen` y `experiencia_anios`, así
que casi ninguna variable derivada mejorará. Descubrirlo y decirlo es la respuesta correcta.

## Parte E — Evaluación final

**E.1**

| | Accuracy |
|---|---|
| Prueba (una sola vez) | **0.7459** |
| Referencia trivial en prueba | 0.7213 |

La mejora sobre la referencia cae a ~2.5 puntos en prueba, frente a los ~6.8 de la validación
cruzada. Es una diferencia que merece comentarse en clase: con 122 observaciones de prueba, el
intervalo de incertidumbre es amplio, y es esperable que una estimación puntual varíe. **No
significa que el modelo esté roto**; significa que un solo número sobre un conjunto pequeño es
un estimador ruidoso. La sesión 8 aborda cómo cuantificar esa incertidumbre.

**E.2 — Coeficientes** (mayor valor absoluto primero)

| Variable | Coeficiente |
|---|---|
| `promedio_pregrado` | +1.117 |
| `puntaje_examen` | +1.097 |
| `fue_entrevistado` | −0.502 |
| `experiencia_anios` | +0.276 |
| `modalidad_Virtual` | −0.253 |
| `programa_Industrial` | −0.250 |
| `log_ingresos` | −0.216 |

Coincide con el EDA: el promedio de pregrado y el puntaje del examen dominan, seguidos de la
experiencia. Son exactamente las tres variables del proceso generador.

El coeficiente **negativo** de `fue_entrevistado` reproduce el hallazgo del ejercicio 01: se
entrevista a los casos dudosos, así que haber sido entrevistado predice **menor** probabilidad
de admisión. Buen momento para recordar que un coeficiente no es una relación causal:
entrevistar a alguien no reduce sus posibilidades.

`log_ingresos` con coeficiente negativo y pequeño es ruido — los ingresos no intervienen en el
proceso generador. Conviene señalarlo: **los modelos asignan coeficientes a todo, tengan
relación o no**.

**E.3** El pipeline recargado debe predecir sobre un `DataFrame` crudo con `NaN`. Si falla,
casi siempre es porque el estudiante aplicó alguna transformación fuera del pipeline y el
objeto guardado no la contiene — que es precisamente la lección.

**E.4** Con `handle_unknown="ignore"`, el `OneHotEncoder` codifica la categoría desconocida
como todo ceros y la predicción funciona. Sin ese parámetro, lanza
`ValueError: Found unknown categories`.

> Es el fallo que tumba una API en producción el día que llega un valor nuevo, y no aparece en
> ninguna prueba hecha con los datos históricos.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A: pipeline correcto con `ColumnTransformer`; partición antes de todo | 1.0 |
| A.3: explica por qué la función fila a fila es segura | 0.5 |
| B: detecta y cuantifica la fuga; enuncia los límites del chequeo por correlación | 0.7 |
| C.1–C.3: mide las tres fugas correctamente | 0.8 |
| C.4: **explica** por qué la selección infla menos aquí que en el notebook 03 | 1.0 |
| D.2: reconoce que no hay mejora demostrable | 0.5 |
| E: evaluación única en prueba; interpreta coeficientes; `handle_unknown` | 0.5 |
| **Total** | **5.0** |

> **C.4** es la pregunta que separa a quien memorizó "la fuga es mala" de quien entendió *por
> qué* y *cuándo*. Vale un punto entero a propósito.

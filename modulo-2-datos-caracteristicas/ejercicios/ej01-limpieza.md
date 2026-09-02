# Ejercicio 01 · Diagnóstico y limpieza de un dataset sucio

**Módulo 2 · Sesión 4** · Tiempo estimado: **90 min** · Con código

> **Objetivo.** Aplicar el diagnóstico completo de calidad de datos sobre un dataset que
> nunca has visto, identificar cada problema y **justificar** qué hacer con él. Se evalúa el
> criterio, no la cantidad de líneas de código.

## Contexto

`../datos/matriculas-sucio.csv` contiene 620 solicitudes de admisión a programas de posgrado.
Los datos son sintéticos, pero los problemas de calidad son los que aparecen en un archivo
real que ha pasado por varias manos.

La variable objetivo es `admitido` (1 = admitido, 0 = no admitido).

```python
import numpy as np
import pandas as pd

datos = pd.read_csv("../datos/matriculas-sucio.csv")
```

Entrega un notebook `ej01-<tu-apellido>.ipynb` que corra de principio a fin.

> **Advertencia.** El archivo tiene al menos **nueve** problemas distintos. Algunos son
> visibles con `info()`; otros solo aparecen si los buscas. No confíes en que `isna()` te los
> muestre todos.

## Parte A — Perfilado inicial (15 min)

**A.1** Reporta forma, tipos y memoria del dataset. ¿Qué columnas tienen un tipo que **no**
corresponde a lo que representan? Enumera al menos tres.

**A.2** Construye el diccionario de datos: para cada columna, su significado, tipo esperado,
rango o categorías, y —muy importante— **si estará disponible en el momento de decidir la
admisión**.

**A.3** Hay una columna que **no debe usarse jamás** como variable predictora. Identifícala,
demuestra por qué con una tabla cruzada, y nombra el concepto.

## Parte B — Faltantes, visibles y disfrazados (25 min)

**B.1** Reporta los valores faltantes declarados (`NaN`) por columna.

**B.2** Hay faltantes que `isna()` **no detecta**. Búscalos:

- Revisa los valores únicos de `puntaje_examen`. ¿Por qué la columna es de tipo texto?
- Revisa el mínimo de `ingresos_hogar`. ¿Tiene sentido?

Cuantifica cuántos hay de cada tipo y conviértelos correctamente a `NaN`.

**B.3** Para `experiencia_anios`, determina el **mecanismo** de ausencia. Calcula la tasa de
faltantes por `modalidad` y por `programa`. ¿Es MCAR, MAR o MNAR? Justifica con los números.

**B.4** Para `nota_entrevista`, haz lo mismo. Además:

- ¿Qué proporción falta?
- Compara la tasa de admisión entre quienes tienen nota de entrevista y quienes no.
- ¿Cuál es el mecanismo? ¿Qué harías con esta columna y por qué?

**B.5** Escribe la tabla de decisiones de imputación para las cinco columnas afectadas, con la
justificación de cada una. Recuerda: **no las apliques todavía**.

## Parte C — Duplicados (15 min)

**C.1** ¿Cuántas filas están completamente duplicadas?

**C.2** ¿Cuántos `id_solicitud` se repiten?

**C.3** ¿Cuántas filas son idénticas **ignorando** `id_solicitud`?

**C.4** Los tres números no coinciden. Explica qué significa cada uno, cuáles son duplicados
**reales** y cuáles son coincidencias, y qué harías con cada grupo. Este es el punto central
del ejercicio.

## Parte D — Valores extremos e inconsistencias (20 min)

**D.1** Revisa el rango de `edad`. Hay valores imposibles: cuántos, cuáles, y qué haces con
ellos.

**D.2** Aplica la regla del IQR a `ingresos_hogar` (usando solo los valores válidos). ¿Cuántos
outliers marca? Examina los más altos: ¿son errores o valores legítimos? Justifica.

**D.3** ¿Qué transformación propondrías para `ingresos_hogar`? Compara la asimetría antes y
después.

**D.4** Cuenta las categorías de `estado_civil`. Deberían ser tres y no lo son. Normalízala y
reporta el conteo final.

**D.5** `fecha_solicitud` está como texto. Conviértela a fecha y extrae al menos dos variables
derivadas que puedan ser útiles.

## Parte E — Análisis exploratorio (15 min)

Con los datos ya diagnosticados (y `admitido_texto` fuera):

**E.1** Tasa de admisión por `programa` y por `modalidad`, **siempre con el conteo al lado**.

**E.2** Compara la distribución de `promedio_pregrado` y `puntaje_examen` entre admitidos y no
admitidos. (Recuerda que `promedio_pregrado` necesita conversión previa.)

**E.3** Matriz de correlación de las numéricas frente a `admitido`. ¿Qué variables se asocian
más con la admisión?

**E.4** Busca una **interacción**: ¿el efecto del promedio sobre la admisión es igual en las
dos modalidades? Presenta una tabla o gráfica que lo responda.

## Entrega

Un notebook con:

1. El código ejecutado.
2. Las respuestas en celdas Markdown.
3. Una **tabla final de decisiones** con el formato: problema · evidencia · decisión ·
   justificación. Esta tabla es lo que más pesa en la calificación.

> Ninguna transformación que aprenda algo de los datos (medias, medianas, modas) debe
> aplicarse fuera de un `Pipeline`. Puedes dejarlas anotadas como decisiones a implementar en
> el ejercicio 02.

# 04 · Monitoreo y drift: el modelo después del despliegue

**Módulo 6 · Sesión 14** — De modelo a producto

## Objetivos

- Distinguir los tipos de cambio que degradan un modelo en producción —drift de datos,
  de concepto, de etiquetas— y qué herramienta detecta cada uno.
- Saber construir un monitoreo en dos capas: entradas y predicciones (sin etiquetas) y
  desempeño (cuando llegan).
- Tener un criterio medido para decidir cuándo reentrenar y con qué datos.

## 1. Un modelo se entrena una vez y el mundo sigue cambiando

Todo lo que el curso midió —CV, conjunto de prueba, comparación pareada— supone que los
datos futuros se parecen a los del entrenamiento. En producción esa suposición caduca:
cambia la población que llega, cambia lo que se mide y cómo, cambia la relación entre las
variables y el objetivo. El modelo no lo sabe: sigue devolviendo probabilidades con la
misma confianza. Monitorear es comprobar, mes a mes, que la suposición sigue en pie, y
saber qué hacer cuando deja de estarlo.

Los tipos de cambio, con los nombres que usa la literatura:

| Tipo | Qué cambia | Ejemplo | ¿Se ve sin etiquetas? | ¿Daña? |
|---|---|---|---|---|
| **Drift de datos** (*covariate shift*) | La distribución de $\mathbf{X}$; $P(y \mid \mathbf{X})$ igual | Llegan más estudiantes que trabajan | **Sí**: PSI, KS sobre las entradas | No necesariamente: si el modelo es correcto en la región nueva, no |
| **Drift de concepto** | La relación $P(y \mid \mathbf{X})$ | Cambia la forma de evaluar; las horas de estudio pesan menos | **No**: las entradas se ven iguales | Sí |
| **Drift de etiquetas** (*prior shift*) | $P(y)$: la tasa base | Sube la tasa de deserción sin que cambien las variables | Parcialmente: la distribución de las predicciones se mueve | Depende: el umbral y la calibración quedan desajustados |
| **Cambios de esquema / calidad** | Unidades, columnas, nulos, un sensor roto | Alcohol en g/L en vez de % vol. | Sí, y antes que nada: validación del contrato (`02-apis-para-modelos.md`) | Sí, de golpe |

Los dos primeros son los que el notebook 02 planta y mide.

## 2. Capa 1: monitorear las entradas y las predicciones (sin etiquetas)

Desde el primer día de operación se tienen las peticiones. Con ellas se compara la
distribución de cada variable en una ventana reciente contra la de **referencia** (los
datos de entrenamiento, o un periodo de operación sano):

- **Índice de estabilidad poblacional** (PSI). Se parte el rango de la variable en 10
  cuantiles de la referencia y se compara la fracción de datos en cada uno:

$$
\text{PSI} = \sum_{b=1}^{10} \left(p_b^{\text{nuevo}} - p_b^{\text{ref}}\right) \ln \frac{p_b^{\text{nuevo}}}{p_b^{\text{ref}}}
$$

  Es simétrica, no depende de $n$ (a diferencia de un valor $p$), y tiene una escala
  empírica de la industria del crédito: $< 0.1$ sin cambio, $0.1$–$0.25$ cambio moderado,
  $> 0.25$ cambio importante. En el notebook 02, `trabaja` pasa de PSI ≈ 0 a 0.3–0.4 el
  mes exacto del drift de datos.
- **Prueba de Kolmogorov-Smirnov** para variables continuas (distancia máxima entre las
  distribuciones acumuladas) y **chi-cuadrado** para categóricas. Dan un valor $p$: con
  muchas peticiones detectan cambios minúsculos, así que dicen si el cambio es real, no si
  importa. El PSI, o el tamaño del efecto, dicen si importa.
- **La distribución de las predicciones**: la media y el PSI de la salida del modelo.
  Resume todas las variables en una y detecta combinaciones raras que ninguna variable
  sola muestra. En el notebook 02, la nota media predicha cae de 3.42 a 3.16 en el mes 13.

Lo que esta capa **no** ve: el drift de concepto. Del mes 19 en adelante, con la relación
cambiada, los PSI de todas las entradas y de las predicciones se quedan exactamente donde
estaban.

## 3. Capa 2: monitorear el desempeño (cuando llegan las etiquetas)

Las etiquetas llegan con retraso (la nota final, al cerrar el semestre; la deserción,
meses después) o parcialmente (solo se conoce el resultado de los créditos aprobados). Cuando
llegan, la métrica del modelo —RMSE, AP, la que se eligió en el módulo 1— se calcula por
periodo y se compara contra una **carta de control**: la media y la desviación de la
métrica en periodos de referencia, y una alarma a tres desviaciones (o al valor que la
decisión de negocio tolere).

El notebook 02 mide las dos sorpresas que hacen necesaria esta capa:

1. **Drift de datos sin daño.** Meses 13–18: PSI alto, predicciones desplazadas, y el RMSE
   sigue en 0.34 — dentro de la carta. El modelo es el correcto y la región nueva estaba
   representada en el entrenamiento (el 38 % ya trabajaba); un cambio en la distribución
   de las entradas no lo daña. Un modelo flexible (gradient boosting) tampoco se degrada
   aquí, aunque lo haría si el cambio llevara a una región **sin** datos de entrenamiento.
   El PSI alto es una alarma que obliga a comprobar, no una sentencia.
2. **Drift de concepto sin aviso.** Mes 19: las entradas iguales, el RMSE de 0.34 a 0.44
   (+30 %). Solo la etiqueta lo ve.

Cuando no hay etiquetas y no las va a haber, quedan sustitutos débiles: la confianza
media del modelo, la fracción de predicciones cerca del umbral, el acuerdo con un modelo
más simple, y la retroalimentación indirecta del negocio (si un modelo de deserción
señala menos estudiantes y las bajas no bajan, algo pasa).

## 4. Diagnosticar: qué cambió

Una alarma sin diagnóstico lleva a reentrenar a ciegas. Dos herramientas baratas:

- Con drift de datos: **qué variables** tienen el PSI alto, y hacia dónde se movieron (la
  media por periodo). En el notebook 02: `trabaja` de 0.38 a 0.65, `promedio_anterior`
  0.15 menor.
- Con drift de concepto: **reajustar el mismo modelo** sobre el periodo en alarma y
  comparar los coeficientes (o las importancias) con los originales. En el notebook 02, el
  coeficiente de `horas_estudio_semana` cae de 0.053 a 0.019 y el intercepto sube 0.7:
  exactamente el cambio plantado. Ese hallazgo es lo que hay que llevar al dueño del
  problema —¿cambió la evaluación? ¿cómo se registran las horas?—, porque el modelo no
  puede saber por qué su relación dejó de valer.

## 5. Reentrenar: cuándo y con qué datos

Tres políticas, de menos a más informada:

| Política | Cuándo reentrena | Con qué datos | Problema |
|---|---|---|---|
| **Periódica** | Cada mes / trimestre, pase lo que pase | Ventana reciente o todo | Reentrena cuando no hace falta (costo, riesgo de introducir regresiones) y llega tarde cuando sí |
| **Por alarma** | Cuando la carta de control (o el PSI) dispara | Depende del diagnóstico | Necesita etiquetas para la carta, o acepta falsas alarmas del PSI |
| **Continua** | Cada lote nuevo, en línea | Los últimos datos | Solo para modelos y volúmenes que lo justifiquen; difícil de validar |

Y la pregunta que el diagnóstico responde: **con qué datos**. El notebook 02 lo mide
tras el drift de concepto, reentrenando al cerrar el mes 20 y evaluando sobre 22–24:

| Datos de reentrenamiento | RMSE 22–24 |
|---|---|
| Ninguno (modelo original) | 0.437 |
| Todo el historial (meses 1–20) | 0.416 |
| Ventana de 6 meses (15–20) | 0.392 |
| Solo desde el cambio (19–20) | **0.357** (≈ ruido) |

Con drift de concepto, **más datos no es mejor**: los anteriores al cambio describen una
relación que ya no existe, y diluyen la nueva. Con drift de datos y modelo correcto, no
hacía falta reentrenar. La política correcta no es "reentrenar cada mes" sino "vigilar,
diagnosticar, y reentrenar desde el cambio cuando la relación cambió".

Cada reentrenamiento pasa por el mismo camino que el primero: una corrida en MLflow con
su hash de datos y sus métricas, la comparación pareada contra el modelo en producción
(módulo 3), una versión nueva en el registro, y un despliegue con reversión posible
(`03-empaquetado-y-despliegue.md`). Reentrenar no es reejecutar un notebook: es una
versión nueva de un producto.

## 6. Un sistema de monitoreo mínimo

Lo que la entrega E6 debería describir (no necesariamente construir):

1. **Registro** de cada petición y respuesta, con marca de tiempo y versión del modelo.
2. **Validación del contrato** en la API: rangos, tipos, campos (drift burdo, al instante).
3. **Capa 1**, semanal o mensual: PSI y KS por variable y de las predicciones contra la
   referencia; umbrales; a quién avisa.
4. **Capa 2**, cuando lleguen etiquetas: la métrica del módulo 1 por periodo, carta de
   control, umbral de alarma ligado a la decisión de negocio.
5. **Protocolo** ante alarma: diagnóstico (§4), decisión de reentrenar (§5), y cómo se
   valida y despliega la versión nueva.

## Referencias

- Gama, J. et al. (2014). A survey on concept drift adaptation. *ACM Computing Surveys*.
- Rabanser, S., Günnemann, S. y Lipton, Z. (2019). Failing loudly: an empirical study of
  methods for detecting dataset shift. *NeurIPS*.
- Huyen, C. (2022). *Designing Machine Learning Systems*, cap. 8 (data distribution
  shifts and monitoring).
- Siddiqi, N. (2017). *Intelligent Credit Scoring*, 2.ª ed. — origen y escala del PSI.

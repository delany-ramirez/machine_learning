# Solución · Ejercicio 03 · CV, grid vs. random, CV anidada y ¿ayuda `foundation`?

> **Material del docente.** Todos los números provienen de ejecutar el código sobre
> `ames-housing.csv` con `random_state=42`, sobre las variables de los ejercicios 01 y 02.

## Parte A — Elegir $\lambda$ con `GridSearchCV`

**A.1**

| Modelo | $\lambda$ elegido (CV) | RMSE de CV |
|---|---|---|
| Ridge | 7.20 | \$40,764 |
| Lasso | 7.20 | \$40,775 |

> Los $\lambda$ de la tabla corresponden a la rejilla sugerida en `ej02-regularizacion.md`,
> `np.logspace(-2, 3, 15)`, cuyo punto más cercano al óptimo es 7.20. Un estudiante que use
> otra rejilla obtendrá un $\lambda$ algo distinto (con 20 puntos, 7.85) y prácticamente el
> mismo RMSE: la curva es muy plana en esa zona, y eso es en sí mismo parte de la lección.

**A.2** El $\lambda$ de Ridge por CV (7.20) es bastante mayor que el "≈1" elegido a ojo en
`ej02-regularizacion-sol.md` sobre un solo split de validación — otra muestra de que un split
único es ruidoso (`05-sesgo-varianza-validacion.md`, sección 2). El RMSE de 5-fold CV
(\$40,764) es más bajo que el RMSE de prueba del ejercicio 02 (\$43,342): son números
distintos por construcción —CV promedia el error sobre 5 particiones del 80% de entrenamiento,
mientras el RMSE de prueba se mide sobre el 20% final que nunca participó en nada—, y no hay
razón para esperar que coincidan. Se acepta cualquier respuesta que note que son estimaciones
sobre conjuntos distintos, no una contradicción.

## Parte B — Grid vs. random

**B.1**

| Método | Evaluaciones | Tiempo | RMSE de CV |
|---|---|---|---|
| Grid | 40 | 1.33 s | 40,764.33 |
| Random | 15 | 0.51 s | 40,765.10 |

**B.2** Sí se sostiene: con menos de la mitad de las evaluaciones (15 vs. 40), random search
llega a un RMSE prácticamente idéntico (diferencia de menos de un dólar) en un tercio del
tiempo. Es exactamente el resultado de Bergstra & Bengio citado en
`06-seleccion-hiperparametros.md`: en un espacio de un solo hiperparámetro razonablemente
suave, no hace falta cubrir la rejilla completa.

## Parte C — Validación cruzada anidada

**C.1** RMSE de CV anidada: **\$40,814 ± \$3,663** (error estándar sobre los 5 pliegues
externos).

**C.2** RMSE ingenuo (parte A): \$40,764. Optimismo medido: **\$50** — minúsculo, y muy por
debajo del error estándar de \$3,663 de la propia CV anidada. Con este dataset y este
$\lambda$ ya cercano a OLS, la fuga por no anidar es, en la práctica, indetectable. Vale la
pena que el estudiante note la analogía con `04-regularizacion-aplicado.ipynb`: cuando el
modelo ya está cerca de su óptimo sin regularizar, hay poco margen para que la elección del
hiperparámetro produzca una estimación sesgada.

## Parte D — ¿`foundation` ayuda de verdad?

**D.1–D.2**

| Comparación pareada (10 pliegues) | Valor |
|---|---|
| Diferencia media (sin `foundation` − con `foundation`) | **+\$961** |
| Error estándar de la diferencia | \$211 |

**D.3 — El resultado central del ejercicio.** La diferencia (\$961) es más de **4 veces** su
error estándar (\$211) — muy por encima de la regla práctica de dos errores estándar de
`05-sesgo-varianza-validacion.md`. A diferencia de la comparación Ridge-vs-Lasso del notebook
06, donde la diferencia era indistinguible del ruido, **aquí sí hay evidencia real**: el
modelo sin `foundation` comete, en promedio, casi mil dólares más de error. `foundation` no es
una variable de relleno — vale la pena mantenerla.

> **Por qué es un buen cierre de módulo.** El estudiante ya vio, en el notebook 06, un caso
> donde la comparación pareada concluye "no hay diferencia". Este ejercicio muestra el caso
> contrario con la misma herramienta: la validación cruzada pareada no está sesgada a
> concluir "todo da igual" — cuando la diferencia es real, la detecta con claridad. Ambos
> resultados son la herramienta funcionando correctamente, no dos comportamientos distintos.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A: `GridSearchCV` con `KFold` bien construido; compara contra el ejercicio 02 | 1.0 |
| B: comparación grid/random con tiempos y conclusión correcta | 1.0 |
| C: CV anidada implementada correctamente (el interno nunca ve el pliegue externo) | 1.0 |
| D.2: comparación pareada sobre los mismos 10 pliegues para ambos modelos | 1.0 |
| D.3: interpreta correctamente que aquí SÍ hay diferencia detectable, y por qué contrasta con el notebook 06 | 1.0 |
| **Total** | **5.0** |

> La pregunta que mejor discrimina es **D.3**: quien concluye "no hay diferencia" por
> costumbre (arrastrando la conclusión del notebook 06 sin mirar sus propios números) se la
> pierde por completo.

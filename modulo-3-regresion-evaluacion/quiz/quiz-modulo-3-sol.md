# Clave · Quiz Módulo 3 — Regresión y evaluación

> **Material del docente.** Se indica lo mínimo exigible y, cuando aplica, el error típico que
> conviene comentar en la retroalimentación.

---

**1. Embudo en los residuales**

**a)** **Homocedasticidad** (supuesto 3 de `01-regresion-lineal.md`): la varianza del error no
es constante, crece con el valor ajustado.

**b)** **No.** $R^2$ y $R^2$ ajustado son medidas **globales** de ajuste; el embudo es un
patrón **local** (el error se concentra en un rango de precios). Un modelo puede tener buen
$R^2$ global y aun así equivocarse sistemáticamente mal en las viviendas caras — exactamente
lo que se midió en `02-regresion-multiple-aplicado.ipynb`.

**c)** Cualquiera razonable: modelar $\log(1+y)$; usar una pérdida ponderada; reportar
métricas por segmento de precio en vez de solo el número global.

---

**2. Descenso que explota o converge lentísimo**

**a)** **Algo previo a la tasa de aprendizaje** — casi con certeza, falta estandarizar los
predictores. Que $\eta=0.1$ explote y $\eta=0.0001$ tarde 50.000 iteraciones para el *mismo*
problema es la firma de una superficie de costo muy alargada (`02-descenso-gradiente.md`,
sección 4), no de una tasa de aprendizaje mal elegida en el vacío.

**b)** Estandarizar cada predictor ($z=(x-\bar x)/s$) antes de correr el descenso. Con la
superficie de costo aproximadamente circular, una $\eta$ intermedia (p. ej. 0.1) converge
rápido sin diverger — resuelve la explosión de un compañero y la lentitud del otro a la vez,
porque ambos síntomas eran el mismo problema visto con dos tasas distintas.

---

**3. Batch, mini-batch, SGD**

| Variante | Gradiente sobre | Curva de aprendizaje |
|---|---|---|
| Batch | Todos los datos | **Suave**: cada paso usa el gradiente exacto |
| Mini-batch | Un subconjunto ($b$ filas) | Moderadamente ruidosa: menos que SGD, más que batch |
| SGD | Una sola fila | **Muy ruidosa**: cada paso usa una estimación del gradiente basada en un solo ejemplo |

Se espera que se mencione que el ruido de mini-batch/SGD no impide la convergencia, solo hace
que la curva oscile en vez de bajar monótonamente (se diagnostica sobre una versión suavizada).

---

**4. VIF bajo no es garantía total**

**a)** **En desacuerdo, parcialmente.** El VIF individual de cada variable mide su relación
con **todas las demás juntas**; puede ser bajo para cada una por separado y aun así existir
colinealidad **mutua moderada** entre varias que, en conjunto, siguen desestabilizando
coeficientes concretos. VIF bajo reduce el riesgo, no lo elimina.

**b)** El de `ej02-regularizacion-sol.md`: `full_bath` y `half_bath` con VIF < 2.5 cada una,
pero con coeficiente de signo negativo (contraintuitivo) porque varias variables de tamaño
(`total_bsmt_sf`, `1st_flr_sf`, `2nd_flr_sf`) ya capturaban gran parte de esa señal. Se acepta
cualquier ejemplo análogo, propio o de otro material del curso.

---

**5. `area^2` dispara el VIF**

**a)** $x$ y $x^2$ están casi linealmente relacionadas en el rango donde viven la mayoría de
los datos — elevar al cuadrado no genera información verdaderamente independiente
(`03-multicolinealidad-polinomica.md`, sección 5).

**b)** **No, por sí solo.** Si el objetivo es predecir y el $R^2$ de prueba mejora, el VIF alto
no es motivo suficiente para descartar el término — daña la interpretación de los coeficientes
individuales de `area` y `area^2`, no necesariamente la predicción. Sería motivo de
preocupación si el objetivo fuera explicar el efecto de cada término por separado.

---

**6. Geometría de Lasso vs. Ridge**

La región de penalización de Ridge ($\lVert\boldsymbol\beta\rVert_2^2 \le t$) es un **círculo**
(o esfera): no tiene esquinas, así que el punto donde las curvas de nivel del error de OLS
tocan la frontera casi nunca cae exactamente sobre un eje — ningún coeficiente se fuerza a
cero. La región de Lasso ($\lVert\boldsymbol\beta\rVert_1 \le t$) es un **diamante**, que sí
tiene esquinas sobre los ejes (donde alguna coordenada vale cero); esas esquinas son puntos de
tangencia geométricamente mucho más probables, y por eso Lasso produce coeficientes
exactamente cero con frecuencia.

> Una respuesta que solo diga "porque la derivada de $|\beta|$ en cero no existe" sin mencionar
> la geometría es incompleta para el punto completo.

---

**7. Cinco variables correlacionadas, todas relevantes**

**Elastic Net.** Con Lasso puro, el grupo correlacionado se trataría de forma inestable:
elegiría una o pocas del grupo casi al azar y pondría las demás en cero, aunque todas aporten
señal real. El componente Ridge de Elastic Net tiende a mantener el grupo completo con
coeficientes de magnitud similar en vez de una selección arbitraria, que es justo lo que
conviene cuando se sabe que las cinco son relevantes.

---

**8. Entrenamiento 0.02, validación 0.31 → 0.29 con más datos**

**a)** **Varianza alta.** La brecha enorme entre entrenamiento (0.02) y validación (0.31) —no
un error alto en ambos— es la firma de varianza, no de sesgo. Que duplicar los datos baje algo
el error de validación (0.29) lo confirma: la varianza sí mejora con más datos; el sesgo, no.

**b)** Ayudarían: regularizar más fuerte (Ridge/Lasso con mayor $\lambda$); reducir la
complejidad del modelo (menos variables, menor grado polinómico); conseguir más datos de
entrenamiento. **No ayudaría:** agregar todavía más variables o aumentar el grado del
polinomio — eso empeoraría la varianza, no la mejoraría.

---

**9. Reportar el RMSE de la misma CV que eligió $\lambda$**

**a)** Es una estimación **optimista** del desempeño real: el $\lambda$ se eligió precisamente
porque minimizaba ese número sobre esos pliegues, así que reportarlo como si fuera una medición
independiente sobredimensiona el desempeño esperado — el mismo problema, en espíritu, que
seleccionar variables mirando los datos de validación (módulo 2).

**b)** Un bucle **externo** de $k$ pliegues estima el error de generalización; dentro de cada
uno de esos pliegues de entrenamiento, un bucle **interno** de CV elige el mejor $\lambda$.
El modelo final de cada iteración externa se evalúa sobre un pliegue que el bucle interno
**nunca vio**, ni para entrenar ni para elegir el hiperparámetro.

**c)** Cuando el dataset es pequeño y/o el número de hiperparámetros (y el tamaño de la
rejilla) es grande: más oportunidades de que la búsqueda "encuentre" una combinación que
funciona bien por azar en esos pliegues específicos.

---

**10. 20 evaluaciones, dos hiperparámetros**

Con presupuesto **fijo y chico** (20), **random search u Optuna** son preferibles a grid
search: una rejilla 2D razonable ya necesita más de 20 combinaciones para cubrir el espacio con
algo de resolución, y grid gastaría evaluaciones de forma pareja sin importar qué tan
influyente sea cada hiperparámetro. Optuna, además, usa el historial de evaluaciones para
decidir dónde probar después, lo que en general lo hace más eficiente que random con
presupuestos ajustados.

Con 200 evaluaciones: grid search se vuelve viable (una rejilla 14×14, por ejemplo, cubre el
espacio con más resolución) y compite mejor con las otras dos; random search también mejora,
simplemente por explorar más puntos; Optuna sigue teniendo la ventaja de usar el historial,
pero la brecha con random search se reduce a medida que el presupuesto crece.

---

## Distribución de puntos

| Pregunta | Puntos | Evalúa |
|---|---|---|
| 1 | 0.5 | Homocedasticidad; límites del $R^2$ global |
| 2 | 0.5 | Diagnóstico de divergencia del descenso del gradiente |
| 3 | 0.5 | Batch vs. mini-batch vs. SGD |
| 4 | 0.5 | Límites del VIF individual |
| 5 | 0.5 | Polinómica y su costo en colinealidad |
| 6 | 0.5 | Geometría Ridge vs. Lasso |
| 7 | 0.5 | Cuándo usar Elastic Net |
| 8 | 0.5 | Diagnóstico de sesgo vs. varianza |
| 9 | 0.5 | CV anidada y optimismo |
| 10 | 0.5 | Grid vs. random vs. Optuna según presupuesto |
| **Total** | **5.0** | |

> Las preguntas **4, 8 y 9** son las que mejor discriminan. La 4 y la 9 comparten un mismo
> error de fondo —tratar un diagnóstico o una búsqueda como si garantizara más de lo que en
> realidad garantiza— que vale la pena señalar como patrón, no como dos errores sueltos.

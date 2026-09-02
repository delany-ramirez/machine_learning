# Solución · Ejercicio 01 · Encuadrar problemas de Machine Learning

> **Material del docente.** Varias respuestas admiten matices; lo evaluable es la
> justificación. Se señalan los puntos donde conviene detenerse en la discusión con el grupo.

## Parte A — Tipo de aprendizaje

| # | Situación | Respuesta | Justificación |
|---|---|---|---|
| 1 | Cuántos estudiantes se matricularán | Supervisado · **regresión** | La respuesta es un número continuo (o conteo); hay histórico etiquetado |
| 2 | Agrupar en perfiles | **No supervisado** (clustering) | No hay etiquetas ni número de grupos conocido |
| 3 | Correo fraudulento o no | Supervisado · **clasificación binaria** | Etiqueta categórica de dos clases |
| 4 | Nota del examen final | Supervisado · **regresión** | Valor continuo |
| 5 | Transacciones inusuales sin ejemplos | **No supervisado** (detección de anomalías) | Sin etiquetas de fraude; se busca lo que se desvía del patrón |
| 6 | Ajustar dificultad para maximizar aprendizaje a largo plazo | **Por refuerzo** | Hay un agente que decide secuencialmente y recibe recompensa diferida |
| 7 | Clasificar artículos en tres líneas | Supervisado · **clasificación multiclase** | Categorías conocidas de antemano |

> **Punto de discusión.** El caso 5 se vuelve supervisado en cuanto se dispone de un histórico
> de fraudes confirmados; entonces sería clasificación binaria fuertemente desbalanceada. Que
> el tipo de tarea dependa de los datos disponibles, y no solo del enunciado, es justamente la
> idea a transmitir.

## Parte B — Ficha del problema

| Elemento | Respuesta esperada |
|---|---|
| Decisión que apoya | A qué estudiantes ofrecer las 60 tutorías disponibles |
| Variable objetivo | No formaliza matrícula en el periodo académico siguiente (binaria) |
| Tipo de tarea | Clasificación binaria supervisada, con clases desbalanceadas (~18 % positivos) |
| Momento de predicción | Al final de las primeras 4–6 semanas del semestre, con tiempo para intervenir |
| Referencia | La regla actual: el criterio manual del coordinador. Como mínimo, un clasificador trivial |
| Métrica técnica | **Recall** de la clase "deserta", o precisión@60 — ver nota abajo |
| Métrica de negocio | Estudiantes retenidos por semestre; costo por retención lograda |
| Restricción operativa | Solo 60 cupos de tutoría: el modelo debe **ordenar**, no solo clasificar |

**B.1 — Asimetría de costos.** No son simétricos. Un **falso negativo** (no detectar a quien
va a desertar) significa perder al estudiante: costo alto y en buena medida irreversible. Un
**falso positivo** (citar a quien no iba a desertar) cuesta una tutoría que probablemente
igual le sirva. Por eso se prioriza el recall sobre la precisión, aunque con el límite que
impone el presupuesto.

**B.2 — Consecuencia de los 60 cupos.** Es el punto clave del ejercicio y conviene detenerse
en él. Con 400 estudiantes y 18 % de deserción hay unos **72 desertores esperados**, y solo
**60 cupos**. El problema no es "clasificar en riesgo / no riesgo", sino **ordenar a los 400
por probabilidad de deserción y atender a los 60 primeros**.

Esto cambia todo:

- La salida útil del modelo es una **probabilidad**, no una etiqueta.
- La métrica adecuada es de tipo *precisión@k* con $k=60$: de los 60 citados, ¿cuántos iban
  realmente a desertar?
- El umbral de decisión no lo fija el modelo, lo fija el presupuesto.

> Este es un buen momento para anticipar la sesión 9: el umbral es una decisión de negocio,
> no un detalle técnico.

## Parte C — Fugas de datos

| # | Variable | ¿Fuga? | Por qué |
|---|---|---|---|
| 1 | Promedio al ingresar | **No** | Se conoce antes de que empiece el semestre |
| 2 | Créditos matriculados el semestre siguiente | **Sí** | Es prácticamente la variable objetivo: si no matricula créditos, ya desertó |
| 3 | Asistencia de las primeras 4 semanas | **No** | Disponible en el momento de predecir |
| 4 | Solicitó retiro formal | **Sí** | El retiro *es* la deserción. Predeciría casi perfecto y sería inútil |
| 5 | Estrato socioeconómico | **No** técnicamente | Disponible, pero ver la nota ética abajo |
| 6 | Promedio del semestre calculado al cierre | **Sí** | Solo se conoce al final; para entonces la intervención ya no es posible |
| 7 | Ingresos a la plataforma en el primer mes | **No** | Disponible temprano y muy informativo |
| 8 | Si el coordinador ya lo citó | **Sí**, fuga sutil | Refleja la decisión que el modelo pretende reemplazar. El modelo aprendería a imitar al coordinador, incluidos sus sesgos, y en producción la variable no existiría antes de decidir |

> **Punto de discusión.** Las fugas 2, 4 y 6 son evidentes una vez señaladas. La número **8**
> es la valiosa: es una fuga por *retroalimentación*, donde la variable predictora es
> consecuencia del proceso de decisión. Aparece constantemente en sistemas reales y casi nunca
> se detecta mirando solo las métricas — que además mejoran, lo que la hace más peligrosa.
>
> Regla práctica: **si una variable mejora las métricas de forma sospechosamente buena,
> sospecha de fuga antes que de suerte.**

## Parte D — Argumentar en contra

**D.1 — Razones para no usar ML.** Se acepta cualquier par bien argumentado:

- Si una regla simple (por ejemplo, "asistencia < 60 % o pérdida del primer parcial") ya
  identifica a la mayoría de los casos, un modelo añade complejidad y mantenimiento sin
  aportar valor. **Hay que medirlo antes de descartarlo.**
- Con 400 estudiantes por semestre y ~72 casos positivos, los datos son escasos para un modelo
  complejo; el riesgo de sobreajuste es alto.
- Si la causa real de la deserción es económica y la universidad no puede actuar sobre eso, el
  modelo predice bien y no cambia nada: la decisión no está en su alcance.
- Si el objetivo es entender **por qué** desertan (causalidad), el ML predictivo no responde
  esa pregunta.

**D.2 — Riesgo ético.** Respuesta esperada: los datos históricos registran quién desertó bajo
las políticas y sesgos existentes. Si históricamente los estudiantes de menor estrato o de
cierto programa desertaron más por falta de apoyo económico, el modelo aprenderá a señalarlos
como "de alto riesgo" — y podría terminar **normalizando** esa situación en vez de corregirla,
o estigmatizando a un grupo.

Formas de detectarlo:

- Evaluar las métricas **por subgrupo** (estrato, género, programa) en lugar de solo en
  agregado.
- Comparar las tasas de falsos positivos y falsos negativos entre subgrupos.
- Revisar la importancia de las variables (sesión 11): si el estrato domina la predicción, hay
  que discutir explícitamente si debe usarse.
- Mantener supervisión humana sobre la decisión final, nunca automatizarla por completo.

> Conviene cerrar con la idea del documento de teoría: *el algoritmo no es responsable de sus
> sesgos; quien modela, sí*.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| Parte A: tipos correctos con justificación | 1.0 |
| Parte B: ficha coherente y completa | 1.5 |
| Parte B.2: reconoce que el problema es de ordenamiento, no de clasificación | 1.0 |
| Parte C: identifica las cuatro fugas, incluida la sutil (#8) | 1.0 |
| Parte D: argumentos concretos, no genéricos | 0.5 |
| **Total** | **5.0** |

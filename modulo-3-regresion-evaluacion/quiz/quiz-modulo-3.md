# Quiz · Módulo 3 — Supervisado I: regresión y evaluación

**Sesiones 6–8** · 10 preguntas · Tiempo sugerido: **30 min** · Sin material de consulta

> Responde de forma breve y justificada. Se evalúa el razonamiento, no la extensión.

---

**1.** Ajustas una regresión lineal para predecir el precio de una vivienda. El gráfico de
residuales contra valores ajustados tiene forma de embudo: la dispersión crece con el precio.

- a) ¿Qué supuesto del modelo lineal se está violando?
- b) Tu $R^2$ es 0.81 y tu $R^2$ ajustado es 0.80. ¿Ese resultado, por sí solo, te dice algo
  sobre el problema del embudo? Justifica.
- c) Menciona una acción concreta que podrías probar.

---

**2.** Implementas descenso del gradiente para una regresión múltiple y, con
$\eta=0.1$, el costo explota a infinito en pocas iteraciones. Un compañero prueba con
$\eta=0.0001$ y converge, pero necesita 50.000 iteraciones.

- a) ¿Qué es más probable que esté mal: la tasa de aprendizaje o algo previo a elegirla?
  Justifica.
- b) Propón la corrección, y explica por qué resolvería **ambos** síntomas a la vez.

---

**3.** Explica la diferencia entre descenso **batch**, **mini-batch** y **estocástico (SGD)**.
Para cada uno, indica si la curva de aprendizaje (costo vs. iteración) es suave o ruidosa, y
por qué.

---

**4.** Calculas el VIF de seis predictores y todos dan menos de 3. Un compañero concluye "no
hay ningún problema de multicolinealidad, puedo interpretar cada coeficiente con confianza".

- a) ¿Estás de acuerdo? Justifica con lo que mide realmente el VIF.
- b) Describe un escenario (puede ser el que viste en los ejercicios del módulo) donde el VIF
  individual sea bajo y aun así un coeficiente tenga signo contraintuitivo.

---

**5.** Agregas `area^2` como predictor a un modelo que ya tenía `area`. El $R^2$ de prueba
mejora, pero el VIF de `area` pasa de 3 a 45.

- a) ¿Por qué ocurre eso casi siempre al agregar un término polinómico?
- b) ¿El aumento del VIF es, por sí solo, una razón para no usar el término? Justifica con el
  criterio de predicción vs. interpretación.

---

**6.** Explica, con el argumento **geométrico** (no solo "porque sí"), por qué Lasso puede
producir coeficientes exactamente iguales a cero y Ridge no. Tu respuesta debe mencionar la
forma de la región de penalización de cada uno.

---

**7.** Tienes cinco variables fuertemente correlacionadas entre sí, todas relevantes para el
objetivo. ¿Usarías Ridge, Lasso o Elastic Net? Justifica en términos de qué le pasaría a los
coeficientes de ese grupo con cada opción.

---

**8.** Entrenas un modelo y obtienes: error de entrenamiento = 0.02, error de validación =
0.31. Duplicas los datos de entrenamiento y el error de validación baja a 0.29.

- a) ¿El problema es de sesgo alto o de varianza alta? Justifica con los dos números.
- b) Menciona dos acciones que atacarían la causa real, y una que **no** ayudaría aunque
  suene razonable.

---

**9.** Un compañero elige el $\lambda$ de su Ridge con `GridSearchCV` y reporta el mejor
`RMSE_cv` de esa misma búsqueda como el "desempeño esperado del modelo en producción".

- a) ¿Qué problema tiene esa práctica?
- b) Describe, en dos o tres frases, cómo se estructura una validación cruzada **anidada**
  para evitarlo.
- c) ¿En qué escenario esperarías que la brecha entre el número "ingenuo" y el de la CV
  anidada sea más grande?

---

**10.** Tienes presupuesto para 20 evaluaciones de validación cruzada y dos hiperparámetros
que ajustar. ¿Elegirías grid search, random search u optimización bayesiana (Optuna)?
Justifica, y explica qué ganarías al aumentar el presupuesto a 200 evaluaciones con cada
método.

---

> **Puntuación:** cada pregunta vale 0.5 puntos, para un total de 5.0.

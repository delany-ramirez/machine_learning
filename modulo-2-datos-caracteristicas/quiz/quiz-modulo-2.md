# Quiz · Módulo 2 — Datos: preprocesamiento e ingeniería de características

**Sesiones 4–5** · 10 preguntas · Tiempo sugerido: **30 min** · Sin material de consulta

> Responde de forma breve y justificada. Se evalúa el razonamiento, no la extensión.

---

**1.** Un dataset tiene una columna `edad` con un 30 % de valores faltantes. Un compañero
propone `df.dropna()`. Da dos razones concretas por las que puede ser una mala idea, y describe
qué harías tú antes de decidir.

---

**2.** Explica la diferencia entre MCAR, MAR y MNAR con un ejemplo propio de cada uno.
Para el caso MAR, indica qué estrategia de imputación es apropiada y cuál sería incorrecta.

---

**3.** En un dataset de pacientes, la columna `nivel_colesterol` tiene un 45 % de faltantes. Al
investigar, descubres que solo se midió a los pacientes que el médico consideró de riesgo.

- a) ¿Qué mecanismo de ausencia es?
- b) ¿Por qué imputar con la mediana sería especialmente engañoso aquí?
- c) ¿Qué harías en su lugar?

---

**4.** Un dataset de 5.000 filas tiene 340 filas completamente idénticas. Describe el
procedimiento que seguirías antes de decidir si eliminarlas, y explica en qué situación
concreta **no** deberías hacerlo.

---

**5.** Tienes una variable `ingreso_mensual` cuyo diagrama de caja marca 200 outliers en la
cola alta, todos correspondientes a personas reales de altos ingresos.

- a) ¿Los eliminas? Justifica.
- b) Menciona dos alternativas a eliminarlos.
- c) ¿Qué modelos del curso se verían afectados por esos valores y cuáles no?

---

**6.** Estás preparando datos para un modelo de KNN. Tienes `edad` (18–65), `salario`
(1.000.000–20.000.000) y `antiguedad_meses` (0–400).

- a) ¿Qué problema hay si aplicas KNN directamente?
- b) ¿Cómo lo resuelves?
- c) Si en vez de KNN usaras un Random Forest, ¿cambiaría tu respuesta? ¿Por qué?

---

**7.** Explica la diferencia entre codificación one-hot y codificación ordinal. Da un ejemplo
de una variable donde la ordinal sea correcta y otro donde sea un error, explicando qué le
"dice" al modelo la codificación incorrecta.

---

**8.** Un compañero construye este flujo y reporta un 94 % de accuracy:

```python
X_escalado = StandardScaler().fit_transform(X)
X_sel = SelectKBest(f_classif, k=30).fit_transform(X_escalado, y)
puntajes = cross_val_score(modelo, X_sel, y, cv=5)
```

El dataset tiene 300 filas y 8.000 columnas.

- a) Identifica **los dos** errores y di cuál es mucho más grave.
- b) Explica por qué el más grave produce un resultado tan optimista en este dataset concreto.
- c) Reescribe el código correctamente.

---

**9.** Se quiere predecir si un cliente cancelará su suscripción el próximo mes. Para cada
variable candidata, indica si produce fuga de datos y por qué:

- a) Número de reclamos presentados en los últimos 6 meses.
- b) Fecha de la solicitud de cancelación.
- c) Promedio de uso del servicio en el mes que se quiere predecir.
- d) Antigüedad del cliente en meses.
- e) Si el equipo de retención lo contactó (después de que el sistema lo marcara como riesgo).

---

**10.** Explica qué garantiza un `Pipeline` de scikit-learn que no garantiza aplicar los mismos
pasos por separado. En tu respuesta menciona qué ocurre exactamente al llamar a `.fit()` y a
`.predict()`, y por qué el artefacto que se despliega en producción debe ser el pipeline
completo y no solo el modelo.

---

> **Puntuación:** cada pregunta vale 0.5 puntos, para un total de 5.0.

# Quiz · Módulo 6 — MLOps: trazabilidad y despliegue

**Sesión 14** · 10 preguntas · Tiempo sugerido: **30 min** · Sin material de consulta

> Responde de forma breve y justificada. Se evalúa el razonamiento, no la extensión.

---

**1.** Un equipo tiene en producción un modelo con AP 0.83 y nadie sabe con qué versión de
los datos se entrenó. Nombra los cuatro niveles de reproducibilidad del módulo 1 y di,
para cada uno, qué registra una corrida de MLflow que lo garantice.

---

**2.** En el registro de modelos de Wine Quality hay dos versiones: `campeon` (Extra-Trees,
AP 0.589, 12 MB) y `produccion` (gradient boosting, AP 0.547, 0.15 MB).

- a) ¿Por qué no coinciden? ¿Qué métricas, además de la AP, se registraron para poder
  decidirlo?
- b) ¿Qué cambia en el código de la API cuando se promueve una versión nueva a
  `produccion`?

---

**3.** Un compañero cambia una fila del CSV de Adult Census y reentrena: la AP en CV sale
idéntica hasta el sexto decimal. Concluye que "el cambio no importa y no hace falta
registrar el hash de los datos". Responde.

---

**4.** Escribe el contrato mínimo de un servicio de predicción (entrada, salida, errores)
para el modelo de estudiantes, y explica por qué la salida incluye el umbral y la versión
del modelo, y por qué un valor de `asistencia_pct = 250` debe devolver 422 y no una
predicción.

---

**5.** La API del módulo carga el modelo en el `lifespan` y no dentro de `/predict`; la
codificación `tinto → 1` vive en la API y no en el cliente. Justifica las dos decisiones
con una consecuencia concreta de hacer lo contrario.

---

**6.** Explica por qué en el `Dockerfile` se copia `requirements-api.txt` y se instalan las
dependencias **antes** de copiar el código, y por qué se instala `requirements-api.txt` en
vez del `pyproject.toml` del curso.

---

**7.** Define drift de datos, drift de concepto y drift de etiquetas con un ejemplo del
caso de estudiantes cada uno, y di cuál de los tres se puede detectar sin etiquetas y
cuál no.

---

**8.** En el notebook 02, entre los meses 13 y 18 el PSI de `trabaja` es 0.3–0.4 y la nota
media predicha cae 0.25, pero el RMSE del modelo no se mueve. Un gerente exige reentrenar
"porque los datos cambiaron". ¿Qué le respondes, y qué condición hacía que el modelo no
se degradara?

---

**9.** Tras un drift de concepto detectado en el mes 19, se reentrena al cerrar el mes 20.
Con todo el historial (1–20) el RMSE en los meses 22–24 es 0.42; con solo los meses 19–20,
0.36; sin reentrenar, 0.44. Explica por qué más datos dio peor resultado y qué
diagnóstico previo habría indicado con qué datos reentrenar.

---

**10.** En el ejercicio 02, la AP mensual de un clasificador de `aprobo` cae por debajo de
la carta de control en el mes 13, cuando solo hubo drift de datos, y vuelve a subir en el
mes 19, cuando hubo drift de concepto. ¿Qué propiedad de la AP explica ese
comportamiento, qué métrica lo evita, y qué te enseña sobre la elección de la métrica que
se vigila en producción?

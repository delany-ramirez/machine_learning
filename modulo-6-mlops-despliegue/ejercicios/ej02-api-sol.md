# Solución · Ejercicio 02 · Una API para el modelo de estudiantes, y su plan de monitoreo

> **Material del docente.** Se describe la estructura esperada y los números de
> referencia (semilla 42). El código completo es una adaptación directa de `api/`; aquí
> se indica qué cambia y qué debe salir.

## Parte A — El contrato primero

**A.1** `Estudiante` con: `edad: int` (18–60), `estrato: int` (1–6), `trabaja: bool`,
`promedio_anterior: float` (2.0–5.0), `horas_estudio_semana: float` (0–40),
`asistencia_pct: float` (0–100). Rangos con margen sobre los observados (edad 21–39,
horas 0.5–29.5, asistencia 55–100). `Prediccion` con `probabilidad_aprobar`, `en_riesgo`
(bool), `umbral`, `version_modelo`. Ejemplo: un estudiante típico (edad 26, estrato 3,
no trabaja, promedio 3.7, 9 horas, 87 %).

**A.2** La API devuelve la probabilidad de **aprobar** (lo que el modelo estima) y una
decisión `en_riesgo = probabilidad < umbral`, porque quien consume es un programa de
acompañamiento que actúa sobre los que probablemente **no** aprueban. El umbral se elige
por costos: no llamar a un estudiante que va a reprobar (falso "no riesgo") cuesta más que
llamar a uno que iba a aprobar (una llamada de más); con FN = 3 × FP sobre probabilidades
de CV el umbral sale en **0.85** y se marca en riesgo al 50 % de los estudiantes —
muchas llamadas, pocos reprobados sin llamar. La decisión de los costos es del programa,
no del modelo, y se documenta en el contrato.

## Parte B — Entrenar y servir

**B.1** Regresión logística con `StandardScaler` sobre los 400 estudiantes: AP en CV
**0.963 ± 0.005**, AUC **0.894**. (La AP es alta porque la prevalencia de `aprobo` es 0.74:
predecir "aprueba" siempre ya da AP 0.74. Es un detalle que reaparece en D.)

**B.2** El estudiante en riesgo (promedio 2.5, trabaja, 3 horas, 60 %) sale con
probabilidad de aprobar 0.005 y `en_riesgo = true`; el ejemplo típico, con 0.944.

**B.3** Las cinco pruebas siguen el patrón de `api/probar_api.py`. `estrato = 9` y
`asistencia_pct = 250` deben devolver 422 nombrando el campo.

**B.4** Latencia comparable a la de Wine Quality (mediana ≈ 2–3 ms, p95 ≈ 4 ms): el modelo
es aún más ligero (una logística), y el tiempo es HTTP y validación.

## Parte C — Empaquetar

**C.1** El `Dockerfile` cambia solo en el nombre de la carpeta y del módulo
(`api-estudiantes.main:app`). La imagen pesa ~350 MB; el entorno mínimo, ~270 MB. Sin
Docker: `uv venv` + `uv pip install -r requirements-api.txt` y `uvicorn` desde ese
entorno, como se verificó para la API del módulo.

**C.2** `.dockerignore`: `notebooks/` (desarrollo), `datos/` (entrenamiento, no
producción), `*.db` y `mlruns/` (tracking), `__pycache__/` (basura), `probar_api.py`
(pruebas), `entrenar_modelo.py` (entrenamiento). Solo entra lo que hace falta para
**predecir**.

## Parte D — El plan de monitoreo

**D.1** Capa 1 (referencia: meses 1–6). PSI de `trabaja` ≈ 0 en los meses 7–12 y
**0.23–0.42 desde el mes 13**; `promedio_anterior` 0.08–0.17 desde el 13; el PSI de la
probabilidad predicha, 0.02–0.04 antes y 0.16–0.32 después; la probabilidad media de
aprobar cae de 0.76 a 0.62–0.66. Todo salta en el mes 13 y **nada cambia en el 19**: la
capa 1 ve el drift de datos y es ciega al de concepto, como en el notebook 02.

**D.2** Capa 2. Aquí el ejercicio tiene una trampa que conviene que el estudiante
descubra. Con la **AP** como métrica (referencia 0.965 ± 0.006, umbral de alarma 0.947):

| Meses | AP mensual | Tasa de aprobación | AUC mensual |
|---|---|---|---|
| 7–12 | 0.955–0.970 | 0.74–0.82 | 0.86–0.92 |
| 13–18 (drift de datos) | **0.919–0.950** (alarma en 4 de 6 meses) | **0.61–0.67** | 0.88–0.91 |
| 19–24 (+ drift de concepto) | 0.935–0.961 (alarma en 3 de 6) | 0.73–0.80 | **0.82–0.87** |

La AP dispara en el mes 13, **con el drift de datos**, aunque la relación no cambió — y
lo hace porque la AP depende de la **prevalencia**: llegan más estudiantes que trabajan,
aprueban menos (0.74 → 0.65), y la AP de cualquier clasificador baja con la tasa base
(módulo 4, S9). Es drift de etiquetas (*prior shift*) disfrazado de pérdida de
desempeño. Y en los meses 19–24, cuando la relación sí cambia, la AP **vuelve a subir**
porque la tasa de aprobación vuelve a 0.79, y solo alarma a ratos.

El **AUC**, que no depende de la prevalencia, cuenta la historia correcta: se queda en
0.88–0.91 durante el drift de datos y cae a 0.82–0.87 con el drift de concepto (la
referencia era 0.89 ± 0.02, así que el umbral a tres desviaciones no dispara del todo;
con dos desviaciones o con una ventana de tres meses, sí). Lo mínimo exigible: que el
estudiante note que la AP alarma en el mes 13 sin que el modelo se haya degradado, y
proponga el AUC (o la AP **comparada con la prevalencia del mes**) para separar cambio
de tasa base de cambio de relación. Es la misma lección de los módulos 3 y 4 —la métrica
que se vigila decide lo que se ve— en producción.

**D.3** `monitoreo.md` debe contener, como mínimo:

- **Registro por petición**: marca de tiempo, versión del modelo y del contrato, las
  seis variables, la probabilidad y la decisión; sin `id_estudiante` en claro (o
  cifrado).
- **Capa 1, mensual**: PSI y KS por variable y de la probabilidad predicha contra los
  meses 1–6; alarma en 0.25 en cualquier variable o 0.1 en tres o más; aviso al equipo
  de datos.
- **Capa 2, al cerrar cada semestre**: AUC y AP por cohorte contra la carta de control
  (referencia: meses 7–12), con la prevalencia al lado; alarma a dos desviaciones en dos
  meses seguidos; aviso al programa de acompañamiento y al equipo de datos.
- **Protocolo ante alarma**: (1) capa 1 sola → comprobar rangos y esquema, reajustar el
  modelo sobre el periodo y comparar coeficientes; si no cambian, documentar y no
  reentrenar; (2) capa 2 → diagnóstico de coeficientes, reentrenar **desde el cambio**,
  comparación pareada contra producción sobre los meses recientes, versión nueva en el
  registro, despliegue con reversión posible.

## Lo que se espera cambiar de `api/` para el proyecto

Cualquiera de: versionar la ruta (`/v1/predict`); registrar cada petición en un archivo o
tabla para alimentar el monitoreo; devolver la prevalencia de referencia junto al umbral;
un `/health` que además compruebe que el modelo responde (una predicción de prueba);
autenticación por clave. Lo que no se espera: cambiar el principio de "contrato explícito,
validado antes del modelo, respuesta auditable".

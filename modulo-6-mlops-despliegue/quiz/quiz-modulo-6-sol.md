# Clave · Quiz Módulo 6 — MLOps: trazabilidad y despliegue

> **Material del docente.** Se indica lo mínimo exigible y, cuando aplica, el error típico
> que conviene comentar en la retroalimentación.

---

**1. Cuatro niveles de reproducibilidad**

| Nivel (módulo 1) | Qué registra la corrida |
|---|---|
| **Semilla** | `semilla` como parámetro (y la partición/CV que depende de ella) |
| **Entorno** | Versiones de Python y librerías como parámetros, y el `requirements.txt` / `python_env.yaml` que MLflow guarda junto al modelo |
| **Datos** | El **hash** (SHA-256) del archivo y su ruta; opcionalmente el número de filas |
| **Artefacto** | El modelo serializado con firma y ejemplo de entrada (`log_model`), más los artefactos de diagnóstico |

Y el enlace entre todos: el commit de Git del código. Error típico: registrar solo
métricas e hiperparámetros, que es lo que la interfaz muestra primero, y ninguno de los
cuatro niveles.

---

**2. `campeon` y `produccion`**

**a)** Porque la decisión de producción no se toma solo con la métrica de calidad: se
registraron **tamaño** del modelo serializado (12 MB frente a 0.15), **latencia** por
predicción (20× más lenta en el bosque) y tiempo de ajuste. Para una API que se descarga
en cada réplica y responde en tiempo real, 0.04 de AP no compensa 80× el tamaño. La razón
queda anotada como tag de la versión.

**b)** **Nada.** La API pide `models:/wine-buena@produccion` (o carga el artefacto
exportado de esa versión); promover es mover el alias a otra versión. Eso desacopla el
ciclo de entrenamiento del de despliegue. Error típico: pensar que promover implica
cambiar la ruta o el nombre del modelo en el código.

---

**3. La métrica no detecta cambios en los datos**

La conclusión está al revés. Que la AP no cambie con una fila alterada (un año en un
histograma de LightGBM cae en el mismo *bin*) demuestra que **la métrica no es un
detector de cambios en los datos**: una recarga con filas de menos, una columna
recodificada o una fuga pueden dejar la métrica igual o incluso subirla. El hash detecta
cualquier cambio de un byte, por eso se registra, y por eso la reproducción del notebook
01 empieza comprobando que el hash actual coincide con el registrado antes de comparar
la AP.

---

**4. El contrato**

Entrada: los seis campos con tipo y rango (edad entero 18–60, estrato entero 1–6,
`trabaja` booleano, promedio 2–5, horas 0–40, asistencia 0–100). Salida: probabilidad de
aprobar, decisión (`en_riesgo`), umbral, versión del modelo. Errores: 422 con el campo y
el motivo para tipo inválido, campo faltante o valor fuera de rango.

El umbral y la versión van en la salida para que quien consume pueda **interpretar y
auditar** la respuesta después: con qué criterio se decidió y con qué modelo, aunque el
modelo haya cambiado desde entonces. `asistencia_pct = 250` es casi con seguridad un error
de unidades o de columna: el modelo no ha visto nada parecido y extrapolaría; una
probabilidad devuelta con `200` se consumiría como válida. Rechazar con 422 es la primera
capa de defensa contra el drift burdo. Error típico: validar solo el tipo, no el rango.

---

**5. Dos decisiones de la API**

- **Cargar en el `lifespan`**: cargar un `joblib` tarda milisegundos y predecir
  microsegundos; hacerlo en cada petición multiplicaría la latencia por cien (medida: 2.7
  ms por petición con el modelo ya en memoria) y el consumo de memoria y disco bajo carga.
- **Codificación en la API**: `tinto → 1` es parte del modelo, no del dominio. Si la hace
  el cliente, cada cliente la reimplementa, alguno la invierte, y cuando el modelo cambie
  la codificación (por ejemplo, *one-hot*) habrá que cambiar a todos los clientes. El
  cliente habla en términos del dominio (`"tinto"`); la API traduce.

---

**6. El `Dockerfile`**

Docker construye por **capas** y reutiliza las que no cambian. Las dependencias cambian
poco y tardan minutos en instalarse; el código cambia en cada versión y se copia en
milisegundos. Con las dependencias antes, cambiar `main.py` no reinstala nada. Y
`requirements-api.txt` en vez de `pyproject.toml` porque la API necesita scikit-learn,
pandas, FastAPI y uvicorn (~270 MB) y el entorno del curso trae PyTorch, JupyterLab y
MLflow (1.6 GB): una imagen más pequeña se construye, se transfiere y arranca más rápido y
tiene menos superficie de fallo. Las versiones son las mismas de `uv.lock`, fijadas.

---

**7. Tres drifts**

- **Datos** (*covariate shift*): cambia $P(\mathbf{X})$; p. ej., llegan más estudiantes que
  trabajan. **Se detecta sin etiquetas** (PSI, KS sobre las entradas).
- **Concepto**: cambia $P(y \mid \mathbf{X})$; p. ej., las horas de estudio pesan menos en la
  nota por un cambio en la evaluación. **No se detecta sin etiquetas**: las entradas se
  ven iguales.
- **Etiquetas** (*prior shift*): cambia $P(y)$; p. ej., sube la tasa de reprobación. Se
  detecta parcialmente (la distribución de las predicciones se mueve) y desajusta el
  umbral y las métricas que dependen de la prevalencia (pregunta 10).

---

**8. Drift de datos sin daño**

Que el cambio en las entradas es real y está bien detectado, pero el modelo **no se ha
degradado**: el RMSE sigue en la carta de control, y eso es lo que decide reentrenar.
Reentrenar sin razón cuesta y arriesga (una versión nueva puede introducir errores). La
condición: el modelo era **correcto también en la región nueva** — la relación no cambió
(solo cambió quién llega) y la región (estudiantes que trabajan) estaba representada en
el entrenamiento (38 %). Si el cambio hubiera llevado a una región sin datos de
entrenamiento, o el modelo estuviera mal especificado, sí podría degradarse: el PSI alto
obliga a **comprobar el desempeño**, no a reentrenar.

---

**9. Más datos, peor resultado**

Porque los 18 meses anteriores al cambio obedecen a una relación que **ya no existe**
(coeficiente de horas 0.055) y diluyen la nueva (0.020): el modelo reentrenado con todo
queda a medio camino (coeficiente 0.051) y falla sobre los meses nuevos. Con drift de
concepto, los datos viejos no son más información sino información contradictoria. El
diagnóstico previo: **reajustar el mismo modelo sobre el periodo en alarma y comparar
coeficientes** (notebook 02, sección 4): al ver que el de horas cayó de 0.053 a 0.019 y el
intercepto subió, se sabe que cambió la relación y desde cuándo, y por tanto que hay que
reentrenar **desde el cambio**. Error típico: "reentrenar con todo siempre es mejor
porque hay más datos".

---

**10. La métrica que se vigila decide lo que se ve**

La **AP depende de la prevalencia**: con menos positivos, la AP de cualquier clasificador
baja aunque su capacidad de ordenar no cambie (módulo 4, S9: la AP de un clasificador
aleatorio es la prevalencia). En el mes 13 llegaron más estudiantes que trabajan y la tasa
de aprobación bajó de 0.74 a 0.65 (drift de etiquetas inducido por el de datos); la AP
cayó sin que la relación cambiara. En el mes 19 la tasa volvió a 0.79 y la AP subió, justo
cuando la relación sí cambió. El **AUC** no depende de la prevalencia: se mantuvo con el
drift de datos y cayó con el de concepto. Lección: en producción hay que vigilar una
métrica cuya variación signifique lo que se quiere detectar, reportar la prevalencia al
lado, y saber qué **no** mide la métrica elegida — la misma lección de los módulos 3 y 4
(RMSE frente a MAE, AUC frente a AP), ahora con consecuencias operativas.

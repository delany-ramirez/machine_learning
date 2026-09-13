# Ejercicio 02 · Una API para el modelo de estudiantes, y su plan de monitoreo

**Módulo 6 · Sesión 14** · Tiempo estimado: **90 min** · Con código

> **Objetivo.** Construir de punta a punta —contrato, script de entrenamiento, API,
> pruebas, imagen— el servicio de predicción del caso que el curso viene usando desde el
> módulo 1 (`rendimiento-estudiantes.csv`), y dejar escrito cómo se monitorearía con las
> cohortes del notebook 02. Es el ensayo general de la entrega E6 del proyecto integrador,
> sobre un caso conocido.

## Contexto

Datos: `rendimiento-estudiantes.csv` (módulos 1, 3, 5) para entrenar;
`cohortes-estudiantes.csv` (módulo 6) para el monitoreo. Modelo: regresión logística
para `aprobo` (con `StandardScaler`, `Pipeline` completo) sobre los seis predictores de
siempre. Parte de `api/` de este módulo como plantilla: copia la carpeta a
`api-estudiantes/` dentro de tu entrega y modifícala.

Entrega: la carpeta `api-estudiantes/` completa (código, modelo, pruebas, `Dockerfile`),
más un documento `monitoreo.md`.

## Parte A — El contrato primero (15 min)

**A.1** Escribe `esquemas.py` con la entrada `Estudiante` (seis campos con tipo y rango
válido tomados de los datos con margen; `trabaja` como booleano; `estrato` como entero
entre 1 y 6) y la salida `Prediccion` (probabilidad de aprobar, decisión, umbral, versión
del modelo). Añade un ejemplo en `json_schema_extra`.

**A.2** Decide y justifica en dos líneas: ¿la API devuelve la probabilidad de **aprobar**
o de **reprobar**? ¿Qué umbral usa, y con qué costos se eligió? (Piensa en quién consume
la predicción: un programa de acompañamiento que llama a los estudiantes en riesgo.)

## Parte B — Entrenar y servir (30 min)

**B.1** `entrenar_modelo.py`: entrena el `Pipeline`, elige el umbral por costos sobre
probabilidades de CV, y guarda `modelo-estudiantes.joblib` como diccionario con modelo,
columnas, umbral y metadatos (versión, fecha, hash del CSV, versión de scikit-learn, AP y
AUC en CV). Reporta AP y AUC.

**B.2** `main.py`: `/health` y `/predict` (y `/predict/lote`), con el modelo cargado en el
`lifespan`. Levántala con `uvicorn` y prueba desde `/docs` con el ejemplo y con un
estudiante en riesgo (promedio 2.5, trabaja, 3 horas, 60 % de asistencia).

**B.3** `probar_api.py` con al menos cinco pruebas: `/health`; una predicción con la forma
del contrato; un lote; rechazo de `estrato = 9` y de `asistencia_pct = 250`; y la
coincidencia entre la probabilidad de la API y la del modelo cargado directamente.

**B.4** Mide la latencia: 200 peticiones a `/predict`, mediana y p95. Compara con la de
la API de Wine Quality (`api/README.md`).

## Parte C — Empaquetar (15 min)

**C.1** `requirements-api.txt` con las versiones de `uv.lock`, y el `Dockerfile` adaptado.
Si tienes Docker: construye la imagen, ejecútala y consulta `/health` desde fuera del
contenedor; anota el tamaño de la imagen (`docker images`). Si no: crea un entorno
mínimo con `uv venv` + `uv pip install -r requirements-api.txt` y demuestra que la API
arranca desde él.

**C.2** ¿Qué archivos de tu carpeta **no** deben entrar en la imagen? Escribe el
`.dockerignore` y justifica cada línea en una palabra.

## Parte D — El plan de monitoreo (30 min)

Con `cohortes-estudiantes.csv` como si fueran las peticiones que la API recibió durante
24 meses (una cohorte por mes), y el modelo entrenado en B.1:

**D.1** Capa 1, sin etiquetas: PSI de cada variable y de la probabilidad predicha, mes a
mes, contra los meses 1–6. ¿En qué mes salta, en qué variables, y cuánto?

**D.2** Capa 2, con etiquetas: AP mensual de tu modelo contra una carta de control
construida con los meses 7–12. ¿En qué mes dispara? ¿Coincide con el salto de la capa 1?

**D.3** Escribe `monitoreo.md` (una página) con: qué se registra en cada petición; qué
se calcula cada mes en cada capa y con qué umbrales; a quién se avisa; y el protocolo
ante alarma (diagnóstico → decisión de reentrenar → con qué datos → cómo se valida y se
despliega la versión nueva). Usa los números de D.1 y D.2 como ejemplos.

## Entrega

La carpeta `api-estudiantes/`, `monitoreo.md`, y un párrafo con lo que **cambiarías** del
diseño de `api/` del módulo para tu proyecto integrador.

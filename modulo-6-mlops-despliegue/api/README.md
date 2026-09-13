# API de predicción · Wine Quality

Servicio HTTP que responde "¿es bueno este vino?" con el modelo del módulo 6. Es el
ejemplo de referencia para la entrega E6 del proyecto integrador.

## Archivos

| Archivo | Qué es |
|---|---|
| `main.py` | La aplicación FastAPI: carga el modelo al arrancar y expone `/health`, `/predict` y `/predict/lote` |
| `esquemas.py` | El **contrato**: qué campos entran (con rangos válidos) y qué campos salen, como modelos de Pydantic |
| `entrenar_modelo.py` | Entrena el modelo y escribe `modelo-ejemplo.joblib` con sus metadatos |
| `modelo-ejemplo.joblib` | El modelo servido (0.15 MB): `HistGradientBoostingClassifier` + columnas + umbral + metadatos. Se versiona porque es pequeño |
| `probar_api.py` | Seis pruebas del contrato, sin levantar servidor (`TestClient`) |
| `requirements-api.txt` | Las dependencias **mínimas** de la API, con las versiones exactas de `uv.lock`; lo que instala la imagen Docker |

## Ejecutar en local

Desde la carpeta del módulo (`modulo-6-mlops-despliegue/`), con el entorno del curso:

```bash
uv run uvicorn api.main:app --reload
```

- <http://localhost:8000/docs> — documentación interactiva (Swagger), generada a partir de
  los esquemas; permite enviar peticiones desde el navegador.
- <http://localhost:8000/health> — estado del servicio y del modelo cargado.

`--reload` reinicia el servidor al guardar un archivo; útil mientras se desarrolla, no en
producción.

## Probar

Con el servidor levantado, desde otra terminal:

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"fixed_acidity\": 7.3, \"volatile_acidity\": 0.25, \"citric_acid\": 0.39, \"residual_sugar\": 4.6, \"chlorides\": 0.036, \"free_sulfur_dioxide\": 21, \"total_sulfur_dioxide\": 88, \"density\": 0.9904, \"ph\": 3.16, \"sulphates\": 0.42, \"alcohol\": 13.0, \"tipo\": \"blanco\"}"
```

Respuesta:

```json
{"probabilidad": 0.7403, "buena": true, "umbral": 0.22, "version_modelo": "1.0.0"}
```

Un valor fuera de rango (por ejemplo `"alcohol": 94`) devuelve **422** con el campo y el
motivo, sin llegar al modelo. En PowerShell, `curl` es un alias de `Invoke-WebRequest` y
las comillas se escapan distinto; es más cómodo usar la página `/docs`.

Las pruebas automáticas, sin servidor:

```bash
uv run python -m api.probar_api
```

(o `uv run pytest api/probar_api.py -q` si prefieres pytest). Comprueban `/health`, una
predicción, un lote, el rechazo de valores fuera de rango y de campos faltantes, y que la
probabilidad de la API coincide con la del modelo cargado directamente.

## Reentrenar el modelo

```bash
uv run api/entrenar_modelo.py
```

Reescribe `modelo-ejemplo.joblib` con la fecha, el hash de los datos y las métricas
actualizadas; `/health` las reporta. Si cambia el umbral o las columnas, el contrato de
`esquemas.py` debe revisarse.

## Diseño

- **El modelo se carga una vez** (en el `lifespan` de la aplicación), no por petición.
  Latencia medida en local: mediana 2.7 ms por petición, p95 3.7 ms, casi toda en HTTP y
  validación; la predicción en sí tarda microsegundos.
- **La codificación de `tipo` (`tinto` → 1) vive en la API**, no en el cliente, porque es
  parte del modelo: el cliente habla en términos del dominio.
- **La respuesta incluye el umbral y la versión**: quien consume la API puede saber con qué
  decisión y con qué modelo se le respondió, y auditar después.
- Lo que **no** tiene, y un servicio real necesitaría: autenticación, registro de cada
  petición y respuesta (para el monitoreo del notebook 02), límites de tasa, y un
  `/predict` que devuelva también la versión del contrato.

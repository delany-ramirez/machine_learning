# 02 · APIs para modelos: del `predict_proba` al servicio

**Módulo 6 · Sesión 14** — De modelo a producto

## Objetivos

- Entender qué es una API HTTP y por qué es la forma habitual de poner un modelo a
  disposición de otras aplicaciones.
- Diseñar el **contrato** de un servicio de predicción: entradas, validación, salidas y
  errores.
- Conocer la estructura mínima de una API de inferencia con FastAPI y las decisiones que
  la hacen correcta y rápida.

## 1. Por qué una API

Un modelo entrenado es una función: recibe un vector de variables y devuelve una
probabilidad. Quien la necesita —una aplicación web, un sistema de matrículas, otro
equipo— no tiene el notebook, ni el entorno, ni debería tenerlos. La forma estándar de
ofrecer una función a través de la red es una **API HTTP**: el cliente envía una petición
con los datos, el servidor responde con la predicción, y ninguno sabe en qué lenguaje
está escrito el otro.

Las alternativas, y cuándo tienen sentido: predicción **por lotes** (un trabajo
programado que puntúa una tabla entera cada noche; más simple y suficiente cuando nadie
necesita la respuesta al instante) y **modelo embebido** (la librería del modelo dentro de
la aplicación; acopla los ciclos de vida y exige que la aplicación esté en Python). La
API es la opción por defecto cuando hay varios consumidores o se necesita respuesta en
tiempo real.

## 2. HTTP en lo que importa aquí

Una petición HTTP tiene un **método**, una **ruta**, cabeceras y, opcionalmente, un
**cuerpo**. Una respuesta tiene un **código de estado** y un cuerpo. Para un servicio de
predicción bastan:

| Método | Ruta | Cuerpo | Uso |
|---|---|---|---|
| `GET` | `/health` | — | ¿Está viva la API y qué modelo tiene cargado? Lo consulta el orquestador cada pocos segundos |
| `POST` | `/predict` | JSON con una observación | Una predicción |
| `POST` | `/predict/lote` | JSON con una lista | Varias predicciones en una petición (menos sobrecarga por observación) |

`GET` para leer sin efectos, `POST` para enviar datos. El cuerpo va en **JSON**: un
diccionario de campos con nombre, legible por cualquier lenguaje. Y los códigos de estado
dicen qué pasó sin leer el cuerpo:

| Código | Significa | Cuándo lo devuelve la API del curso |
|---|---|---|
| `200` | Correcto | Predicción hecha |
| `422` | Petición inválida (*Unprocessable Entity*) | Un campo falta, tiene el tipo equivocado o está fuera de rango |
| `500` | Error interno | Algo falló en el servidor (no debería ocurrir; si ocurre, es un bug) |
| `503` | Servicio no disponible | Habitual en servicios reales mientras el modelo se carga; la API del curso prefiere no arrancar si el modelo no carga, y así el orquestador lo detecta |

## 3. El contrato

Lo más importante de una API no es el código sino el **contrato**: qué entra, qué sale,
qué se rechaza. Se escribe antes que el código y se comparte con quien va a consumir el
servicio. Para la API del curso (`api/esquemas.py`):

**Entrada** (`Vino`): las 11 medidas fisicoquímicas como números y `tipo` como
`"tinto"` o `"blanco"`. Cada número tiene un **rango válido**, tomado del dataset de
entrenamiento con un margen. La razón: el modelo no ha visto nada fuera de ese rango y
extrapolaría sin avisar; un valor como `alcohol: 94` es casi con seguridad un error de
unidades, y es mejor rechazarlo con un mensaje claro que devolver una probabilidad
inventada. Es la primera línea de defensa contra el drift más burdo
(`04-monitoreo-y-drift.md`).

**Salida** (`Prediccion`): la probabilidad, la decisión con el umbral, **el umbral** y
**la versión del modelo**. Los dos últimos no son decorativos: quien consume la API puede
saber con qué criterio se le respondió y auditarlo después, y cuando el modelo cambie, las
respuestas antiguas seguirán siendo interpretables.

**Errores**: un `422` con la lista de campos inválidos y el motivo de cada uno. Nunca un
`200` con una predicción sobre datos malos.

Con **Pydantic** el contrato es código ejecutable: una clase con los campos, sus tipos y
sus restricciones (`Field(ge=..., le=...)`). FastAPI la usa para validar cada petición
antes de que llegue al modelo, para construir la respuesta, y para generar la
**documentación interactiva** (`/docs`) donde el consumidor ve los campos, prueba
peticiones y lee los ejemplos.

## 4. La aplicación

`api/main.py` tiene cuatro partes, y cada una responde a una decisión:

1. **Cargar el modelo una vez, al arrancar** (el `lifespan` de la aplicación), no en cada
   petición. Cargar un `joblib` tarda milisegundos y predecir microsegundos; una API que
   recargara el modelo por petición sería cien veces más lenta de lo necesario. Lo cargado
   es un diccionario —modelo, columnas, umbral, metadatos— producido por
   `api/entrenar_modelo.py`.
2. **Convertir la petición al formato exacto del entrenamiento**: un `DataFrame` con las
   mismas columnas, en el mismo orden, con `tipo` codificado igual (`tinto` → 1). Esa
   codificación **vive en la API**, no en el cliente, porque es parte del modelo; el
   cliente habla en términos del dominio.
3. **Predecir y aplicar el umbral** elegido en entrenamiento por costos (FN = 3 × FP,
   módulo 4). La API no decide el umbral: lo reporta.
4. **`/health`** devuelve los metadatos del modelo cargado: versión, fecha, hash de los
   datos, versión de scikit-learn, AP en prueba. Un orquestador lo usa para saber si el
   servicio está vivo; una persona, para saber qué está sirviendo sin abrir nada.

Medido en local (`api/README.md`): mediana 2.7 ms por petición, p95 3.7 ms. Casi todo es
HTTP y validación; el modelo tarda microsegundos. Un modelo 20 veces más lento (el
Extra-Trees de 12 MB) apenas se notaría en la latencia total — pero sí en la memoria y en
el tiempo de arranque de cada réplica.

## 5. Probar

Una API se prueba como cualquier código, y el contrato dice qué probar
(`api/probar_api.py`, con `TestClient`, sin levantar servidor):

- `/health` responde `200` con el estado esperado.
- Una observación válida devuelve exactamente los campos del contrato, con una
  probabilidad en $[0, 1]$ y una decisión coherente con el umbral.
- Un lote se procesa entero y conserva el orden.
- Un valor fuera de rango, un campo faltante y un tipo inválido devuelven `422`, y el
  error nombra el campo.
- La probabilidad de la API **coincide** con la del modelo cargado directamente: la API
  no altera la predicción.

Estas pruebas corren en segundos y son las que deben pasar antes de construir la imagen
(`03-empaquetado-y-despliegue.md`).

## 6. Lo que falta para producción

La API del curso es el mínimo correcto. Un servicio real añade:

- **Autenticación** (una clave por cliente) y **límites de tasa**.
- **Registro de cada petición y respuesta** (sin datos personales, o cifrados): es la
  materia prima del monitoreo del notebook 02, y de la auditoría.
- **Versionado del contrato** en la ruta (`/v1/predict`), para poder cambiar campos sin
  romper a los clientes existentes.
- **Tiempo máximo de respuesta** y qué hacer si el modelo no responde (una predicción por
  defecto, un error explícito).
- Observabilidad: métricas de latencia y de errores por endpoint, y trazas.

Ninguna cambia la idea: un contrato explícito, validado antes del modelo, con la
respuesta suficiente para auditar después.

## Referencias

- Documentación de FastAPI: <https://fastapi.tiangolo.com/> (tutorial; *lifespan events*;
  *testing*).
- Documentación de Pydantic v2: <https://docs.pydantic.dev/latest/> (*fields*, validación).
- Huyen, C. (2022). *Designing Machine Learning Systems*, cap. 7 (despliegue: lotes vs.
  en línea, latencia).

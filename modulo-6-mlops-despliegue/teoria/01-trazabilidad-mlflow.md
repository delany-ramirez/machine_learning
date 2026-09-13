# 01 · Trazabilidad: experimentos, corridas y registro de modelos

**Módulo 6 · Sesión 14** — De modelo a producto

## Objetivos

- Entender qué se pierde cuando los experimentos viven en notebooks y qué resuelve un
  sistema de *tracking*.
- Conocer las cuatro piezas de MLflow que usa el curso —corridas, artefactos, modelos con
  firma, registro con alias— y qué debe registrarse en cada corrida.
- Saber promover un modelo a producción de forma que la API no dependa de la versión
  concreta.

## 1. El problema: "¿de dónde salió ese 0.589?"

Los módulos 4 y 5 compararon una docena de modelos sobre Wine Quality. Los resultados
están en celdas impresas: para saber con qué hiperparámetros, qué partición, qué versión
de scikit-learn y qué archivo de datos salió cada número hay que leer el código y
confiar en que nadie lo cambió desde entonces. En un proyecto real, con varias personas y
meses de trabajo, esa confianza no existe, y la pregunta "¿podemos volver a producir el
modelo que está en producción?" suele tener una respuesta incómoda.

El módulo 1 definió cuatro niveles de reproducibilidad: **semilla**, **entorno**, **datos**
(hash) y **artefacto** (el modelo guardado). Un sistema de tracking los anota
automáticamente en cada entrenamiento, junto con los resultados, y los hace consultables.
Es la diferencia entre un cuaderno de laboratorio y una hoja suelta.

## 2. MLflow: corridas, experimentos y artefactos

**MLflow** (Zaharia et al., 2018; código abierto, agnóstico de librería) organiza el
trabajo en:

| Concepto | Qué es | En el notebook 01 |
|---|---|---|
| **Experimento** | Un problema; agrupa corridas | `wine-quality-buena` |
| **Corrida** (*run*) | Un entrenamiento: parámetros, métricas, tags, artefactos, modelo | una por candidato |
| **Parámetros** | Valores de entrada, texto: hiperparámetros y contexto | `n_estimators`, `datos.sha256`, `codigo.commit`, `semilla` |
| **Métricas** | Números de salida, opcionalmente por paso | `ap_cv`, `ap_cv_ee`, `tamano_mb`, `latencia_ms_por_fila` |
| **Tags** | Etiquetas libres para filtrar | `modelo.familia` |
| **Artefactos** | Archivos: figuras, tablas, el modelo | curva PR, AP por pliegue, `modelo/` |

Dos almacenes detrás: los **metadatos** (parámetros, métricas, tags) van a una base de
datos —SQLite en local, PostgreSQL en un servidor compartido— y los **artefactos** a una
carpeta o a un bucket. En el curso: `sqlite:///mlflow.db` y `mlruns/`, ambos fuera de
Git. Lo que se versiona con Git es el código que produce las corridas; lo que producen se
registra en MLflow. La interfaz web (`mlflow ui`) lee los mismos almacenes.

### Qué registrar en cada corrida

Lo mínimo para poder reproducirla y para poder decidir con ella:

1. **Hiperparámetros** del modelo y del preprocesamiento.
2. **Contexto**: hash del archivo de datos, commit del código, versiones de Python y de
   las librerías, semilla. Todo eso se obtiene con cuatro líneas y se olvida siempre.
3. **Métricas de calidad** con su incertidumbre: media **y** error estándar de la CV
   (módulo 3). Una métrica sin error estándar no permite comparar corridas.
4. **Métricas de despliegue**: tamaño del modelo serializado, latencia por predicción,
   tiempo de entrenamiento. No aparecen en ninguna tabla de los módulos anteriores y
   deciden despliegues: sobre Wine Quality, el mejor modelo en AP (Extra-Trees con 300
   árboles) pesa **12 MB** y predice 20 veces más lento que un gradient boosting de
   0.15 MB que pierde 0.04 de AP (`01-mlflow-aplicado.ipynb`, sección 4).
5. **Artefactos de diagnóstico**: la curva precisión-recall, la tabla por pliegue, la
   matriz de confusión — lo que se querría mirar después sin reentrenar.
6. **El modelo**, con su firma y sus dependencias (§3).

`mlflow.search_runs()` devuelve todo eso como un `DataFrame`, filtrable y ordenable; es
la tabla comparativa de los módulos 4 y 5, persistente.

## 3. El modelo como artefacto: firma y dependencias

`mlflow.sklearn.log_model` (y su equivalente por librería: `mlflow.lightgbm`,
`mlflow.pytorch`, …) guarda el modelo en un formato con tres cosas que un `pickle` suelto
no tiene:

- La **firma** (*signature*): los nombres y tipos de las columnas de entrada y el tipo de
  la salida. Permite validar una petición antes de predecir, y documenta el contrato.
- Un **ejemplo de entrada**, para probar el modelo cargado.
- Las **dependencias** (`requirements.txt`, `python_env.yaml`): las versiones exactas con
  las que se puede cargar. Un modelo de scikit-learn 1.9 no se garantiza cargable con 1.5.

Un detalle de seguridad: MLflow 3 guarda los modelos de scikit-learn en formato **skops**,
que a diferencia de `pickle` rechaza cargar tipos que no estén declarados (un `pickle` puede
ejecutar código arbitrario al cargarse). Por eso un modelo de LightGBM se registra con el
*flavor* de LightGBM y no con el de scikit-learn, aunque tenga la interfaz de
scikit-learn.

Cargar un modelo es `mlflow.sklearn.load_model(uri)`, donde el URI puede apuntar a una
corrida (`runs:/<id>/modelo`) o al registro (§4).

## 4. El registro de modelos: versiones y alias

Una corrida es un experimento. Un **modelo registrado** es una decisión: "este es el modelo
`wine-buena`". El registro (*Model Registry*) guarda **versiones numeradas** de un mismo
nombre, cada una enlazada a la corrida que la produjo, y permite ponerles **alias**:

- `campeon`: la mejor versión según la métrica de calidad.
- `produccion`: la versión que sirve la API.

No tienen por qué coincidir, y en el notebook 01 no coinciden: el campeón en AP es
Extra-Trees (versión 1, 12 MB) y producción es el gradient boosting (versión 2, 0.15 MB),
con la razón anotada como tag de la versión. El código de la API pide
`models:/wine-buena@produccion` y **no cambia** cuando se promueve una versión nueva:
promover es mover el alias. Eso desacopla el ciclo de entrenamiento del ciclo de
despliegue, que es lo que un equipo necesita para que el científico de datos y quien
opera el servicio no tengan que coordinarse línea a línea.

Con MLflow en local (SQLite), el registro funciona igual que con un servidor; solo cambia
la URI de tracking.

## 5. Reproducir

La prueba de que la trazabilidad sirve es **reproducir un número**: tomar una corrida,
leer de ella los hiperparámetros, la semilla y el hash de los datos, comprobar que el
archivo actual tiene el mismo hash, reentrenar, y obtener la misma AP hasta el último
decimal (`01-mlflow-aplicado.ipynb`, sección 6: 0.567139 en ambos casos). Si no sale
igual, algo no quedó registrado — y eso también es información.

Lo que no garantiza el registro: que el modelo siga siendo **bueno**. Eso lo responde el
monitoreo (`04-monitoreo-y-drift.md`).

## 6. Alternativas y cuándo usar cada una

| Herramienta | Tipo | Cuándo |
|---|---|---|
| **MLflow** | Código abierto, autoalojado o gestionado (Databricks) | Por defecto; funciona en local sin servidor |
| Weights & Biases, Neptune, Comet | Servicios en la nube con interfaz muy pulida | Equipos que ya pagan por ellos; deep learning con muchas corridas |
| DVC (módulo 1) + Git | Versiona datos y pipelines; `dvc exp` registra experimentos ligeros | Proyectos pequeños que ya usan DVC |
| Una hoja de cálculo | — | Nunca para esto: no enlaza con el código ni con los artefactos |

Para el proyecto integrador: MLflow en local, una corrida por modelo evaluado desde E3 en
adelante, y el modelo de E6 promovido en el registro con alias `produccion`.

## Referencias

- Zaharia, M. et al. (2018). Accelerating the machine learning lifecycle with MLflow.
  *IEEE Data Engineering Bulletin*.
- Documentación de MLflow: <https://mlflow.org/docs/latest/> (Tracking, Models, Model
  Registry).
- Sculley, D. et al. (2015). Hidden technical debt in machine learning systems. *NeurIPS*
  — por qué la trazabilidad y el monitoreo son la parte cara de un sistema de ML.

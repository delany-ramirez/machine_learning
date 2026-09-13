# Módulo 6 — MLOps: trazabilidad y despliegue (S14, 3.5 h)

> Estado: **completo** (Fase 6 de [`../PLAN.md`](../PLAN.md)).

## Objetivos

Al finalizar el módulo, el estudiante será capaz de registrar y comparar experimentos de
forma trazable y reproducible, elegir el modelo de producción con las métricas de calidad
**y** de despliegue a la vista, exponerlo como un servicio HTTP con un contrato validado,
empaquetarlo en un contenedor, y describir —con números— cómo se monitorea en producción,
qué cambio detecta cada capa del monitoreo y cuándo y con qué datos reentrenar.

## Contenidos

### ✅ Núcleo

- **S14** — MLflow: experimentos, corridas, artefactos, modelos con firma; qué registrar
  (hash de datos, commit, versiones, semilla, tamaño y latencia); `search_runs`; registro
  de modelos con versiones y alias; reproducir una corrida.
- **S14** — Serialización y versionado del modelo: `joblib`, skops, ONNX; el modelo como
  paquete (modelo + columnas + umbral + metadatos).
- **S14** — APIs: HTTP en lo que importa, el **contrato** (entrada con rangos, salida con
  umbral y versión, errores 422), FastAPI y Pydantic, pruebas del contrato.
- **S14** — Empaquetado con Docker: imagen, capas, dependencias mínimas fijadas, usuario
  sin privilegios; dónde ejecutar; cómo se cambia un modelo en producción (sombra,
  canario, reversión).
- **S14** — Monitoreo y drift: de datos, de concepto, de etiquetas; PSI, KS y distribución
  de las predicciones (sin etiquetas); carta de control del error (con etiquetas);
  diagnóstico; políticas de reentrenamiento y con qué datos.

### 🔵 Opcional

- `mlflow models serve` y otros servidores de modelos (teoría 03).
- Integración continua: las pruebas de `api/probar_api.py` como puerta antes de construir
  la imagen.
- Cierre: sustentación de los proyectos integradores.

## Materiales

### Teoría

| # | Documento | Tema |
|---|---|---|
| 01 | [`teoria/01-trazabilidad-mlflow.md`](teoria/01-trazabilidad-mlflow.md) | Por qué tracking; corridas, artefactos, modelos con firma y dependencias; registro con alias; reproducir; alternativas |
| 02 | [`teoria/02-apis-para-modelos.md`](teoria/02-apis-para-modelos.md) | Por qué una API; HTTP mínimo; el contrato; la aplicación línea a línea; probar; lo que falta para producción |
| 03 | [`teoria/03-empaquetado-y-despliegue.md`](teoria/03-empaquetado-y-despliegue.md) | Formatos de serialización y sus riesgos; el `Dockerfile` explicado; dónde ejecutar; despliegue con criterio |
| 04 | [`teoria/04-monitoreo-y-drift.md`](teoria/04-monitoreo-y-drift.md) | Tipos de drift; monitoreo sin y con etiquetas; diagnóstico; reentrenar cuándo y con qué; un sistema mínimo |

### Notebooks

| # | Notebook | Tipo | Contenido |
|---|---|---|---|
| 01 | [`notebooks/01-mlflow-aplicado.ipynb`](notebooks/01-mlflow-aplicado.ipynb) | aplicado | Seis candidatos de M4–M5 sobre Wine Quality como corridas de MLflow con contexto, métricas de calidad y de despliegue (tamaño, latencia), artefactos y modelo con firma; `search_runs`; registro con alias `campeon` y `produccion`; reproducción exacta de una corrida; exportación para la API |
| 02 | [`notebooks/02-drift-intuicion.ipynb`](notebooks/02-drift-intuicion.ipynb) | intuición | 24 meses simulados con drift plantado: PSI y KS por variable, distribución de las predicciones, carta de control del RMSE; drift de datos sin daño y drift de concepto invisible sin etiquetas; diagnóstico por coeficientes; cuatro estrategias de reentrenamiento medidas |

> **Hallazgo del notebook 01.** El mejor modelo en AP (Extra-Trees, 0.589) pesa **12 MB** y
> predice 20 veces más lento que el gradient boosting de 0.15 MB que pierde 0.04 de AP.
> El campeón y el modelo de producción no tienen por qué ser el mismo, y las métricas que
> lo deciden —tamaño, latencia— no aparecían en ninguna tabla de los módulos anteriores.
> Con los parámetros, la semilla y el hash de los datos registrados, la AP se reproduce
> hasta el sexto decimal.
>
> **Hallazgo del notebook 02.** El drift de **datos** (mes 13: PSI de `trabaja` de 0 a
> 0.3–0.4, nota predicha media de 3.42 a 3.16) se detecta el mismo mes sin etiquetas y **no
> degrada** al modelo (RMSE 0.34, dentro de la carta de control): la relación no cambió y
> el modelo era correcto en la región nueva. El drift de **concepto** (mes 19) sube el RMSE
> un 30 % y **no se ve** en ninguna entrada. Tras reentrenar, todo el historial apenas
> ayuda (0.42); solo los datos posteriores al cambio recuperan el error de referencia
> (0.36): con drift de concepto, más datos no es mejor.

### Código de despliegue

| Ruta | Contenido |
|---|---|
| [`api/main.py`](api/main.py) | API FastAPI: modelo cargado en el `lifespan`, `/health`, `/predict`, `/predict/lote` |
| [`api/esquemas.py`](api/esquemas.py) | El contrato en Pydantic: 11 medidas con rango válido + `tipo`; salida con probabilidad, decisión, umbral y versión |
| [`api/entrenar_modelo.py`](api/entrenar_modelo.py) | Entrena el `HistGradientBoostingClassifier` de la versión `produccion` y escribe `modelo-ejemplo.joblib` con columnas, umbral por costos y metadatos |
| [`api/modelo-ejemplo.joblib`](api/modelo-ejemplo.joblib) | El modelo servido (0.15 MB; versionado) |
| [`api/probar_api.py`](api/probar_api.py) | Seis pruebas del contrato con `TestClient` |
| [`api/requirements-api.txt`](api/requirements-api.txt) | Dependencias mínimas de la API con las versiones exactas de `uv.lock` |
| [`api/README.md`](api/README.md) | Cómo ejecutar, probar y reentrenar; decisiones de diseño; latencia medida |
| [`docker/Dockerfile`](docker/Dockerfile) | Imagen del servicio sobre la imagen oficial de uv con Python 3.11 |
| [`docker/README.md`](docker/README.md) | Construir, ejecutar, el `Dockerfile` línea a línea, por qué no se instala todo el `pyproject.toml` |
| [`.dockerignore`](.dockerignore) | Lo que no entra en la imagen |

**Verificado:** las seis pruebas pasan; la API levantada con `uvicorn` responde a `curl`
(`/health`, `/predict`, 422 fuera de rango) con mediana 2.7 ms y p95 3.7 ms por petición;
y arranca desde un entorno construido **solo** con `requirements-api.txt` (272 MB), que es
lo que hace el `Dockerfile`. La imagen no se construyó con `docker build` (sin Docker en
la máquina del docente); ver la nota en `docker/README.md`.

### Datos

| Archivo | Descripción | Por qué este |
|---|---|---|
| [`datos/wine-quality.csv`](datos/wine-quality.csv) | Los mismos vinos de los módulos 4 y 5 | El notebook 01 registra en MLflow los modelos ya conocidos (AP 0.52–0.59) y la API sirve el elegido |
| [`datos/preparar-wine-quality.py`](datos/preparar-wine-quality.py) | Descarga y prepara Wine Quality (copiado del módulo 4) | Procedencia |
| [`datos/cohortes-estudiantes.csv`](datos/cohortes-estudiantes.csv) | 24 meses × 300 estudiantes del proceso de `rendimiento-estudiantes.csv`, con **drift de datos desde el mes 13** (más estudiantes que trabajan, promedio 0.15 menor) y **drift de concepto desde el 19** (coeficiente de horas 0.055 → 0.020, intercepto +0.45) | Conocer el proceso generador permite comprobar qué detecta cada herramienta de monitoreo y cuál se queda ciega, como en el módulo 1 |
| [`datos/generar-cohortes-drift.py`](datos/generar-cohortes-drift.py) | Generador con semilla fija; documenta qué cambia y cuándo | Reproducible byte a byte |

### Ejercicios

| # | Enunciado | Solución | Duración |
|---|---|---|---|
| 01 | [`ejercicios/ej01-mlflow.md`](ejercicios/ej01-mlflow.md) | [`ej01-mlflow-sol.md`](ejercicios/ej01-mlflow-sol.md) | 60 min |
| 02 | [`ejercicios/ej02-api.md`](ejercicios/ej02-api.md) | [`ej02-api-sol.md`](ejercicios/ej02-api-sol.md) | 90 min |

El 01 registra en MLflow los modelos de **Adult Census** (módulos 4 y 5) con métricas de
despliegue —y descubre que allí campeón y producción sí coinciden (LightGBM: mejor AP,
0.15 MB, el más rápido)— y rompe la reproducibilidad a propósito: cambiar una fila del
CSV deja la AP idéntica hasta el sexto decimal; solo el hash lo detecta. El 02 construye
de punta a punta la API del **modelo de estudiantes** (contrato, entrenamiento, pruebas,
imagen) y su plan de monitoreo sobre las cohortes, con una trampa medida: la AP mensual
del clasificador de `aprobo` dispara con el drift de datos —porque la prevalencia bajó de
0.74 a 0.65— y vuelve a subir con el de concepto; el AUC, que no depende de la
prevalencia, cuenta la historia correcta.

### Quiz

| Archivo | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-6.md`](quiz/quiz-modulo-6.md) | [`quiz-modulo-6-sol.md`](quiz/quiz-modulo-6-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E6 — Entrega final.** Los modelos del proyecto registrados en MLflow (una corrida por
modelo evaluado desde E3, con hash de datos, métricas de calidad con error estándar y
métricas de despliegue), el modelo final promovido con alias `produccion`, expuesto como
API con contrato validado y pruebas, empaquetado (Dockerfile, aunque no se construya), un
documento de monitoreo de una página (qué se registra, qué se calcula en cada capa, con
qué umbrales, y el protocolo ante alarma), más el informe final del caso y su
sustentación. Ver [`../proyecto-integrador/`](../proyecto-integrador/).

---

> Docker solo se necesita en este módulo; si no puedes instalarlo, la API se ejecuta
> igual con `uv run uvicorn api.main:app` y el empaquetado se demuestra con un entorno
> mínimo (`uv venv` + `uv pip install -r api/requirements-api.txt`). Ver
> [`docker/README.md`](docker/README.md) y [`../docs/guia-entorno.md`](../docs/guia-entorno.md).

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml); el notebook 01 crea `mlflow.db` y `mlruns/`
> en `notebooks/` (ambos fuera de Git). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

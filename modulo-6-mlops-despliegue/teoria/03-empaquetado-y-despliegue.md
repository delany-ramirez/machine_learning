# 03 · Empaquetado y despliegue: serializar, contener, ejecutar

**Módulo 6 · Sesión 14** — De modelo a producto

## Objetivos

- Saber qué se guarda cuando se "guarda un modelo", con qué formato y qué riesgos tiene
  cada uno.
- Entender qué problema resuelve Docker y leer un `Dockerfile` línea a línea.
- Conocer las opciones de despliegue y el criterio para elegir entre ellas.

## 1. Serializar: el modelo como archivo

Un modelo entrenado es un objeto en memoria. Para que otro proceso —la API, mañana, en
otra máquina— lo use, hay que escribirlo en disco. Opciones:

| Formato | Qué es | Ventaja | Riesgo |
|---|---|---|---|
| `pickle` / **`joblib`** | Serialización nativa de objetos Python; `joblib` comprime bien los arreglos de NumPy | Universal en el ecosistema de scikit-learn; una línea | **Ejecuta código al cargar**: un `pickle` malicioso puede hacer cualquier cosa. Solo cargar archivos de origen conocido. Atado a las versiones de las librerías |
| **skops** | Formato seguro para scikit-learn; solo carga tipos declarados | Sin ejecución de código arbitrario; es el que usa MLflow 3 | Solo scikit-learn (y librerías que lo adopten) |
| **ONNX** | Grafo de cómputo independiente del lenguaje | Se ejecuta desde C++, Java, JavaScript, móviles; rápido | Conversión no siempre completa; cada operador debe estar soportado |
| Formato propio de la librería (`LightGBM` `.txt`, PyTorch `state_dict`, `SavedModel`) | Lo que la librería define | Estable entre versiones de esa librería | Solo esa librería |

El curso usa `joblib` para la API (`api/modelo-ejemplo.joblib`) por simplicidad, con dos
precauciones: el archivo viene del propio repositorio, y no se guarda **solo el modelo**
sino un diccionario con el modelo, la lista de columnas esperadas, el umbral y los
metadatos (versión, fecha, hash de los datos, versión de scikit-learn, métricas). Un
modelo sin sus columnas y su umbral es una función sin documentación.

Dos reglas que evitan la mayoría de los accidentes:

- **Serializar el `Pipeline` completo**, preprocesamiento incluido (módulo 2). Si el
  escalador o el codificador quedan fuera, la API tiene que reimplementarlos, y en algún
  momento divergen.
- **Fijar la versión de la librería** con la que se guardó. scikit-learn avisa al cargar un
  modelo guardado con otra versión, y no garantiza compatibilidad. El `requirements.txt`
  que MLflow escribe junto al modelo, o `requirements-api.txt` en la API, es esa
  garantía.

Y una medida que ya apareció en el notebook 01: el **tamaño**. Extra-Trees con 300
árboles sin podar sobre 4256 vinos pesa 12 MB; el gradient boosting elegido, 0.15 MB.
Para un archivo en Git, para una imagen de contenedor que se descarga en cada réplica y
para el tiempo de arranque, la diferencia importa.

## 2. El problema que resuelve un contenedor

"En mi máquina funciona" tiene tres causas: otra versión de Python, otras versiones de
las librerías, otro sistema operativo (o librerías del sistema, como OpenMP para
LightGBM). El entorno virtual del módulo 0 resuelve las dos primeras dentro de una
máquina. Un **contenedor** resuelve las tres en cualquier máquina: es un proceso que corre
con su propio sistema de archivos —Python, dependencias, código, modelo— aislado del
sistema anfitrión, construido a partir de una **imagen** que se describe con un
`Dockerfile` y que se puede copiar tal cual a otro servidor.

No es una máquina virtual: comparte el núcleo del sistema operativo anfitrión, arranca
en segundos y pesa lo que pesan sus archivos (la imagen de la API del curso, unos
350 MB con Python y las dependencias).

### El `Dockerfile` de la API, línea a línea

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
WORKDIR /app
COPY api/requirements-api.txt ./
RUN uv pip install --system --no-cache -r requirements-api.txt
COPY api/ ./api/
RUN useradd --create-home servicio
USER servicio
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- `FROM`: la imagen base. La oficial de `uv` con Python **3.11** —la misma versión de
  `.python-version`— sobre Debian *slim*, sin nada que no haga falta.
- `COPY requirements` + `RUN uv pip install` **antes** de `COPY api/`: Docker construye la
  imagen por **capas** y reutiliza las que no cambian. Las dependencias cambian poco y
  tardan; el código cambia siempre y es instantáneo. En ese orden, cambiar una línea de
  `main.py` no reinstala nada.
- `requirements-api.txt`, no `pyproject.toml`: la API necesita scikit-learn, pandas,
  FastAPI y uvicorn, no PyTorch ni JupyterLab. Las versiones son las mismas de `uv.lock`,
  fijadas; el entorno resultante pesa ~270 MB frente a 1.6 GB del entorno del curso.
  Verificado: la API arranca y responde desde un entorno construido solo con ese archivo.
- `USER servicio`: el proceso no corre como root dentro del contenedor. Si alguien
  explota una vulnerabilidad de la API, no tiene privilegios.
- `EXPOSE` documenta el puerto; `-p 8000:8000` al ejecutar lo publica.
- `CMD`: el proceso del contenedor. `--host 0.0.0.0` para aceptar conexiones desde fuera
  del contenedor (con `127.0.0.1` el servicio solo se vería a sí mismo).

`.dockerignore` deja fuera del contexto lo que no debe entrar en la imagen (notebooks,
datos, `mlruns/`): más rápido de construir y sin datos de entrenamiento en producción.

### Construir, ejecutar, publicar

```bash
docker build -f docker/Dockerfile -t wine-api .      # construir la imagen
docker run --rm -p 8000:8000 wine-api                 # ejecutarla
docker tag wine-api registro/wine-api:1.0.0           # etiquetar por versión del modelo
docker push registro/wine-api:1.0.0                   # publicarla en un registro de imágenes
```

La etiqueta de la imagen debería coincidir con la versión del modelo que lleva dentro
(`/health` la reporta): la imagen **es** el artefacto desplegable, y su etiqueta el
enlace con el registro de modelos del notebook 01.

## 3. Dónde ejecutarlo

| Opción | Qué es | Cuándo |
|---|---|---|
| **Sin contenedor** (`uv run uvicorn …` en un servidor con el entorno del curso) | Lo mismo que en local | Demostraciones, un único servidor que administra uno mismo. Es la alternativa del curso si no se puede instalar Docker |
| **Contenedor en un servidor** (`docker run`, `docker compose`) | Una máquina propia o alquilada | Pocos servicios, control total, sin escalar |
| **Servicio gestionado de contenedores** (Cloud Run, Azure Container Apps, AWS App Runner / ECS) | Se entrega la imagen; el proveedor la ejecuta, escala y reinicia | El punto de partida habitual: sin administrar servidores, se paga por uso |
| **Orquestador** (Kubernetes) | Coordina muchos contenedores, réplicas, despliegues graduales | Muchos servicios, equipos de plataforma |
| **Funciones sin servidor** (Lambda, Cloud Functions) | Código que se ejecuta por petición, sin proceso permanente | Tráfico esporádico; el arranque en frío (cargar el modelo en cada nueva instancia) penaliza modelos grandes |
| **Servidores de modelos** (`mlflow models serve`, BentoML, TorchServe, Triton) | Una API genérica ya escrita alrededor de un modelo registrado | Prototipos rápidos; menos control sobre el contrato |

El criterio: empezar por lo más simple que cumpla los requisitos de latencia, tráfico y
disponibilidad, y medir. Un servicio gestionado con una imagen como la del curso cubre
la mayoría de los casos de un proyecto de este tamaño.

## 4. Despliegue con criterio: cómo se cambia un modelo en producción

Sustituir el modelo de producción por uno nuevo es una decisión con riesgo, y hay formas
de tomarla con datos en vez de fe:

- **Sombra** (*shadow*): el modelo nuevo recibe las mismas peticiones que el viejo, sus
  predicciones se registran pero no se usan. Se compara sin afectar a nadie.
- **Canario**: el modelo nuevo atiende una fracción pequeña del tráfico (5 %); si sus
  métricas y su latencia van bien, se amplía.
- **Prueba A/B**: dos modelos atienden fracciones comparables y se mide el resultado de
  negocio (no solo la métrica técnica: módulo 1, S2).
- **Reversión** (*rollback*): volver al modelo anterior debe ser una operación de un
  minuto — mover el alias `produccion` a la versión previa y redesplegar la imagen
  anterior. Si revertir es difícil, nadie se atreve a desplegar.

Todas necesitan lo mismo: versiones identificables (registro + etiquetas de imagen) y
registro de peticiones y respuestas (`04-monitoreo-y-drift.md`).

## Referencias

- Documentación de Docker: <https://docs.docker.com/get-started/> y la referencia del
  `Dockerfile`.
- Imágenes oficiales de uv: <https://docs.astral.sh/uv/guides/integration/docker/>.
- Huyen, C. (2022). *Designing Machine Learning Systems*, caps. 7 y 9.
- Documentación de skops: <https://skops.readthedocs.io/> (persistencia segura).

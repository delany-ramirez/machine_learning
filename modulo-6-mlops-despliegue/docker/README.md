# Empaquetar la API con Docker

Un contenedor es la forma de garantizar que la API corre igual en tu máquina, en la del
docente y en un servidor: la imagen lleva **su propio Python, sus dependencias con
versiones exactas, el código y el modelo**. Es el último nivel de reproducibilidad del
módulo 1 —el entorno— llevado hasta el sistema operativo.

## Requisitos

[Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, con WSL 2;
macOS; o Docker Engine en Linux). Comprueba con `docker --version`. Si no puedes
instalarlo, la API se ejecuta igual sin contenedor con `uv run uvicorn api.main:app`
(ver [`../api/README.md`](../api/README.md)); lo que pierdes es el empaquetado, no el
servicio.

## Construir la imagen

Desde la carpeta del módulo (`modulo-6-mlops-despliegue/`), que es el **contexto** de
construcción — de ahí salen los archivos que `COPY` mete en la imagen; `.dockerignore`
excluye lo que no hace falta (notebooks, datos, teoría):

```bash
docker build -f docker/Dockerfile -t wine-api .
```

La primera vez descarga la imagen base (~150 MB) e instala las dependencias; las
siguientes reutilizan las capas que no cambiaron. Si solo cambió `api/main.py`, no se
reinstala nada.

## Ejecutar

```bash
docker run --rm -p 8000:8000 wine-api
```

`-p 8000:8000` conecta el puerto 8000 del contenedor con el 8000 de tu máquina; `--rm`
borra el contenedor al pararlo (Ctrl + C). Después, igual que en local:

```bash
curl http://localhost:8000/health
```

y <http://localhost:8000/docs> en el navegador.

## Qué hace cada línea del `Dockerfile`

| Instrucción | Por qué |
|---|---|
| `FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim` | Imagen oficial de `uv` con Python **3.11** (la versión de `.python-version`) sobre Debian slim: pequeña y con el mismo gestor del curso |
| `WORKDIR /app` | Carpeta de trabajo dentro del contenedor |
| `COPY api/requirements-api.txt` + `RUN uv pip install --system …` | Instala **solo** las dependencias de la API, con las versiones exactas de `uv.lock`. Va antes que el código para que esta capa (la lenta) se reutilice cuando solo cambia el código |
| `COPY api/ ./api/` | El código y el modelo. Es la capa que cambia en cada versión |
| `RUN useradd … ` + `USER servicio` | El servicio no corre como root dentro del contenedor |
| `EXPOSE 8000` | Documenta el puerto (no lo publica; eso lo hace `-p` al ejecutar) |
| `CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", …]` | El proceso del contenedor. `0.0.0.0` para aceptar conexiones desde fuera del contenedor (con `127.0.0.1` solo se vería a sí mismo) |

## Por qué no se instala todo el `pyproject.toml`

El entorno del curso pesa 1.6 GB (PyTorch, JupyterLab, MLflow, …). La API necesita
scikit-learn, pandas, FastAPI y uvicorn: `requirements-api.txt` los fija con las mismas
versiones de `uv.lock`, y el entorno resultante pesa ~270 MB. Una imagen más pequeña se
construye, se transfiere y arranca más rápido, y tiene menos superficie de fallo. Si
cambian las versiones en `uv.lock`, hay que actualizar `requirements-api.txt` (el
encabezado del archivo dice cómo).

## Verificación

- Verificado: la API arranca y responde desde un entorno construido **solo** con
  `requirements-api.txt` (`uv venv` + `uv pip install -r`), que es exactamente lo que hace
  el `Dockerfile`.
- La construcción de la imagen con `docker build` no se ha podido ejecutar en la máquina
  del docente (sin Docker Desktop instalado). Si al construirla algo falla, lo más probable
  es la etiqueta de la imagen base; la lista actual está en
  <https://github.com/astral-sh/uv/pkgs/container/uv>.

## Siguientes pasos (fuera del alcance del curso)

- Publicar la imagen en un registro (Docker Hub, GitHub Container Registry) con una
  etiqueta por versión del modelo.
- Ejecutarla en un servicio gestionado (Cloud Run, Azure Container Apps, ECS) o en un
  servidor con `docker compose`.
- Añadir un *health check* al contenedor (`HEALTHCHECK` con `curl /health`) para que el
  orquestador reinicie el servicio si deja de responder.

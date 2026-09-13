# Imagen del servicio de inferencia (modulo 6, sesion 14).
#
# Construir y ejecutar desde modulo-6-mlops-despliegue/ (el contexto es la carpeta del modulo):
#   docker build -f docker/Dockerfile -t wine-api .
#   docker run --rm -p 8000:8000 wine-api
# y probar:  curl http://localhost:8000/health
#
# Base: la imagen oficial de uv con Python 3.11 (la misma version que .python-version),
# sobre Debian slim. uv instala las dependencias fijadas de api/requirements-api.txt en el
# Python del sistema del contenedor: no hace falta un entorno virtual dentro de la imagen.

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Primero las dependencias (cambian poco): esta capa se reutiliza entre construcciones.
COPY api/requirements-api.txt ./
RUN uv pip install --system --no-cache -r requirements-api.txt

# Despues el codigo y el modelo (cambian mas).
COPY api/ ./api/

# Un usuario sin privilegios para ejecutar el servicio.
RUN useradd --create-home servicio
USER servicio

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

"""API de inferencia para el modelo de Wine Quality (módulo 6, sesión 14).

Dos endpoints, los mínimos de cualquier servicio de predicción:

    GET  /health   → ¿está viva la API y qué modelo tiene cargado?
    POST /predict  → una observación, una predicción
    POST /predict/lote → varias observaciones en una petición

Ejecutar en local, desde modulo-6-mlops-despliegue/:
    uv run uvicorn api.main:app --reload
y abrir http://localhost:8000/docs para la documentación interactiva (generada a partir de
los esquemas de esquemas.py).

El modelo se carga UNA vez al arrancar (lifespan), no en cada petición: cargar un joblib
tarda milisegundos, predecir microsegundos, y una API que recargara el modelo por
petición sería cien veces más lenta de lo necesario.
"""

from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI

from .esquemas import LoteVinos, Prediccion, PrediccionLote, Salud, Vino

RUTA_MODELO = Path(__file__).parent / "modelo-ejemplo.joblib"
recursos = {}


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    paquete = joblib.load(RUTA_MODELO)                      # arranque: cargar el modelo
    recursos.update(paquete)
    yield
    recursos.clear()                                        # apagado: liberar


app = FastAPI(
    title="Wine Quality · API de predicción",
    description="¿Es bueno este vino (quality ≥ 7)? Modelo del módulo 6 del curso de Machine Learning.",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)


def a_dataframe(vinos: list[Vino]) -> pd.DataFrame:
    """Convierte las observaciones validadas al formato exacto que vio el modelo en entrenamiento."""
    filas = [v.model_dump() for v in vinos]
    datos = pd.DataFrame(filas)
    datos["tipo"] = (datos["tipo"] == "tinto").astype(int)   # la misma codificación del entrenamiento
    return datos[recursos["columnas"]]                        # mismas columnas, mismo orden


def predecir(datos: pd.DataFrame) -> list[Prediccion]:
    probabilidades = recursos["modelo"].predict_proba(datos)[:, 1]
    umbral = recursos["umbral"]
    version = recursos["metadatos"]["version"]
    return [Prediccion(probabilidad=round(float(p), 4), buena=bool(p >= umbral), umbral=umbral, version_modelo=version)
            for p in probabilidades]


@app.get("/health", response_model=Salud, summary="Estado del servicio y del modelo cargado")
def health():
    m = recursos["metadatos"]
    return Salud(estado="ok", version_modelo=m["version"], algoritmo=m["algoritmo"],
                 fecha_entrenamiento=m["fecha_entrenamiento"], datos_sha256=m["datos_sha256"],
                 sklearn=m["sklearn"], ap_prueba=m["ap_prueba"])


@app.post("/predict", response_model=Prediccion, summary="Predicción para un vino")
def predict(vino: Vino):
    return predecir(a_dataframe([vino]))[0]


@app.post("/predict/lote", response_model=PrediccionLote, summary="Predicción para varios vinos")
def predict_lote(lote: LoteVinos):
    predicciones = predecir(a_dataframe(lote.vinos))
    return PrediccionLote(predicciones=predicciones, n=len(predicciones))

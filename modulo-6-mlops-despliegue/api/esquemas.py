"""Contrato de la API: qué entra y qué sale, validado con Pydantic.

Los rangos de cada variable son los del dataset de entrenamiento con un margen (el modelo
no ha visto nada fuera de ellos y extrapolaría). Un valor fuera de rango devuelve un error
422 con el campo y el motivo, antes de llegar al modelo. Es la primera línea de defensa
contra el drift más burdo: unidades equivocadas, columnas intercambiadas, nulos.
"""

from typing import Literal

from pydantic import BaseModel, Field


class Vino(BaseModel):
    """Una observación con las 11 medidas fisicoquímicas y el tipo de vino."""

    fixed_acidity: float = Field(ge=3.0, le=17.0, description="Acidez fija (g/L de ácido tartárico)")
    volatile_acidity: float = Field(ge=0.05, le=2.0, description="Acidez volátil (g/L de ácido acético)")
    citric_acid: float = Field(ge=0.0, le=2.0, description="Ácido cítrico (g/L)")
    residual_sugar: float = Field(ge=0.5, le=70.0, description="Azúcar residual (g/L)")
    chlorides: float = Field(ge=0.005, le=0.7, description="Cloruros (g/L de cloruro de sodio)")
    free_sulfur_dioxide: float = Field(ge=1.0, le=300.0, description="SO₂ libre (mg/L)")
    total_sulfur_dioxide: float = Field(ge=5.0, le=450.0, description="SO₂ total (mg/L)")
    density: float = Field(ge=0.98, le=1.05, description="Densidad (g/cm³)")
    ph: float = Field(ge=2.5, le=4.2, description="pH")
    sulphates: float = Field(ge=0.2, le=2.2, description="Sulfatos (g/L de sulfato de potasio)")
    alcohol: float = Field(ge=7.5, le=15.5, description="Alcohol (% vol.)")
    tipo: Literal["tinto", "blanco"] = Field(description="Tipo de vino")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"fixed_acidity": 7.4, "volatile_acidity": 0.70, "citric_acid": 0.00, "residual_sugar": 1.9,
                 "chlorides": 0.076, "free_sulfur_dioxide": 11.0, "total_sulfur_dioxide": 34.0, "density": 0.9978,
                 "ph": 3.51, "sulphates": 0.56, "alcohol": 9.4, "tipo": "tinto"}
            ]
        }
    }


class LoteVinos(BaseModel):
    """Varias observaciones en una sola petición."""

    vinos: list[Vino] = Field(min_length=1, max_length=1000)


class Prediccion(BaseModel):
    probabilidad: float = Field(description="Probabilidad estimada de que el vino sea bueno (quality ≥ 7)")
    buena: bool = Field(description="Decisión con el umbral del modelo")
    umbral: float = Field(description="Umbral de decisión usado (elegido por costos en entrenamiento)")
    version_modelo: str


class PrediccionLote(BaseModel):
    predicciones: list[Prediccion]
    n: int


class Salud(BaseModel):
    estado: Literal["ok"]
    version_modelo: str
    algoritmo: str
    fecha_entrenamiento: str
    datos_sha256: str
    sklearn: str
    ap_prueba: float

"""Pruebas de la API sin levantar un servidor (TestClient de FastAPI).

Uso, desde modulo-6-mlops-despliegue/:
    uv run python -m api.probar_api
o con pytest:
    uv run pytest api/probar_api.py -q

Comprueba lo que un contrato debe garantizar: que /health responde, que una observación
válida produce una predicción con la forma acordada, que un lote se procesa entero, que
los valores fuera de rango y los campos que faltan se rechazan con 422 antes de llegar al
modelo, y que la predicción coincide con la del modelo cargado directamente.
"""

import joblib
import pandas as pd
from fastapi.testclient import TestClient

from .main import RUTA_MODELO, app

EJEMPLO = {"fixed_acidity": 7.4, "volatile_acidity": 0.70, "citric_acid": 0.00, "residual_sugar": 1.9,
           "chlorides": 0.076, "free_sulfur_dioxide": 11.0, "total_sulfur_dioxide": 34.0, "density": 0.9978,
           "ph": 3.51, "sulphates": 0.56, "alcohol": 9.4, "tipo": "tinto"}
BUENO = {"fixed_acidity": 7.3, "volatile_acidity": 0.25, "citric_acid": 0.39, "residual_sugar": 4.6,
         "chlorides": 0.036, "free_sulfur_dioxide": 21.0, "total_sulfur_dioxide": 88.0, "density": 0.9904,
         "ph": 3.16, "sulphates": 0.42, "alcohol": 13.0, "tipo": "blanco"}


def test_health():
    with TestClient(app) as cliente:
        r = cliente.get("/health")
        assert r.status_code == 200
        cuerpo = r.json()
        assert cuerpo["estado"] == "ok" and cuerpo["algoritmo"] == "HistGradientBoostingClassifier"


def test_predict_un_vino():
    with TestClient(app) as cliente:
        r = cliente.post("/predict", json=EJEMPLO)
        assert r.status_code == 200
        cuerpo = r.json()
        assert set(cuerpo) == {"probabilidad", "buena", "umbral", "version_modelo"}
        assert 0.0 <= cuerpo["probabilidad"] <= 1.0
        assert cuerpo["buena"] == (cuerpo["probabilidad"] >= cuerpo["umbral"])


def test_predict_lote():
    with TestClient(app) as cliente:
        r = cliente.post("/predict/lote", json={"vinos": [EJEMPLO, BUENO]})
        assert r.status_code == 200
        cuerpo = r.json()
        assert cuerpo["n"] == 2 and len(cuerpo["predicciones"]) == 2
        assert cuerpo["predicciones"][1]["probabilidad"] > cuerpo["predicciones"][0]["probabilidad"]


def test_rechaza_fuera_de_rango():
    with TestClient(app) as cliente:
        r = cliente.post("/predict", json={**EJEMPLO, "alcohol": 94.0})      # ¿% o g/L? Fuera de rango
        assert r.status_code == 422
        assert "alcohol" in str(r.json()["detail"][0]["loc"])


def test_rechaza_campo_faltante_y_tipo_invalido():
    with TestClient(app) as cliente:
        sin_ph = {k: v for k, v in EJEMPLO.items() if k != "ph"}
        assert cliente.post("/predict", json=sin_ph).status_code == 422
        assert cliente.post("/predict", json={**EJEMPLO, "tipo": "rosado"}).status_code == 422


def test_coincide_con_el_modelo():
    paquete = joblib.load(RUTA_MODELO)
    fila = pd.DataFrame([{**EJEMPLO, "tipo": 1}])[paquete["columnas"]]
    p_directa = float(paquete["modelo"].predict_proba(fila)[0, 1])
    with TestClient(app) as cliente:
        p_api = cliente.post("/predict", json=EJEMPLO).json()["probabilidad"]
    assert abs(p_api - p_directa) < 1e-4


if __name__ == "__main__":
    pruebas = [v for k, v in globals().items() if k.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print(f"{len(pruebas)} pruebas superadas")

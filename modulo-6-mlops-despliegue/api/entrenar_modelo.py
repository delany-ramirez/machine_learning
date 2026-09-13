"""Entrena el modelo que sirve la API y lo guarda en modelo-ejemplo.joblib.

Es el HistGradientBoostingClassifier de la version `produccion` del notebook
01-mlflow-aplicado (0.15 MB, microsegundos por prediccion), entrenado sobre Wine Quality
con la misma particion de los modulos 4 y 5. El umbral de decision se elige por costo
(FN = 3 x FP, como en el modulo 4) sobre probabilidades de validacion cruzada.

El archivo guardado es un diccionario, no solo el modelo: lleva las columnas esperadas,
el umbral, y metadatos (version, fecha, hash de los datos, versiones de librerias,
metricas) para que la API pueda reportarlos en /health y nadie tenga que adivinar con
que se entreno.

Uso, desde la raiz del repositorio:
    uv run modulo-6-mlops-despliegue/api/entrenar_modelo.py
"""

import hashlib
import platform
from datetime import date
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split

SEMILLA = 42
COSTO_FP, COSTO_FN = 1, 3
VERSION = "1.0.0"
RUTA_DATOS = Path(__file__).parent.parent / "datos" / "wine-quality.csv"
RUTA_MODELO = Path(__file__).parent / "modelo-ejemplo.joblib"


def cargar_datos():
    vinos = pd.read_csv(RUTA_DATOS)
    vinos["tipo"] = (vinos["tipo"] == "tinto").astype(int)
    vinos = vinos.drop_duplicates().reset_index(drop=True)
    vinos["buena"] = (vinos["quality"] >= 7).astype(int)
    X = vinos.drop(columns=["quality", "buena"])
    y = vinos["buena"]
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEMILLA)


def umbral_de_minimo_costo(y, p):
    umbrales = np.round(np.linspace(0.05, 0.95, 91), 2)
    costos = [COSTO_FP * np.sum((p >= u) & (y == 0)) + COSTO_FN * np.sum((p < u) & (y == 1)) for u in umbrales]
    return float(umbrales[int(np.argmin(costos))])


def main():
    X_train, X_test, y_train, y_test = cargar_datos()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)
    modelo = HistGradientBoostingClassifier(random_state=SEMILLA)

    p_cv = cross_val_predict(modelo, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
    umbral = umbral_de_minimo_costo(y_train.to_numpy(), p_cv)
    modelo.fit(X_train, y_train)
    p_test = modelo.predict_proba(X_test)[:, 1]

    paquete = {
        "modelo": modelo,
        "columnas": list(X_train.columns),
        "umbral": umbral,
        "metadatos": {
            "version": VERSION,
            "fecha_entrenamiento": date.today().isoformat(),
            "algoritmo": type(modelo).__name__,
            "datos": RUTA_DATOS.name,
            "datos_sha256": hashlib.sha256(RUTA_DATOS.read_bytes()).hexdigest()[:12],
            "filas_entrenamiento": int(len(X_train)),
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "ap_cv": round(float(average_precision_score(y_train, p_cv)), 4),
            "ap_prueba": round(float(average_precision_score(y_test, p_test)), 4),
            "auc_prueba": round(float(roc_auc_score(y_test, p_test)), 4),
            "costos_umbral": {"FP": COSTO_FP, "FN": COSTO_FN},
        },
    }
    joblib.dump(paquete, RUTA_MODELO, compress=3)
    print(f"Guardado {RUTA_MODELO} ({RUTA_MODELO.stat().st_size / 1e6:.2f} MB)")
    for k, v in paquete["metadatos"].items():
        print(f"  {k}: {v}")
    print(f"  umbral: {umbral}")


if __name__ == "__main__":
    main()

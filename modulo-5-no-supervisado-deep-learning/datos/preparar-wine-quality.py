"""Descarga y prepara el dataset conductor de los modulos 4 y 5: Wine Quality.

Fuente: Cortez, P., Cerdeira, A., Almeida, F., Matos, T. y Reis, J. (2009).
"Modeling wine preferences by data mining from physicochemical properties."
Decision Support Systems, 47(4), 547-553. Publicado en el UCI Machine Learning
Repository (licencia CC BY 4.0) como dos archivos separados, uno por tipo de
vino (tinto y blanco), con separador ';'.

Este script une los dos archivos en un solo CSV con una columna `tipo`
('tinto'/'blanco'), normaliza los encabezados a snake_case y guarda
`wine-quality.csv`. Es idempotente: si el archivo ya existe, no descarga.
El CSV resultante pesa <1 MB, asi que se versiona en git.
"""

import urllib.request
from pathlib import Path

import pandas as pd

URL_BASE = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
ARCHIVOS = {"tinto": "winequality-red.csv", "blanco": "winequality-white.csv"}
RUTA_SALIDA = Path(__file__).parent / "wine-quality.csv"


def a_snake_case(nombre: str) -> str:
    return nombre.strip().lower().replace(" ", "_")


def preparar() -> pd.DataFrame:
    if RUTA_SALIDA.exists():
        print(f"{RUTA_SALIDA.name} ya existe, no se descarga de nuevo.")
        return pd.read_csv(RUTA_SALIDA)

    partes = []
    for tipo, archivo in ARCHIVOS.items():
        url = URL_BASE + archivo
        print(f"Descargando {url} ...")
        with urllib.request.urlopen(url) as respuesta:
            parte = pd.read_csv(respuesta, sep=";")
        parte["tipo"] = tipo
        partes.append(parte)

    df = pd.concat(partes, ignore_index=True)
    df.columns = [a_snake_case(c) for c in df.columns]

    df.to_csv(RUTA_SALIDA, index=False)
    print(f"Guardado {RUTA_SALIDA} — {df.shape[0]} filas, {df.shape[1]} columnas.")
    return df


if __name__ == "__main__":
    preparar()

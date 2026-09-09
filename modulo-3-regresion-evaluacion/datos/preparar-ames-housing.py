"""Descarga y prepara el dataset conductor del modulo 3: Ames Housing.

Fuente: De Cock, D. (2011). "Ames, Iowa: Alternative to the Boston Housing
Data as an End of Semester Regression Project." Journal of Statistics
Education, 19(3). Datos de dominio publico servidos como CSV por
https://github.com/wblakecannon/ames (copia estable del dataset original
del USDA/Ames City Assessor).

Este script es idempotente: si `ames-housing.csv` ya existe, no vuelve a
descargar. Se versiona el CSV resultante (pesa <1 MB), no el script se
ejecuta en cada notebook.
"""

import urllib.request
from pathlib import Path

import pandas as pd

URL_ORIGEN = (
    "https://raw.githubusercontent.com/wblakecannon/ames/"
    "refs/heads/master/data/housing.csv"
)
RUTA_SALIDA = Path(__file__).parent / "ames-housing.csv"

# Columnas identificadoras sin valor predictivo (indice de fila, orden del
# archivo original, identificador catastral).
COLUMNAS_ID = ["Unnamed: 0", "Order", "PID"]


def a_snake_case(nombre: str) -> str:
    return (
        nombre.strip()
        .lower()
        .replace("/", "_")
        .replace(" ", "_")
    )


def preparar() -> pd.DataFrame:
    if RUTA_SALIDA.exists():
        print(f"{RUTA_SALIDA.name} ya existe, no se descarga de nuevo.")
        return pd.read_csv(RUTA_SALIDA)

    print(f"Descargando desde {URL_ORIGEN} ...")
    with urllib.request.urlopen(URL_ORIGEN) as respuesta:
        df = pd.read_csv(respuesta)

    df = df.drop(columns=COLUMNAS_ID)
    df.columns = [a_snake_case(c) for c in df.columns]

    df.to_csv(RUTA_SALIDA, index=False)
    print(f"Guardado {RUTA_SALIDA} — {df.shape[0]} filas, {df.shape[1]} columnas.")
    return df


if __name__ == "__main__":
    preparar()

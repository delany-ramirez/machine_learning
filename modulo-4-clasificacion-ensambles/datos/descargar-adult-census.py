"""Descarga y prepara el dataset secundario del modulo 4: Adult Census Income.

Fuente: Kohavi, R. y Becker, B. (1996). Extraido del censo de EE. UU. de 1994.
UCI Machine Learning Repository (licencia CC BY 4.0). Viene en dos archivos
sin encabezado, `adult.data` (32 561 filas) y `adult.test` (16 281 filas, con
una linea de comentario al inicio y un punto final en las etiquetas).

Este script une ambos archivos, nombra las columnas en snake_case, convierte el
marcador ' ?' en valor faltante, y crea el objetivo binario `ingreso_alto`
(1 si el ingreso anual supera 50 000 USD). Guarda `adult-census.csv`.

El CSV resultante pesa ~5 MB, por encima del umbral de 1 MB de
docs/convenciones.md, asi que NO se versiona: esta en .gitignore y cada
estudiante lo genera una vez con:

    python descargar-adult-census.py

Es idempotente: si el archivo ya existe, no descarga.
"""

import urllib.request
from pathlib import Path

import pandas as pd

URL_BASE = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/"
RUTA_SALIDA = Path(__file__).parent / "adult-census.csv"

COLUMNAS = [
    "edad", "tipo_empleo", "fnlwgt", "educacion", "anos_educacion",
    "estado_civil", "ocupacion", "relacion", "raza", "sexo",
    "ganancia_capital", "perdida_capital", "horas_semana", "pais_origen",
    "ingreso",
]


def leer(archivo: str, saltar: int) -> pd.DataFrame:
    url = URL_BASE + archivo
    print(f"Descargando {url} ...")
    with urllib.request.urlopen(url) as respuesta:
        df = pd.read_csv(
            respuesta,
            header=None,
            names=COLUMNAS,
            skiprows=saltar,
            skipinitialspace=True,
            na_values="?",
        )
    df["particion_original"] = "train" if archivo == "adult.data" else "test"
    return df


def preparar() -> pd.DataFrame:
    if RUTA_SALIDA.exists():
        print(f"{RUTA_SALIDA.name} ya existe, no se descarga de nuevo.")
        return pd.read_csv(RUTA_SALIDA)

    df = pd.concat([leer("adult.data", 0), leer("adult.test", 1)], ignore_index=True)

    # En adult.test las etiquetas terminan en punto ('>50K.'); se unifican.
    df["ingreso"] = df["ingreso"].str.rstrip(".")
    df["ingreso_alto"] = (df["ingreso"] == ">50K").astype(int)
    df = df.drop(columns=["ingreso"])

    df.to_csv(RUTA_SALIDA, index=False)
    print(
        f"Guardado {RUTA_SALIDA} — {df.shape[0]} filas, {df.shape[1]} columnas, "
        f"{df['ingreso_alto'].mean():.1%} de ingresos altos."
    )
    return df


if __name__ == "__main__":
    preparar()

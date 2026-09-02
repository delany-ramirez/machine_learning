"""Descarga el dataset conductor del módulo 2: titanic.csv

Fuente: repositorio `seaborn-data` (https://github.com/mwaskom/seaborn-data), que a su vez
lo toma del conjunto clásico del Titanic usado en docencia desde hace décadas. Dominio
público.

El archivo pesa ~57 KB, así que **también está versionado en el repositorio**: no necesitas
ejecutar este script salvo que quieras regenerarlo. Se incluye para documentar la
procedencia exacta de los datos, que es parte de la reproducibilidad (sesión 2).

El script es idempotente: si el archivo ya existe, no lo vuelve a descargar.

Uso:
    python descargar-titanic.py
    python descargar-titanic.py --forzar
"""

import sys
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
SALIDA = Path(__file__).parent / "titanic.csv"


def descargar(forzar: bool = False) -> Path:
    if SALIDA.exists() and not forzar:
        print(f"Ya existe: {SALIDA.name} ({SALIDA.stat().st_size:,} bytes). Nada que hacer.")
        return SALIDA

    print(f"Descargando desde {URL} ...")
    with urllib.request.urlopen(URL, timeout=60) as respuesta:
        contenido = respuesta.read()

    SALIDA.write_bytes(contenido)
    print(f"Escrito: {SALIDA.name} ({len(contenido):,} bytes)")
    return SALIDA


if __name__ == "__main__":
    ruta = descargar(forzar="--forzar" in sys.argv)

    # Resumen mínimo para confirmar que el archivo está bien.
    import pandas as pd

    datos = pd.read_csv(ruta)
    print(f"\nFilas: {len(datos)}  Columnas: {len(datos.columns)}")
    print(f"Tasa de supervivencia: {datos['survived'].mean():.1%}")
    print("\nValores faltantes por columna:")
    faltantes = datos.isna().sum()
    print(faltantes[faltantes > 0].to_string())

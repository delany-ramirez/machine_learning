"""Genera el dataset conductor del módulo 1: rendimiento-estudiantes.csv

Datos **sintéticos** de rendimiento académico de estudiantes de posgrado. Se generan con una
semilla fija, de modo que el archivo es totalmente reproducible: cualquiera puede volver a
crearlo ejecutando este script.

Se usan datos simulados a propósito por dos razones:

1. No hay problemas de licencia ni de privacidad (son estudiantes ficticios).
2. Conocemos el proceso generador real, así que podemos comparar lo que el modelo *estima*
   con lo que de verdad ocurre. Eso es imposible con datos reales y muy útil para aprender.

El dominio (rendimiento y aprobación de estudiantes) anticipa el del proyecto integrador.

Uso:
    python generar-rendimiento-estudiantes.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 42
N = 400
SALIDA = Path(__file__).parent / "rendimiento-estudiantes.csv"

# --- Coeficientes "verdaderos" del proceso generador -------------------------------------
# En un problema real nunca los conocemos; aquí sí, y por eso podremos verificar en el
# notebook 01 qué tan cerca queda el modelo ajustado de estos valores.
COEFICIENTES_REALES = {
    "intercepto": -0.15,
    "promedio_anterior": 0.62,
    "horas_estudio_semana": 0.055,
    "asistencia_pct": 0.011,
    "trabaja": -0.22,
}
RUIDO_SIGMA = 0.35


def generar(semilla: int = SEMILLA, n: int = N) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)

    programa = rng.choice(
        ["Sistemas", "Industrial", "Electrica", "Civil"],
        size=n,
        p=[0.40, 0.25, 0.20, 0.15],
    )
    edad = np.clip(rng.normal(27, 4.5, n), 21, 48).round(0).astype(int)
    estrato = rng.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.08, 0.22, 0.32, 0.22, 0.11, 0.05])

    # Quien trabaja tiende a estudiar menos horas: la variable "trabaja" influye tanto
    # directamente en la nota como indirectamente a través de las horas de estudio.
    trabaja = rng.binomial(1, 0.38, n)

    promedio_anterior = np.clip(rng.normal(3.65, 0.48, n), 2.0, 5.0)
    horas_estudio_semana = np.clip(
        rng.gamma(shape=4.0, scale=2.4, size=n) - 3.0 * trabaja, 0.5, 30.0
    )
    asistencia_pct = np.clip(rng.normal(86 - 6 * trabaja, 9, n), 40, 100)

    nota_final = (
        COEFICIENTES_REALES["intercepto"]
        + COEFICIENTES_REALES["promedio_anterior"] * promedio_anterior
        + COEFICIENTES_REALES["horas_estudio_semana"] * horas_estudio_semana
        + COEFICIENTES_REALES["asistencia_pct"] * asistencia_pct
        + COEFICIENTES_REALES["trabaja"] * trabaja
        + rng.normal(0, RUIDO_SIGMA, n)
    )
    nota_final = np.clip(nota_final, 0.0, 5.0)

    datos = pd.DataFrame(
        {
            "id_estudiante": [f"E{i:04d}" for i in range(1, n + 1)],
            "programa": programa,
            "edad": edad,
            "estrato": estrato,
            "trabaja": trabaja,
            "promedio_anterior": promedio_anterior.round(2),
            "horas_estudio_semana": horas_estudio_semana.round(1),
            "asistencia_pct": asistencia_pct.round(1),
            "nota_final": nota_final.round(2),
        }
    )
    # Variable objetivo alternativa, para los ejemplos de clasificación.
    datos["aprobo"] = (datos["nota_final"] >= 3.0).astype(int)
    return datos


if __name__ == "__main__":
    datos = generar()
    datos.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"Escrito: {SALIDA}")
    print(f"Filas: {len(datos)}  Columnas: {len(datos.columns)}")
    print(f"Tasa de aprobacion: {datos['aprobo'].mean():.1%}")
    print(f"Nota final - media: {datos['nota_final'].mean():.2f}  "
          f"min: {datos['nota_final'].min():.2f}  max: {datos['nota_final'].max():.2f}")

"""Genera cohortes-estudiantes.csv: 24 meses de estudiantes con drift plantado.

Reutiliza el proceso generador de rendimiento-estudiantes.csv (módulo 1) para producir
una cohorte mensual de 300 estudiantes durante 24 meses, con dos cambios deliberados que
el notebook 02-drift-intuicion.ipynb tiene que detectar:

- Meses 1-12: el proceso original, sin cambios (solo cambia la semilla por mes).
- Meses 13-24: **drift de datos** (covariate shift). Cambia la población: la fracción de
  estudiantes que trabajan sube de 0.38 a 0.65 (y con ella bajan las horas de estudio y la
  asistencia, que dependen de `trabaja`), y el promedio anterior baja 0.15. La relación
  entre variables y nota sigue siendo la misma.
- Meses 19-24: además, **drift de concepto**. Cambia la relación: el coeficiente de
  `horas_estudio_semana` cae de 0.055 a 0.020 y el intercepto sube 0.45 para que la nota
  media no se mueva de forma evidente (un cambio de política de evaluación, por ejemplo).
  Las distribuciones de las variables de entrada no cambian respecto a los meses 13-18.

Como en el módulo 1, conocer el proceso generador permite comprobar qué detecta cada
herramienta de monitoreo y cuál se queda ciega.

Uso:
    python generar-cohortes-drift.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 42
N_MES = 300
MESES = 24
SALIDA = Path(__file__).parent / "cohortes-estudiantes.csv"

COEFICIENTES_ORIGINALES = {
    "intercepto": -0.15,
    "promedio_anterior": 0.62,
    "horas_estudio_semana": 0.055,
    "asistencia_pct": 0.011,
    "trabaja": -0.22,
}
RUIDO_SIGMA = 0.35

MES_DRIFT_DATOS = 13      # desde este mes cambia la población
MES_DRIFT_CONCEPTO = 19   # desde este mes cambia además la relación


def coeficientes(mes: int) -> dict:
    c = dict(COEFICIENTES_ORIGINALES)
    if mes >= MES_DRIFT_CONCEPTO:
        c["horas_estudio_semana"] = 0.020
        c["intercepto"] = COEFICIENTES_ORIGINALES["intercepto"] + 0.45
    return c


def generar_mes(mes: int, n: int = N_MES) -> pd.DataFrame:
    rng = np.random.default_rng(SEMILLA + mes)
    drift_datos = mes >= MES_DRIFT_DATOS
    p_trabaja = 0.65 if drift_datos else 0.38
    media_promedio = 3.50 if drift_datos else 3.65

    programa = rng.choice(["Sistemas", "Industrial", "Electrica", "Civil"], size=n, p=[0.40, 0.25, 0.20, 0.15])
    edad = np.clip(rng.normal(27, 4.5, n), 21, 48).round(0).astype(int)
    estrato = rng.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.08, 0.22, 0.32, 0.22, 0.11, 0.05])
    trabaja = rng.binomial(1, p_trabaja, n)
    promedio_anterior = np.clip(rng.normal(media_promedio, 0.48, n), 2.0, 5.0)
    horas_estudio_semana = np.clip(rng.gamma(shape=4.0, scale=2.4, size=n) - 3.0 * trabaja, 0.5, 30.0)
    asistencia_pct = np.clip(rng.normal(86 - 6 * trabaja, 9, n), 40, 100)

    c = coeficientes(mes)
    nota_final = (
        c["intercepto"]
        + c["promedio_anterior"] * promedio_anterior
        + c["horas_estudio_semana"] * horas_estudio_semana
        + c["asistencia_pct"] * asistencia_pct
        + c["trabaja"] * trabaja
        + rng.normal(0, RUIDO_SIGMA, n)
    )
    nota_final = np.clip(nota_final, 0.0, 5.0)

    return pd.DataFrame({
        "mes": mes,
        "id_estudiante": [f"M{mes:02d}-{i:03d}" for i in range(1, n + 1)],
        "programa": programa,
        "edad": edad,
        "estrato": estrato,
        "trabaja": trabaja,
        "promedio_anterior": promedio_anterior.round(2),
        "horas_estudio_semana": horas_estudio_semana.round(1),
        "asistencia_pct": asistencia_pct.round(1),
        "nota_final": nota_final.round(2),
    })


def generar() -> pd.DataFrame:
    return pd.concat([generar_mes(m) for m in range(1, MESES + 1)], ignore_index=True)


if __name__ == "__main__":
    datos = generar()
    datos.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"Escrito: {SALIDA}  ({len(datos)} filas, {MESES} meses de {N_MES})")
    resumen = datos.groupby("mes").agg(trabaja=("trabaja", "mean"), horas=("horas_estudio_semana", "mean"),
                                       nota=("nota_final", "mean")).round(2)
    print(resumen.loc[[1, 12, 13, 18, 19, 24]].to_string())

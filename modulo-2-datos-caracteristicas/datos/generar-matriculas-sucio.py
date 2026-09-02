"""Genera el dataset del ejercicio 01: matriculas-sucio.csv

Datos **sintéticos** de solicitudes de admisión a posgrado, con problemas de calidad
**plantados a propósito**. Cada defecto corresponde a un tema de la sesión 4:

| Problema plantado | Tema |
|---|---|
| `estado_civil` escrito de varias formas | Inconsistencia de formato |
| `-999` en `ingresos_hogar` | Faltante disfrazado |
| `"N/D"`, `"-"`, celda vacía en `puntaje_examen` | Faltantes disfrazados y tipo texto |
| `promedio_pregrado` con coma decimal | Convención local de números |
| Nulos en `experiencia_anios` correlacionados con `modalidad` | Faltante MAR |
| Nulos masivos en `nota_entrevista` | Faltante MNAR (solo se entrevista a algunos) |
| Filas repetidas con el mismo `id_solicitud` | Duplicados **reales** |
| Filas distintas con valores idénticos | Duplicados **aparentes** |
| Edad de 210 años y una negativa | Outliers por error de registro |
| Ingresos muy altos legítimos | Outlier legítimo |
| `admitido_texto` | Fuga de datos: copia del objetivo |
| `fecha_solicitud` como texto | Variable a descomponer |

La semilla está fija: el archivo es reproducible.

Uso:
    python generar-matriculas-sucio.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 7
N = 600
SALIDA = Path(__file__).parent / "matriculas-sucio.csv"


def generar(semilla: int = SEMILLA, n: int = N) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)

    programa = rng.choice(["Sistemas", "Industrial", "Electrica"], n, p=[0.45, 0.33, 0.22])
    modalidad = rng.choice(["Presencial", "Virtual"], n, p=[0.65, 0.35])

    promedio = np.clip(rng.normal(3.85, 0.42, n), 2.5, 5.0).round(2)
    experiencia = np.clip(rng.poisson(4, n) + rng.normal(0, 1, n), 0, 25).round(1)
    puntaje = np.clip(rng.normal(310, 45, n), 150, 450).round(0)
    ingresos = np.clip(rng.lognormal(14.6, 0.55, n), 1_000_000, None).round(-4)
    edad = np.clip(rng.normal(29, 5.5, n), 21, 55).round(0)

    # Probabilidad de admisión: depende del promedio, el puntaje y la experiencia.
    logit = (
        -8.0
        + 1.30 * promedio
        + 0.011 * puntaje
        + 0.09 * experiencia
        + rng.normal(0, 0.9, n)
    )
    admitido = (logit > 0).astype(int)

    # Solo se entrevista a una parte de los solicitantes (mecanismo MNAR).
    entrevistado = rng.random(n) < 0.35
    nota_entrevista = np.where(
        entrevistado, np.clip(rng.normal(3.9, 0.6, n), 1, 5).round(1), np.nan
    )

    fechas = pd.to_datetime("2025-09-01") + pd.to_timedelta(rng.integers(0, 120, n), unit="D")

    datos = pd.DataFrame(
        {
            "id_solicitud": [f"S{i:05d}" for i in range(1, n + 1)],
            "fecha_solicitud": fechas.strftime("%d/%m/%Y"),
            "programa": programa,
            "modalidad": modalidad,
            "edad": edad.astype(int),
            "estado_civil": rng.choice(["Soltero", "Casado", "Union libre"], n, p=[0.55, 0.3, 0.15]),
            "promedio_pregrado": promedio,
            "experiencia_anios": experiencia,
            "puntaje_examen": puntaje,
            "ingresos_hogar": ingresos,
            "nota_entrevista": nota_entrevista,
            "admitido": admitido,
        }
    )

    # ---------------------------------------------------------------- defectos plantados ---

    # 1. Inconsistencia de formato en una categórica.
    indices = rng.choice(n, size=int(0.18 * n), replace=False)
    variantes = {"Soltero": ["soltero", " SOLTERO", "Soltero "],
                 "Casado": ["casado", "CASADO "],
                 "Union libre": ["union libre", "Unión libre"]}
    for i in indices:
        opciones = variantes[datos.loc[i, "estado_civil"]]
        datos.loc[i, "estado_civil"] = opciones[rng.integers(len(opciones))]

    # 2. Faltante disfrazado como -999 en ingresos.
    datos.loc[rng.choice(n, size=int(0.09 * n), replace=False), "ingresos_hogar"] = -999

    # 3. Faltantes MAR en experiencia: faltan más en modalidad virtual.
    prob_falta = np.where(datos["modalidad"] == "Virtual", 0.30, 0.06)
    datos.loc[rng.random(n) < prob_falta, "experiencia_anios"] = np.nan

    # 4. Outliers por error de registro en edad.
    datos.loc[rng.choice(n, size=3, replace=False), "edad"] = 210
    datos.loc[rng.choice(n, size=2, replace=False), "edad"] = -5

    # 5. Ingresos legítimamente altos (no son errores).
    datos.loc[rng.choice(n, size=6, replace=False), "ingresos_hogar"] = (
        rng.uniform(45_000_000, 90_000_000, 6).round(-4)
    )

    # 6. Fuga de datos: el objetivo, escrito en texto.
    datos["admitido_texto"] = np.where(datos["admitido"] == 1, "Admitido", "No admitido")

    # 7. Columnas numéricas guardadas como texto con convenciones locales.
    datos["promedio_pregrado"] = datos["promedio_pregrado"].map(lambda v: f"{v:.2f}".replace(".", ","))
    puntaje_texto = datos["puntaje_examen"].map(lambda v: f"{v:.0f}")
    faltante_puntaje = rng.random(n) < 0.07
    puntaje_texto[faltante_puntaje] = rng.choice(["N/D", "-", ""], faltante_puntaje.sum())
    datos["puntaje_examen"] = puntaje_texto

    # 8. Duplicados REALES: filas repetidas con el mismo id.
    repetidas = datos.sample(12, random_state=semilla)
    datos = pd.concat([datos, repetidas], ignore_index=True)

    # 9. Duplicados APARENTES: distinto id, todo lo demás igual.
    aparentes = datos.sample(8, random_state=semilla + 1).copy()
    aparentes["id_solicitud"] = [f"S9{i:04d}" for i in range(1, len(aparentes) + 1)]
    datos = pd.concat([datos, aparentes], ignore_index=True)

    return datos.sample(frac=1, random_state=semilla).reset_index(drop=True)


if __name__ == "__main__":
    datos = generar()
    datos.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"Escrito: {SALIDA.name}  ({SALIDA.stat().st_size:,} bytes)")
    print(f"Filas: {len(datos)}  Columnas: {len(datos.columns)}")
    print(f"Tasa de admision: {datos['admitido'].mean():.1%}")
    print("\nTipos:")
    print(datos.dtypes.to_string())
    print("\nNulos declarados:")
    nulos = datos.isna().sum()
    print(nulos[nulos > 0].to_string())

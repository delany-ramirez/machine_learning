# Ejercicio 01 · Trazabilidad de los modelos de Adult Census

**Módulo 6 · Sesión 14** · Tiempo estimado: **60 min** · Con código

> **Objetivo.** Convertir la comparación de modelos que ya hiciste sobre Adult Census
> (ejercicios del módulo 4 y ejercicio 03 del módulo 5) en un experimento **trazable**:
> cada modelo como una corrida de MLflow con su contexto, sus métricas de calidad y sus
> métricas de despliegue; elegir producción con las dos cosas a la vista; y demostrar que
> una corrida se puede reproducir.

## Contexto

`adult-census.csv` (`python datos/descargar-adult-census.py` en el módulo 4 o 5 si no lo
tienes), misma partición 80/20 estratificada y CV de 5 pliegues (`random_state=42`).
Reutiliza `registrar` y `medir_tamano_y_latencia` de `01-mlflow-aplicado.ipynb`,
adaptadas. Tracking en `sqlite:///mlflow.db` en la carpeta donde trabajes; experimento
`adult-ingreso-alto`.

Entrega un notebook `ej01-<tu-apellido>.ipynb` y una captura de la interfaz web con las
corridas ordenadas por AP.

## Parte A — Cuatro corridas (25 min)

**A.1** Registra, con parámetros, contexto (hash del CSV, commit, versiones, semilla),
métricas de calidad (AP y AUC en CV, con error estándar) y métricas de despliegue
(tamaño serializado, latencia por fila, segundos de ajuste), estos cuatro candidatos:

- Regresión logística con `ColumnTransformer` (estandarizar + *one-hot*).
- Random Forest (300 árboles, `min_samples_leaf=5`) con *one-hot*.
- `HistGradientBoostingClassifier` con *one-hot* **denso** (`sparse_output=False` en el
  codificador; el HGB no acepta matrices dispersas).
- LightGBM con categóricas nativas (`dtype="category"`), registrado con el *flavor*
  `mlflow.lightgbm`.

**A.2** Registra como artefacto de cada corrida la curva precisión-recall y una tabla con
la AP por pliegue. Registra el modelo con firma y ejemplo de entrada. ¿Qué archivos
aparecen en la carpeta `modelo/` de la corrida? ¿Para qué sirve cada uno?

## Parte B — Comparar y elegir (15 min)

**B.1** `search_runs` ordenado por AP. Grafica AP contra tamaño (escala log) y AP contra
latencia.

**B.2** El mejor en AP y el que elegirías para una API que debe responder a 500 peticiones
por segundo en un contenedor pequeño: ¿son el mismo? Justifica con las tres métricas de
despliegue.

**B.3** Registra en el *Model Registry* el modelo `adult-ingreso-alto` con dos versiones y
los alias `campeon` y `produccion` (pueden coincidir; si coinciden, explica por qué aquí sí
y en Wine Quality no). Anota la razón como tag de cada versión.

## Parte C — Reproducir y romper (20 min)

**C.1** Toma la corrida de LightGBM. Lee de ella los hiperparámetros, la semilla y el hash
de los datos, reentrena, y comprueba que la AP en CV coincide hasta el sexto decimal.

**C.2** Ahora **rompe** la reproducibilidad a propósito: cambia una fila del CSV (por
ejemplo, la edad del primer registro), vuelve a calcular el hash, y repite C.1. ¿Qué
detecta el registro? ¿Cambió la AP? ¿Cuánto? ¿Habrías notado el cambio sin el hash?

**C.3** Carga el modelo `produccion` desde el registro y predice sobre el conjunto de
prueba. Reporta AP y AUC. Compara con el valor de CV registrado: ¿está dentro de lo
esperable?

## Entrega

Notebook, captura de la interfaz, y una tabla final de una fila por corrida con: nombre,
AP ± ee, tamaño, latencia, alias (si lo tiene) y razón.

# Ejercicio 01 · Clasificación, métricas y umbral sobre Adult Census

**Módulo 4 · Sesión 9** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Aplicar el marco de evaluación de `03-metricas-clasificacion.md` sobre un
> dataset más grande y más sucio que Wine Quality: 48 842 personas del censo de EE. UU. de
> 1994, con categóricas de alta cardinalidad, valores faltantes y un 24 % de positivos.
> Encuadrar el problema, construir una regresión logística en `Pipeline`, y decidir el
> umbral con costos explícitos — sin tocar el conjunto de prueba hasta el final.

## Contexto

El dataset **no está versionado** (pesa ~5 MB). Se genera una sola vez con:

```bash
python datos/descargar-adult-census.py
```

El objetivo es `ingreso_alto` (1 si la persona gana más de 50 000 USD al año). Variables:
`edad`, `tipo_empleo`, `fnlwgt` (peso muestral del censo), `educacion`, `anos_educacion`,
`estado_civil`, `ocupacion`, `relacion`, `raza`, `sexo`, `ganancia_capital`,
`perdida_capital`, `horas_semana`, `pais_origen` y `particion_original` (train/test del
archivo original de UCI; **no** se usa como variable).

```python
import numpy as np
import pandas as pd

datos = pd.read_csv("../datos/adult-census.csv")
datos = datos.drop(columns=["particion_original"])
```

Entrega un notebook `ej01-<tu-apellido>.ipynb` que corra de principio a fin. Los tres
ejercicios del módulo se encadenan sobre estos datos: guarda tu partición y tu
`crear_pipeline()`.

## Parte A — Encuadre y diagnóstico (15 min)

**A.1** Reporta la prevalencia del objetivo, las columnas con valores faltantes y su
porcentaje, y la cardinalidad de cada variable categórica.

**A.2** `educacion` y `anos_educacion` parecen decir lo mismo. Compruébalo (¿cuántos valores
distintos de `anos_educacion` hay por cada valor de `educacion`?) y decide cuál conservar.

**A.3** Hay filas completamente idénticas. ¿Cuántas? Con el criterio de
`02-clasificacion-aplicado.ipynb` (sección 2) y de `01-diagnostico-eda-aplicado.ipynb`
(módulo 2), argumenta si aquí conviene eliminarlas o no.

**A.4** `pais_origen` tiene 41 categorías. ¿Qué fracción de las filas es `United-States`?
¿Qué implica para el *one-hot* y cómo lo resuelve `OneHotEncoder(min_frequency=...)`?

## Parte B — Regresión logística en `Pipeline` (20 min)

**B.1** Haz una partición estratificada 80/20 con `random_state=42`. Construye una función
`crear_pipeline(clasificador, escalar=True)` con un `ColumnTransformer` que impute la mediana
y estandarice las numéricas, e impute la constante `"Desconocido"` y codifique *one-hot* (con
`handle_unknown="ignore"` y `min_frequency=50`) las categóricas. ¿Cuántas columnas quedan
tras la codificación?

**B.2** Con `StratifiedKFold(5, shuffle=True, random_state=42)`, reporta accuracy, precisión,
recall, F1, AUC-ROC y AP de la regresión logística (`max_iter=3000`). Compara la accuracy
con la de la referencia trivial.

**B.3** Con `cross_val_predict(..., method="predict_proba")`, construye la matriz de
confusión en el umbral 0.5. ¿Qué error domina?

## Parte C — Curvas y umbral (25 min)

**C.1** Dibuja las curvas ROC y precisión-recall con las probabilidades de CV. ¿Cuál es la
mayor precisión alcanzable con recall $\geq 0.8$?

**C.2** Recorre el umbral de 0.05 a 0.95 y grafica precisión, recall y F1. ¿En qué umbral se
maximiza F1 y cuánto vale?

**C.3** Supón que el modelo se usa para seleccionar a quién ofrecer un producto financiero:
un falso positivo cuesta 1 (una oferta desperdiciada) y un falso negativo cuesta 5 (un
cliente valioso perdido). Encuentra el umbral de mínimo costo y compara el costo con el del
umbral 0.5.

## Parte D — Pesos de clase (15 min)

**D.1** Repite B.2 y C.2 con `class_weight="balanced"`. Reporta AUC-ROC, AP, recall y F1 en
0.5, y el mejor F1 alcanzable moviendo el umbral.

**D.2** ¿Qué cambió y qué no? Concluye, con tus números, si en este problema balancear las
clases aporta algo que mover el umbral no aporte.

# Solución · Ejercicio 02 · Bosques y boosting sobre Adult Census

> **Material del docente.** Números obtenidos con la partición y la CV del ejercicio 01
> (`random_state=42`). Los tiempos son orientativos (dependen de la máquina); las AP no.

## Parte A — Cuatro ensambles con valores por defecto

**A.1**

| Modelo | AP | AUC-ROC | Ajuste por pliegue |
|---|---|---|---|
| Random Forest (300) | 0.775 | 0.906 | 2.5 s |
| Extra-Trees (300) | 0.712 | 0.887 | 3.6 s |
| LightGBM (por defecto) | **0.828** | **0.928** | 0.2 s |
| LightGBM (1000, $\nu = 0.03$) | 0.826 | 0.927 | 0.7 s |

Para referencia, la logística del ejercicio 01: AP 0.766, AUC 0.906.

**A.2** El orden se **invierte** respecto a Wine Quality. Allí, Extra-Trees > Random Forest >
boosting por defecto (0.589 > 0.570 > 0.543); aquí, boosting por defecto > Random Forest >
Extra-Trees (0.828 > 0.775 > 0.712), y Random Forest apenas supera a la logística. Además,
LightGBM es diez veces más rápido.

La explicación que da `05-boosting.md`: boosting tiende a imponerse con **más datos** (39 000
filas frente a 4 000: hay margen para muchas rondas de corrección sin sobreajustar) y con
**variables heterogéneas** (categóricas de alta cardinalidad, numéricas con distribuciones
muy sesgadas como `ganancia_capital`, interacciones fuertes como `relacion × edad`). Los
bosques promedian árboles que, sobre 74 columnas *one-hot* dispersas, son individualmente
malos; Extra-Trees, que además elige umbrales al azar, sufre más todavía. Ningún modelo
gana en todos los datasets — es la lección de `06-boosting-aplicado.ipynb`, ahora en la
dirección contraria.

## Parte B — Random Forest: hojas mínimas

**B.1**

| `min_samples_leaf` | AP | AUC-ROC |
|---|---|---|
| 1 | 0.775 | 0.906 |
| 5 | **0.803** | **0.918** |
| 20 | 0.793 | 0.914 |

**B.2** No se sostiene: aquí los árboles completamente desarrollados son la **peor** opción, y
exigir 5 filas por hoja sube la AP casi tres puntos. Con 39 000 filas y 74 columnas
dispersas, un árbol sin límite tiene profundidad suficiente para aislar personas individuales
—memoriza combinaciones de categorías raras—, y el promedio de 300 árboles no basta para
cancelar todo ese ruido. En Wine Quality, con 12 variables continuas y 4 000 filas, las hojas
de tamaño 1 capturaban estructura real. `min_samples_leaf` es un hiperparámetro que se afina,
como `max_features`: la regla "árboles sin podar en un bosque" es un buen punto de partida,
no una ley.

## Parte C — LightGBM: categóricas nativas y early stopping

**C.1** Con categóricas nativas: AP **0.826**, AUC 0.927, ajuste 0.6 s — la misma AP que con
*one-hot* (0.826) y un tiempo comparable. En este dataset las dos codificaciones son
equivalentes en calidad; la ventaja de la nativa es de higiene (no hay que decidir
`min_frequency` ni construir el `ColumnTransformer`) y crece con la cardinalidad. Conviene
advertir que las categorías del conjunto de prueba deben fijarse a las del entrenamiento
(`pd.Categorical(..., categories=...)`), o LightGBM las codificará con enteros distintos.

**C.2** `best_iteration_` = **335** con $\nu = 0.03$; la AP de validación en ese pliegue es
0.832. La curva es plana alrededor del máximo —la firma de una tasa de aprendizaje baja—
y el early stopping se detuvo en la ronda 535 (200 después del máximo).

**C.3** Comparación pareada sobre 10 pliegues (5 × 2):

| | AP |
|---|---|
| LightGBM (335 rondas, $\nu = 0.03$) | 0.829 |
| Random Forest (`min_samples_leaf=5`) | 0.803 |
| **Diferencia** | **+0.026 ± 0.0007** (cociente 39) |

Detectable sin ninguna duda, y relevante: un 3 % relativo de AP con un error estándar
diminuto (con 39 000 filas, los pliegues son mucho más parecidos entre sí que en Wine
Quality, donde el error estándar era de 0.003–0.015). Contra el Random Forest sin afinar
(`min_samples_leaf=1`), la diferencia es de +0.051.

## Parte D — Conjunto de prueba

**D.1** Umbral de mínimo costo para LightGBM (probabilidades de CV, FN = 5 × FP): **0.15**.
Sobre el conjunto de prueba (9 769 personas):

| Métrica | LightGBM |
|---|---|
| AUC-ROC | 0.931 |
| AP | 0.835 |
| Precisión | 0.545 |
| Recall | 0.923 |
| F1 | 0.685 |
| Costo | 2 705 |

**D.2** La logística del ejercicio 01, sobre el mismo conjunto de prueba y con su propio
umbral óptimo (también 0.15): AP 0.766, F1 0.644, costo **3 151**. LightGBM ahorra un 14 %
del costo total con la misma estructura de costos — en este problema, la elección del modelo
sí mueve la decisión de negocio, a diferencia de Wine Quality, donde el ensamble mejoraba el
costo un 4 % en CV. Ambas conclusiones salen de medir, no de la fama de los algoritmos.

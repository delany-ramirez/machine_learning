# Módulo 3 — Supervisado I: regresión y evaluación (S6–S8, 10.5 h)

> Estado: **completo** (Fase 3 de [`../PLAN.md`](../PLAN.md)).

## Objetivos

Al finalizar el módulo, el estudiante será capaz de formular, ajustar y diagnosticar modelos
de regresión —incluyendo su optimización por descenso del gradiente y su regularización— y de
evaluar cualquier modelo de forma honesta mediante validación cruzada y búsqueda sistemática
de hiperparámetros.

## Contenidos

### ✅ Núcleo

- **S6** — Regresión lineal simple y múltiple. Mínimos cuadrados ordinarios.
- **S6** — Descenso del gradiente: función de costo, tasa de aprendizaje, convergencia.
- **S6** — Supuestos del modelo lineal y análisis de residuales. Métricas: MSE, RMSE, MAE,
  $R^2$ y $R^2$ ajustado.
- **S7** — Multicolinealidad: diagnóstico con matriz de correlación y **VIF**.
- **S7** — Regresión polinómica. Regularización Ridge ($L_2$), Lasso ($L_1$) y Elastic Net.
- **S8** — Compromiso **sesgo-varianza**. Sobreajuste y subajuste.
- **S8** — Validación cruzada: k-fold, estratificada y temporal. Curvas de aprendizaje y de
  validación.
- **S8** — Búsqueda de hiperparámetros: grid, aleatoria y bayesiana (Optuna).
  Reproducibilidad y semillas.

### 🔵 Opcional

- Regresión robusta y tratamiento de outliers influyentes.
- Comparación `scikit-learn` vs. `statsmodels`: predicción vs. inferencia.
- Métricas alternativas: MAPE, error cuadrático logarítmico.

## Materiales

### Teoría

| # | Documento | Sesión | Tema |
|---|---|---|---|
| 01 | [`teoria/01-regresion-lineal.md`](teoria/01-regresion-lineal.md) | S6 | Formulación, OLS, supuestos, residuales, métricas |
| 02 | [`teoria/02-descenso-gradiente.md`](teoria/02-descenso-gradiente.md) | S6 | Función de costo, gradiente, tasa de aprendizaje, variantes |
| 03 | [`teoria/03-multicolinealidad-polinomica.md`](teoria/03-multicolinealidad-polinomica.md) | S7 | VIF, diagnóstico, regresión polinómica |
| 04 | [`teoria/04-regularizacion.md`](teoria/04-regularizacion.md) | S7 | Ridge, Lasso, Elastic Net; geometría e interpretación |
| 05 | [`teoria/05-sesgo-varianza-validacion.md`](teoria/05-sesgo-varianza-validacion.md) | S8 | Descomposición del error, k-fold repetido, comparación pareada |
| 06 | [`teoria/06-seleccion-hiperparametros.md`](teoria/06-seleccion-hiperparametros.md) | S8 | Grid, random, optimización bayesiana; CV anidada |

### Notebooks

| # | Notebook | Tipo | Contenido |
|---|---|---|---|
| 01 | [`notebooks/01-descenso-gradiente-intuicion.ipynb`](notebooks/01-descenso-gradiente-intuicion.ipynb) | intuición | Extiende el descenso a gradiente manual del módulo 1 a regresión múltiple vectorizada; batch/mini-batch/SGD; divergencia sin escalar |
| 02 | [`notebooks/02-regresion-multiple-aplicado.ipynb`](notebooks/02-regresion-multiple-aplicado.ipynb) | aplicado | `Pipeline` sobre Ames Housing; métricas; residuales en embudo; RMSE vs. MAE al modelar en log(precio) |
| 03 | [`notebooks/03-regularizacion-intuicion.ipynb`](notebooks/03-regularizacion-intuicion.ipynb) | intuición | Ridge y Lasso a mano (descenso con penalización $L_2$; descenso por coordenadas para $L_1$); inestabilidad de OLS por colinealidad, medida con bootstrap |
| 04 | [`notebooks/04-regularizacion-aplicado.ipynb`](notebooks/04-regularizacion-aplicado.ipynb) | aplicado | VIF sobre Ames Housing, términos polinómicos y su costo en colinealidad, Ridge/Lasso con `scikit-learn` |
| 05 | [`notebooks/05-sesgo-varianza-intuicion.ipynb`](notebooks/05-sesgo-varianza-intuicion.ipynb) | intuición | Regresión polinómica sobre función verdadera conocida; k-fold a mano con barras de error; por qué barras solapadas no son una comparación pareada; curvas de aprendizaje |
| 06 | [`notebooks/06-seleccion-modelos-aplicado.ipynb`](notebooks/06-seleccion-modelos-aplicado.ipynb) | aplicado | Grid/random/Optuna sobre Ames Housing, CV anidada, comparación pareada Ridge vs. Lasso con y sin fuga de selección, y el RMSE final sobre el conjunto de prueba |

> **Hallazgo del notebook 02.** Modelar $\log(1+\text{precio})$ en vez del precio directo baja
> el MAE y el MAPE en los cuatro cuartiles de precio, pero **sube** el RMSE: una sola vivienda
> atípica (grande, de calidad máxima, vendida muy por debajo de lo esperado) produce un error
> de más de 700 mil dólares al revertir la transformación logarítmica. RMSE y MAE discrepan
> sobre cuál modelo es mejor — la métrica que se elige es una decisión, no un trámite.
>
> **Hallazgo del notebook 04.** Agregar `gr_liv_area²` y `overall_qual²` dispara el VIF de esas
> variables a ≈ 50 y produce coeficientes gigantes de signo opuesto — pero el RMSE de
> validación **no mejora** con más regularización: con $n=2930$ frente a $p\approx 24$, la
> multicolinealidad aquí daña la interpretación, no la predicción, tal como anticipa
> `03-multicolinealidad-polinomica.md`. Ridge y Lasso sí estabilizan el par colineal, a ritmos
> muy distintos entre sí.
>
> **Hallazgo del notebook 06.** Comparando Ridge y Lasso —cada uno afinado por CV— sobre los
> **mismos** 10 pliegues, la conclusión **depende de cómo se haya elegido $\lambda$**. Si se
> elige una sola vez con todo el entrenamiento y después se evalúa sobre pliegues de ese mismo
> entrenamiento —la fuga que el propio notebook mide en la sección 4—, la diferencia es −\$10
> con un error estándar de \$35: "no hay diferencia detectable". Si cada pliegue elige su
> $\lambda$ con datos que no lo incluyen, la diferencia es −\$41 con ee \$17, apenas por encima
> de la regla de dos errores estándar. La higiene metodológica no solo corrige un número: aquí
> cambia la respuesta. Y aun así, \$41 sobre un RMSE de \$33,460 es un 0.12 % —
> **detectable no es lo mismo que relevante**.

### Datos

**Dataset conductor del módulo:** `ames-housing.csv`

| Archivo | Descripción | Por qué este |
|---|---|---|
| [`datos/ames-housing.csv`](datos/ames-housing.csv) | 2930 viviendas vendidas en Ames, Iowa (2006–2010), 80 variables tras limpiar columnas identificadoras. Dominio público (De Cock, 2011), vía [wblakecannon/ames](https://github.com/wblakecannon/ames) | Dataset real de tamaño moderado, con variables numéricas y categóricas, ideal para regresión múltiple, regularización y selección de modelos |
| [`datos/preparar-ames-housing.py`](datos/preparar-ames-housing.py) | Descarga desde la fuente y normaliza encabezados a `snake_case` | Documenta la procedencia exacta; idempotente |
| [`datos/rendimiento-estudiantes.csv`](datos/rendimiento-estudiantes.csv) | Mismo dataset sintético del módulo 1 (400 estudiantes) | El notebook 01 extiende exactamente el ajuste por descenso del gradiente que el módulo 1 hizo con una sola variable, ahora con seis |
| [`datos/generar-rendimiento-estudiantes.py`](datos/generar-rendimiento-estudiantes.py) | Generador con semilla fija (copiado del módulo 1) | Reproducible byte a byte |

### Ejercicios

| # | Enunciado | Solución | Duración |
|---|---|---|---|
| 01 | [`ejercicios/ej01-residuales.md`](ejercicios/ej01-residuales.md) | [`ej01-residuales-sol.md`](ejercicios/ej01-residuales-sol.md) | 75 min |
| 02 | [`ejercicios/ej02-regularizacion.md`](ejercicios/ej02-regularizacion.md) | [`ej02-regularizacion-sol.md`](ejercicios/ej02-regularizacion-sol.md) | 75 min |
| 03 | [`ejercicios/ej03-validacion-cruzada.md`](ejercicios/ej03-validacion-cruzada.md) | [`ej03-validacion-cruzada-sol.md`](ejercicios/ej03-validacion-cruzada-sol.md) | 75 min |

Los tres ejercicios comparten un mismo subconjunto de variables de Ames Housing —distinto al
de los notebooks— y se encadenan: el 01 descubre que `full_bath`/`half_bath` tienen
coeficientes de signo contraintuitivo a pesar de un VIF bajo; el 02 mide ese VIF, prueba
Ridge/Lasso/Elastic Net y muestra que corregir el signo exige mucho más $\lambda$ del que
conviene para predecir; el 03 cierra con CV formal y una comparación pareada que encuentra una
diferencia **que además importa**: `foundation` aporta \$961 de RMSE con un ee de \$211
(cociente 4.6), frente a los \$41 apenas detectables —y prácticamente irrelevantes— que el
notebook 06 mide entre Ridge y Lasso.

### Quiz

| Archivo | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-3.md`](quiz/quiz-modulo-3.md) | [`quiz-modulo-3-sol.md`](quiz/quiz-modulo-3-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E3 — Línea base.** Primer modelo del caso con validación cruzada honesta y métricas
justificadas, que servirá de referencia para todo lo que venga después. Ver
[`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

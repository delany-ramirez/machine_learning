# Módulo 3 — Supervisado I: regresión y evaluación (S6–S8, 10.5 h)

> Estado: **contenido pendiente** (Fase 3 de [`../PLAN.md`](../PLAN.md)). Este README es el
> índice planeado; los archivos se irán creando en esa fase.

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

| # | Documento | Sesión | Tema | Estado |
|---|---|---|---|---|
| 01 | `teoria/01-regresion-lineal.md` | S6 | Formulación, OLS, supuestos, residuales, métricas | ⬜ |
| 02 | `teoria/02-descenso-gradiente.md` | S6 | Función de costo, gradiente, tasa de aprendizaje, variantes | ⬜ |
| 03 | `teoria/03-multicolinealidad-polinomica.md` | S7 | VIF, diagnóstico, regresión polinómica | ⬜ |
| 04 | `teoria/04-regularizacion.md` | S7 | Ridge, Lasso, Elastic Net; geometría e interpretación | ⬜ |
| 05 | `teoria/05-sesgo-varianza-validacion.md` | S8 | Descomposición del error, CV, curvas de aprendizaje | ⬜ |
| 06 | `teoria/06-seleccion-hiperparametros.md` | S8 | Grid, random, optimización bayesiana; CV anidada | ⬜ |

### Notebooks

| # | Notebook | Tipo | Contenido | Estado |
|---|---|---|---|---|
| 01 | `notebooks/01-descenso-gradiente-intuicion.ipynb` | intuición | Descenso del gradiente implementado a mano y comparado con OLS | ⬜ |
| 02 | `notebooks/02-regresion-multiple-aplicado.ipynb` | aplicado | Regresión múltiple con dataset real; residuales y métricas | ⬜ |
| 03 | `notebooks/03-regularizacion-intuicion.ipynb` | intuición | Efecto de $\lambda$ en Ridge y Lasso; trayectoria de coeficientes | ⬜ |
| 04 | `notebooks/04-regularizacion-aplicado.ipynb` | aplicado | VIF, polinómica y comparación Ridge/Lasso/Elastic Net | ⬜ |
| 05 | `notebooks/05-sesgo-varianza-intuicion.ipynb` | intuición | Curvas de aprendizaje y validación sobre un problema controlado | ⬜ |
| 06 | `notebooks/06-seleccion-modelos-aplicado.ipynb` | aplicado | CV, grid/random search y Optuna sobre el dataset del módulo | ⬜ |

### Datos

| Archivo | Descripción | Variables | Estado |
|---|---|---|---|
| — | Dataset conductor del módulo, pendiente de elegir (candidato heredado: Ames Housing) | — | ⬜ |

### Ejercicios

| # | Enunciado | Solución | Estado |
|---|---|---|---|
| 01 | `ejercicios/ej01-residuales.md` | `ej01-residuales-sol.md` | ⬜ |
| 02 | `ejercicios/ej02-regularizacion.md` | `ej02-regularizacion-sol.md` | ⬜ |
| 03 | `ejercicios/ej03-validacion-cruzada.md` | `ej03-validacion-cruzada-sol.md` | ⬜ |

### Quiz

| Archivo | Clave | Estado |
|---|---|---|
| `quiz/quiz-modulo-3.md` | `quiz/quiz-modulo-3-sol.md` | ⬜ |

## Entrega del proyecto integrador

**E3 — Línea base.** Primer modelo del caso con validación cruzada honesta y métricas
justificadas, que servirá de referencia para todo lo que venga después. Ver
[`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../environment.yml`](../environment.yml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

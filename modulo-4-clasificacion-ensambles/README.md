# Módulo 4 — Supervisado II: clasificación y ensambles (S9–S11, 10.5 h)

> Estado: **completo** (Fase 4 de [`../PLAN.md`](../PLAN.md)).

## Objetivos

Al finalizar el módulo, el estudiante será capaz de construir y evaluar clasificadores
eligiendo la métrica adecuada al costo de cada tipo de error, manejar el desbalance de
clases, combinar modelos mediante bagging y boosting, y explicar las predicciones de un
modelo de caja negra — sabiendo dónde se equivoca cada herramienta de explicación.

## Contenidos

### ✅ Núcleo

- **S9** — Regresión logística: odds, log-odds, máxima verosimilitud y softmax multiclase.
  Separación perfecta y por qué se regulariza por defecto.
- **S9** — K-Nearest Neighbors. Máquinas de vectores de soporte (SVM), margen y kernels.
- **S9** — Métricas: matriz de confusión, accuracy, precisión, recall, F1, ROC-AUC y curva
  precisión-recall. Ajuste del umbral de decisión con costos.
- **S9** — Clases desbalanceadas: umbral, pesos de clase y SMOTE, **medidos**.
- **S10** — Árboles de decisión: impureza (Gini, entropía), partición voraz, profundidad,
  poda por costo-complejidad, sobreajuste.
- **S10** — Bagging, error *out-of-bag*, **Random Forest** y Extra-Trees. Cuándo
  decorrelacionar ayuda y cuándo no.
- **S11** — AdaBoost, gradient boosting, early stopping, **XGBoost** y **LightGBM**. Stacking.
- **S11** — Interpretabilidad: importancia por impureza, por permutación y **SHAP**;
  dependencia parcial e ICE; qué no es una explicación.

### 🔵 Opcional

- Naive Bayes y su relación con el teorema de Bayes visto en S3.
- Calibración de probabilidades (Platt, isotónica) — mencionada en `02-knn-y-svm.md`.
- Análisis de errores por segmento y sesgos del modelo — el ejercicio 03 lo hace sobre
  `sexo` en Adult Census.

## Materiales

### Teoría

| # | Documento | Sesión | Tema |
|---|---|---|---|
| 01 | [`teoria/01-regresion-logistica.md`](teoria/01-regresion-logistica.md) | S9 | Sigmoide y logit, razón de momios, entropía cruzada, softmax, separación perfecta |
| 02 | [`teoria/02-knn-y-svm.md`](teoria/02-knn-y-svm.md) | S9 | KNN y su $k$; margen, vectores de soporte, $C$, truco del kernel |
| 03 | [`teoria/03-metricas-clasificacion.md`](teoria/03-metricas-clasificacion.md) | S9 | Matriz de confusión, ROC vs. PR, umbral con costos, desbalance, multiclase |
| 04 | [`teoria/04-arboles-y-bagging.md`](teoria/04-arboles-y-bagging.md) | S10 | Impureza, partición voraz, poda, inestabilidad, bagging, OOB, Random Forest, MDI |
| 05 | [`teoria/05-boosting.md`](teoria/05-boosting.md) | S11 | AdaBoost, gradient boosting, early stopping, XGBoost/LightGBM, stacking |
| 06 | [`teoria/06-interpretabilidad.md`](teoria/06-interpretabilidad.md) | S11 | MDI, permutación, valores de Shapley y SHAP, PDP/ICE, correlación vs. causalidad |

### Notebooks

| # | Notebook | Sesión | Tipo | Contenido |
|---|---|---|---|---|
| 01 | [`notebooks/01-logistica-intuicion.ipynb`](notebooks/01-logistica-intuicion.ipynb) | S9 | intuición | Extiende el descenso del gradiente del módulo 3 a clasificación: sigmoide, entropía cruzada, mismo gradiente; validado contra `scikit-learn`; softmax; separación perfecta |
| 02 | [`notebooks/02-clasificacion-aplicado.ipynb`](notebooks/02-clasificacion-aplicado.ipynb) | S9 | aplicado | Wine Quality: duplicados como fuga, logística/KNN/SVM, matriz de confusión, ROC vs. PR, umbral con costos, pesos vs. SMOTE, softmax sobre 7 clases, conjunto de prueba |
| 03 | [`notebooks/03-arboles-intuicion.ipynb`](notebooks/03-arboles-intuicion.ipynb) | S10 | intuición | Árbol recursivo a mano (coincide con `DecisionTreeClassifier`), profundidad y poda, inestabilidad por bootstrap, bagging a mano con medición de varianza, cuándo Random Forest no gana |
| 04 | [`notebooks/04-arboles-bagging-aplicado.ipynb`](notebooks/04-arboles-bagging-aplicado.ipynb) | S10 | aplicado | Wine Quality: árbol vs. logística, curva de $B$ y OOB, rejilla de `max_features`, Extra-Trees, comparación pareada, conjunto de prueba |
| 05 | [`notebooks/05-boosting-intuicion.ipynb`](notebooks/05-boosting-intuicion.ipynb) | S11 | intuición | AdaBoost y gradient boosting a mano (validados); boosting sobreajusta con las rondas; tasa de aprendizaje; el residual $y-\hat p$; tiempos exacto vs. histogramas |
| 06 | [`notebooks/06-boosting-aplicado.ipynb`](notebooks/06-boosting-aplicado.ipynb) | S11 | aplicado | Wine Quality: boosting por defecto vs. bosques, early stopping, Optuna sobre LightGBM, `scale_pos_weight`, stacking, conjunto de prueba |
| 07 | [`notebooks/07-interpretabilidad-aplicado.ipynb`](notebooks/07-interpretabilidad-aplicado.ipynb) | S11 | aplicado | Tres importancias y sus fallos medidos (ruido plantado, copia de `alcohol`), SHAP global/dependencia/local, PDP e ICE |

> **Hallazgo del notebook 02.** Wine Quality trae 1177 filas idénticas. Con ellas dentro,
> KNN con $k=1$ obtiene un F1 de 0.66 —muy por encima de la logística y la SVM—; sin ellas,
> 0.47. El 30 % de las filas de prueba tenía un gemelo exacto en entrenamiento: la fuga no
> inflaba un número, **elegía al modelo equivocado**. Y sobre el desbalance: pesos de clase y
> SMOTE suben el recall en 0.5 pero no mueven AUC, AP ni el mejor F1 alcanzable — en un
> modelo lineal, balancear es mover el umbral con otro nombre.
>
> **Hallazgo de los notebooks 03 y 04.** Random Forest **no** siempre gana a bagging: con 2
> variables informativas de 20, el 63 % de los nodos no ve ninguna variable útil y el bosque
> es peor que bagging. Sobre Wine Quality, con 12 variables con señal, ocurre lo contrario:
> `max_features=12` (bagging) es la peor fila de la rejilla, `max_features=1` la mejor, y la
> comparación pareada da RF − bagging = 0.016 ± 0.003 de AP. `max_features` se afina.
>
> **Hallazgo del notebook 06.** Con valores por defecto, ningún boosting alcanza a Random
> Forest en Wine Quality (AP 0.54 frente a 0.57), y Extra-Trees sin afinar (0.59) sigue por
> encima de LightGBM tras 40 trials de Optuna (0.57; diferencia 0.022 ± 0.004). El stacking
> gana 0.006 ± 0.003: detectable, no relevante. Los ejercicios muestran el caso contrario
> sobre Adult Census, donde LightGBM saca 0.026 ± 0.001 a un Random Forest afinado.
>
> **Hallazgo del notebook 07.** Una columna de ruido gaussiano queda, por importancia de
> impureza, por encima de cuatro variables reales y 6× por encima de una columna de ruido
> binario. La permutación lo corrige, pero reparte mal entre variables casi redundantes: una
> copia de `alcohol` baja su importancia de 0.104 a 0.017. Y `tipo` (tinto/blanco) vale cero
> en todas las medidas porque la química ya lo dice — importancia cero no es irrelevancia.

### Datos

**Dataset conductor del módulo:** `wine-quality.csv` · **Dataset de los ejercicios:**
`adult-census.csv`

| Archivo | Descripción | Por qué este |
|---|---|---|
| [`datos/wine-quality.csv`](datos/wine-quality.csv) | 6497 vinos portugueses (1599 tintos, 4898 blancos), 11 medidas fisicoquímicas, `tipo` y `quality` (3–9). Cortez et al. (2009), UCI, CC BY 4.0 | Problema binario desbalanceado (`quality ≥ 7`, 19.7 %), multiclase ordinal para softmax, todo numérico (el módulo 2 ya cubrió el preprocesamiento), y 1177 duplicados que sirven para enseñar la fuga por gemelos |
| [`datos/preparar-wine-quality.py`](datos/preparar-wine-quality.py) | Descarga los dos CSV de UCI, los une con la columna `tipo` y normaliza encabezados | Idempotente; documenta la procedencia |
| `datos/adult-census.csv` (**no versionado**, ~5 MB) | 48 842 personas del censo de EE. UU. de 1994, 14 variables, objetivo `ingreso_alto` (23.9 %). Kohavi y Becker (1996), UCI, CC BY 4.0 | Caso más retador para los ejercicios: categóricas de alta cardinalidad, nulos, variables sesgadas, proxies de variables sensibles; y el orden entre bosques y boosting se invierte respecto a Wine Quality |
| [`datos/descargar-adult-census.py`](datos/descargar-adult-census.py) | Descarga `adult.data` + `adult.test`, une, nombra columnas, convierte `?` en nulo, crea `ingreso_alto` | Se ejecuta una vez: `python datos/descargar-adult-census.py` |
| [`datos/rendimiento-estudiantes.csv`](datos/rendimiento-estudiantes.csv) | Mismo dataset sintético de los módulos 1 y 3 (400 estudiantes) | El notebook 01 extiende a `aprobo` el descenso del gradiente que el módulo 3 hizo sobre `nota_final`, con los mismos seis predictores |
| [`datos/generar-rendimiento-estudiantes.py`](datos/generar-rendimiento-estudiantes.py) | Generador con semilla fija (copiado del módulo 1) | Reproducible byte a byte |

### Ejercicios

| # | Enunciado | Solución | Sesión | Duración |
|---|---|---|---|---|
| 01 | [`ejercicios/ej01-metricas-umbral.md`](ejercicios/ej01-metricas-umbral.md) | [`ej01-metricas-umbral-sol.md`](ejercicios/ej01-metricas-umbral-sol.md) | S9 | 75 min |
| 02 | [`ejercicios/ej02-ensambles.md`](ejercicios/ej02-ensambles.md) | [`ej02-ensambles-sol.md`](ejercicios/ej02-ensambles-sol.md) | S10–S11 | 75 min |
| 03 | [`ejercicios/ej03-interpretabilidad.md`](ejercicios/ej03-interpretabilidad.md) | [`ej03-interpretabilidad-sol.md`](ejercicios/ej03-interpretabilidad-sol.md) | S11 | 75 min |

Los tres ejercicios se encadenan sobre **Adult Census**: el 01 encuadra el problema
(redundancia `educacion`/`anos_educacion`, 41 países, duplicados que sí se conservan) y
construye la logística con umbral por costos; el 02 descubre que el orden de los ensambles
se **invierte** respecto a Wine Quality —LightGBM por defecto gana con AP 0.83 frente a 0.78
de Random Forest, y `min_samples_leaf=1` deja de ser la mejor opción—; el 03 encuentra los
sesgos de las importancias en datos reales sin plantar nada (`fnlwgt`, el peso muestral, es
la segunda variable por número de particiones y nada por permutación; `relacion` es
`sexo × estado_civil`), y cierra midiendo qué hace el modelo con `sexo` y por qué quitar la
columna no quita la información.

### Quiz

| Archivo | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-4.md`](quiz/quiz-modulo-4.md) | [`quiz-modulo-4-sol.md`](quiz/quiz-modulo-4-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E4 — Modelos avanzados.** Ensambles ajustados sobre el caso, comparados contra la línea
base de E3 con comparación pareada sobre los mismos pliegues, umbral elegido con costos
explícitos, e interpretación de las variables que más pesan — incluida la pregunta de si
alguna de ellas es una fuga o un proxy de una variable sensible. Ver
[`../proyecto-integrador/`](../proyecto-integrador/).

---

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

# PLAN — Bitácora de construcción del curso

Este archivo es la **memoria del proyecto entre sesiones de trabajo**. Al retomar el trabajo,
léelo primero: dice qué está hecho, qué sigue y qué decisiones ya se tomaron.

**Última actualización:** 2026-09-11 · **Fase actual:** 4 completada, sigue la Fase 5.

---

## 1. Qué estamos construyendo

Refactorización completa del curso de Machine Learning de la Maestría en Ingeniería de
Sistemas y Computación. La edición anterior existía solo como 12 PDFs de diapositivas y 42
notebooks sueltos (guardados en `contenido_anterior/`, fuera de git). Se reconstruye como un
repositorio versionable con teoría en texto, notebooks curados, ejercicios y evaluación.

### Decisiones tomadas (no volver a discutirlas sin motivo)

| Decisión | Valor |
|---|---|
| Carga | 48 h ≈ 14 sesiones de 3.5 h (2 por semana, 7 semanas) |
| Alcance | ML clásico + **1 sesión** de deep learning + MLOps |
| Por qué solo 1 de DL | Los estudiantes tienen después un curso completo de Deep Learning |
| Stack | Solo Python (no hay versión en R, a diferencia del curso `doe`) |
| Organización | Por **módulo temático** (6 módulos), no por semana |
| Slides | No por ahora — fase 10, opcional |
| Evaluación | Proyecto integrador transversal + quiz teórico por módulo |
| Material previo | Insumo de referencia, **no plantilla**: se reescribe todo |
| Entorno conda | Se llama `ml-curso`, **no** `ml`: ya existe un entorno `ML` en la máquina del docente y en Windows los nombres no distinguen mayúsculas |

### Problemas de la edición anterior que este refactor corrige

1. **Duplicación**: 7 notebooks para clasificación 1, 5 para PCA/t-SNE, 4 para regresión
   lineal, 5 para regresión avanzada. Se consolidan a ~20 notebooks curados.
2. **Numeración contradictoria**: en los PDFs S10 = ensambles y S11 = clustering; en los
   notebooks al revés. Ahora `docs/programa.md` es la fuente única de verdad.
3. **Vacíos**: no había deep learning, ni sesión dedicada a evaluación/validación y fuga de
   datos; boosting moderno apenas mencionado; MLOps reducido a una sesión final.
4. **Sin teoría en texto**: el contenido conceptual vivía solo en diapositivas.
5. **Rúbricas dispersas** dentro de notebooks; ahora hay una única en el proyecto integrador.

---

## 2. Estado de las fases

| Fase | Contenido | Estado | Commit |
|---|---|---|---|
| 0 | Estructura del repo, README, docs (programa, convenciones, entorno), entorno, licencia, READMEs índice de los 6 módulos | ✅ hecha | `b0059bd` |
| 1 | **Módulo 1** — Fundamentos y ciclo de vida (S1–S3) | ✅ hecha | `ac80bf0` |
| 2 | **Módulo 2** — Datos y características (S4–S5) | ✅ hecha | |
| 3 | **Módulo 3** — Regresión y evaluación (S6–S8) | ✅ hecha | `887ac33` (S6) · `0933873` (S7) |
| 4 | **Módulo 4** — Clasificación y ensambles (S9–S11) | ✅ hecha | `3466c40` (S9) · `a33831d` (S10) · `49fa45c` (S11) |
| 5 | **Módulo 5** — No supervisado y deep learning (S12–S13) | ⬜ pendiente | |
| 6 | **Módulo 6** — MLOps y despliegue (S14) | ⬜ pendiente | |
| 7 | **Proyecto integrador** — enunciado, datos, rúbrica, entregas | ⬜ pendiente | |
| 8 | **Recursos generales** — bibliografía, enlaces, glosario, cheatsheets, plantillas | ⬜ pendiente | |
| 9 | **QA global** — ejecutar todos los notebooks, verificar enlaces y coherencia | ⬜ pendiente | |
| 10 | *(opcional)* Slides Slidev por módulo | ⬜ no planificada | |

Cada fase cierra con un commit en español (`Fase N: ...`) que incluye la actualización de este
archivo.

---

## 3. Detalle de lo hecho

### ✅ Fase 0 — Estructura base

- `git init` del repositorio.
- Esqueleto de carpetas: 6 módulos con `teoria/`, `notebooks/`, `datos/`, `ejercicios/`,
  `quiz/`; más `docs/`, `proyecto-integrador/`, `recursos/`.
- `README.md` de portada con programa, estructura y puesta en marcha.
- `docs/programa.md` — malla de 14 sesiones, **fuente de verdad** del curso.
- `docs/convenciones.md` — estilo `.md`/LaTeX, reglas de notebooks, nombres, commits.
- `docs/guia-entorno.md` — instalación, verificación y problemas frecuentes.
- `environment.yml` (conda, entorno `ml-curso`) y `requirements.txt` (pip).
- `.gitignore` (excluye `contenido_anterior/`, `mlruns/`, datos pesados) y `LICENSE`
  (CC BY 4.0 + MIT).
- README índice de cada uno de los 6 módulos.

### ✅ Fase 1 — Módulo 1: Fundamentos y ciclo de vida

**Dataset conductor elegido:** `rendimiento-estudiantes.csv` — 400 estudiantes ficticios,
**sintético con semilla fija** y script generador versionado. Se eligió simulado para poder
comparar los coeficientes estimados contra los reales del proceso generador (imposible con
datos reales), y porque anticipa el dominio del proyecto integrador. Tiene objetivo de
regresión (`nota_final`) y de clasificación (`aprobo`, 74 % positivos).

Producido:

- **Teoría (5 documentos):** qué es el ML y cuándo no usarlo · ciclo de vida y definición del
  problema · Git y DVC · álgebra lineal · cálculo y probabilidad. Los dos de fundamentos
  matemáticos incluyen una tabla de "dónde reaparece" que enlaza cada concepto con la sesión
  que lo usa, para que no se perciban como matemáticas sueltas.
- **Notebooks (4):** `01` flujo completo de punta a punta con referencia trivial y
  residuales · `02` los 4 niveles de reproducibilidad (semilla, entorno, hash de datos,
  artefacto) · `03` álgebra lineal a mano hasta SVD · `04` descenso del gradiente a mano hasta
  ajustar una regresión sin scikit-learn.
- **Ejercicios (2 + soluciones):** encuadre de un caso de deserción con detección de fugas de
  datos (incluida una fuga por retroalimentación) · álgebra y gradientes con NumPy.
- **Quiz:** 10 preguntas conceptuales con clave comentada.

**Verificación realizada:** los 4 notebooks se ejecutaron de principio a fin sin errores; los
números citados en las soluciones de los ejercicios provienen de ejecutar el código real.
Todos los enlaces relativos del repositorio resuelven.

**Decisiones tomadas durante la fase:**

- Los notebooks se escriben en formato *percent* (`.py`) y se convierten con
  `herramientas/percent2ipynb.py`. Así se pueden ejecutar como script para verificarlos antes
  de publicarlos, y el diff en git es legible. Usar el mismo flujo en las fases siguientes.
- El entorno conda pasa de llamarse `ml` a **`ml-curso`**, para no colisionar con el entorno
  `ML` que ya existe en la máquina del docente.
- Hallazgos didácticos que conviene conservar al construir los módulos siguientes: el dataset
  tiene variables casi incorreladas, lo que hace que **PCA no aporte nada** sobre él — sirve
  para enseñar cuándo *no* usar reducción de dimensionalidad (ejercicio 02, parte C.4).

### ✅ Fase 2 — Módulo 2: Datos y características

**Dataset conductor elegido:** `titanic.csv` (891 filas, 57 KB, dominio público vía
seaborn-data, versionado). Se eligió porque está sucio de todas las formas que hacen falta
enseñar: `age` 19.9 % nulo (MAR, depende de clase y puerto), `deck` 77.2 % nulo (MNAR),
`class`/`embark_town`/`adult_male` redundantes, 107 filas idénticas que **no** son duplicados
(no hay columna de ID), outliers legítimos (bebé de 5 meses, tarifas de 512) y —el hallazgo
más útil— la columna `alive`, que es **una fuga de datos que viene de fábrica en el dataset**.

Producido:

- **Teoría (5 documentos):** recolección y marco legal · limpieza y calidad (MCAR/MAR/MNAR) ·
  análisis exploratorio · ingeniería de características · selección, `Pipeline` y fuga.
- **Notebooks (4):** `01` diagnóstico y EDA completo del Titanic · `02` 🔵 web scraping ·
  `03` **medición** del sobreoptimismo de cada fuga · `04` `ColumnTransformer` de punta a punta
  hasta el artefacto desplegable.
- **Datos:** además del Titanic, `matriculas-sucio.csv` (620 filas sintéticas con **11 defectos
  plantados**) para el ejercicio 01, y `pagina-ejemplo.html` como fixture local del scraping.
- **Ejercicios (2 + soluciones)** y **quiz** de 10 preguntas con clave comentada.

**Hallazgo empírico que cambió el contenido.** Al medir el sobreoptimismo de cada tipo de fuga
sobre 100 particiones con error estándar, resultó que:

| Fuga | Sobreoptimismo medido |
|---|---|
| Variable derivada del objetivo (`alive`) | hasta accuracy = 1.000 |
| Selección de características fuera de la validación | **+0.09 a +0.13** |
| Imputación con la media fuera del pipeline | indistinguible de cero |
| Escalado fuera del pipeline | indistinguible de cero |

Es decir: **lo que suele enseñarse como el pecado grave (escalar antes de partir) no es
medible, y lo que se menciona de pasada (seleccionar fuera de la validación) es devastador**.
El notebook 03 y la teoría 05 se escribieron alrededor de ese resultado, y el ejercicio 02
hace que el estudiante lo reproduzca sobre otro dataset. Mantener este enfoque —medir en vez de
repetir— en los módulos siguientes.

Otros dos resultados honestos que se conservaron a propósito, en lugar de maquillarlos:

- En el notebook 04, las cuatro variables construidas con buen criterio a partir del EDA **no
  mejoran nada** (diferencia negativa, dentro del ruido). Sirve para enseñar que crear
  variables es barato y demostrar que ayudan es lo caro.
- La importancia por impureza del Random Forest coloca `age` por encima del sexo, porque el
  sexo está repartido en tres columnas y `age` es continua. Se convirtió en la explicación de
  por qué esa gráfica no sirve para descartar variables.

**Verificación realizada:** los 4 notebooks se ejecutan de principio a fin sin errores; todos
los números de las soluciones provienen de ejecutar el código real; los enlaces resuelven.

**Nota de entorno:** la verificación se hace con el entorno conda `ML` preexistente
(Python 3.9), no con `ml-curso` (Python 3.11), que aún no está creado. `lxml` —que necesita
`pd.read_html` en el notebook 02— se instaló en una carpeta temporal vía `PYTHONPATH` para
poder verificar esa celda sin tocar el entorno del docente.

### ✅ Fase 3 — Módulo 3: Regresión y evaluación

**Dataset conductor elegido:** `ames-housing.csv` — 2930 viviendas vendidas en Ames, Iowa
(2006-2010), dominio público (De Cock, 2011) vía [wblakecannon/ames](https://github.com/wblakecannon/ames).
Confirmado con el docente sobre el candidato heredado de `Sesion07-ames_regresion_ml`. Se
descarga y cura con `datos/preparar-ames-housing.py` (columnas identificadoras eliminadas,
encabezados a snake_case); el CSV resultante pesa 923 KB, bajo el umbral de 1 MB, así que se
versiona directo (no requiere script de descarga en `.gitignore`).

**S6 — Regresión lineal (commit `887ac33`).**

- **Teoría (2):** `01-regresion-lineal.md` (formulación matricial, OLS, ecuación normal, los
  5 supuestos del modelo lineal, MSE/RMSE/MAE/$R^2$/$R^2$ ajustado) · `02-descenso-gradiente.md`
  (forma vectorizada, por qué usar descenso en vez de ecuación normal, batch/mini-batch/SGD,
  diagnóstico de convergencia).
- **Notebooks (2):** `01-descenso-gradiente-intuicion` extiende
  `04-gradientes-intuicion.ipynb` del módulo 1 (mismo dataset, `rendimiento-estudiantes.csv`)
  de regresión simple a múltiple (6 predictores), en forma vectorizada; compara batch,
  mini-batch y SGD contra la ecuación normal; y **demuestra en código** que la misma tasa de
  aprendizaje que converge con datos estandarizados diverge sin estandarizar. ·
  `02-regresion-multiple-aplicado` usa Ames Housing con `Pipeline`/`ColumnTransformer`
  (módulo 2), métricas completas y diagnóstico de residuales.

**Hallazgo del notebook 02.** Los residuales del modelo sobre `saleprice` muestran
heterocedasticidad clara (forma de embudo). Modelar $\log(1+\text{precio})$ en vez del precio
directo baja el MAE y el MAPE en los cuatro cuartiles de precio — pero **sube el RMSE
global**, porque una sola vivienda atípica (grande, calidad máxima, vendida muy por debajo de
lo esperado) produce un error de más de 700 mil dólares al revertir la transformación
logarítmica. RMSE y MAE pueden discrepar sobre cuál modelo es mejor.

**S7 — Multicolinealidad y regularización (commit `0933873`).**

- **Teoría (2):** `03-multicolinealidad-polinomica.md` (VIF, qué daña la multicolinealidad y
  qué no, regresión polinómica) · `04-regularizacion.md` (Ridge/Lasso/Elastic Net, geometría
  círculo-vs-diamante, por qué estandarizar es obligatorio).
- **Notebooks (2):** `03-regularizacion-intuicion` — datos sintéticos con dos predictores
  casi idénticos; mide con bootstrap la inestabilidad de OLS; implementa Ridge extendiendo el
  descenso del gradiente y Lasso con descenso por coordenadas (soft-thresholding) a mano,
  ambos validados contra `scikit-learn`. · `04-regularizacion-aplicado` — VIF sobre Ames
  Housing, términos polinómicos que lo disparan a ≈50, Ridge/Lasso con `scikit-learn`.

**Hallazgo del notebook 04.** Agregar `gr_liv_area²` y `overall_qual²` dispara su VIF a ≈50 y
produce coeficientes gigantes de signo opuesto, pero el RMSE de validación **no mejora** con
más regularización: con $n=2930$ frente a $p\approx24$, la multicolinealidad aquí daña la
interpretación, no la predicción. Ridge y Lasso sí estabilizan el par colineal, a ritmos muy
distintos entre sí (Ridge reacciona con $\lambda$ mucho menor que Lasso).

**S8 — Evaluación y selección de modelos (cierra la fase).**

- **Teoría (2):** `05-sesgo-varianza-validacion.md` (descomposición del error, k-fold
  repetido, comparación pareada de modelos con error estándar) · `06-seleccion-hiperparametros.md`
  (grid/random/Optuna, CV anidada, semillas de la búsqueda).
- **Notebooks (2):** `05-sesgo-varianza-intuicion` — sobre $y=\sin(2\pi x)+\varepsilon$ (función
  verdadera conocida), ajusta polinomios de grado 1-15, muestra que el "mejor grado" cambia
  con la semilla del split, implementa k-fold a mano con barras de error, y construye curvas
  de aprendizaje para sub/buen-ajuste/sobreajuste. · `06-seleccion-modelos-aplicado` — sobre
  Ames Housing: `GridSearchCV` reemplaza el split informal de S7; compara grid/random/Optuna
  sobre Elastic Net (2 hiperparámetros); mide el optimismo de no anidar la CV; hace la
  comparación pareada Ridge-vs-Lasso en dos versiones (con y sin fuga de selección) y cierra
  con el RMSE sobre el conjunto de prueba.

**Hallazgo del notebook 06.** Ridge y Lasso, cada uno afinado por CV y comparados sobre los
mismos 10 pliegues, dan **conclusiones distintas según cómo se elija $\lambda$**. Con un
$\lambda$ elegido una sola vez sobre todo `X_train` y evaluado en pliegues de ese mismo
`X_train` —la fuga que el notebook mide en su sección 4—, la diferencia es −\$10 ± \$35
(cociente 0.29): "no hay diferencia detectable". Con $\lambda$ elegido dentro de cada pliegue,
es −\$41 ± \$17 (cociente 2.36): detectable, apenas por encima de la regla de dos errores
estándar. Corregir la fuga no solo movió el número, cambió la respuesta. Y aun así \$41 sobre
un RMSE de \$33,460 es 0.12 %: el notebook cierra distinguiendo **detectable** de **relevante
para decidir**, que es la lección más transferible de la sesión.

**Ejercicios (3) y quiz**, construidos al cerrar la fase, como en los módulos 1 y 2:

- Los tres ejercicios comparten un subconjunto de variables de Ames **distinto** al de los
  notebooks (`lot_frontage`, `1st_flr_sf`, `2nd_flr_sf`, `foundation`, entre otras) y se
  encadenan: `ej01-residuales` descubre que `full_bath`/`half_bath` tienen coeficientes de
  signo contraintuitivo **a pesar de un VIF bajo** (máximo 4.2, ninguna variable supera el
  umbral de 5) — el hallazgo central del módulo en cuanto a los límites del VIF individual.
  `ej02-regularizacion` mide ese VIF, prueba Ridge/Lasso/Elastic Net (incluida la advertencia
  de que la escala de `alpha` de Elastic Net no es comparable a la de Ridge/Lasso solos) y
  muestra que corregir el signo exige un $\lambda$ mucho mayor al que minimiza el RMSE.
  `ej03-validacion-cruzada` cierra con CV formal, grid-vs-random, CV anidada, y una
  comparación pareada que encuentra una diferencia real **y además relevante**: `foundation`
  aporta \$961 ± \$211 de RMSE (cociente 4.6, un 2.4 % del error). El contraste con el
  notebook 06 —donde la diferencia detectable es de \$41, un 0.12 %— es deliberado: la
  herramienta detecta en ambos casos, pero solo en uno la magnitud mueve una decisión.
- **Quiz:** 10 preguntas con clave comentada, cubriendo las tres sesiones.

**Verificación realizada:** los 6 notebooks se ejecutaron de punta a punta sin errores
(código extraído del `.py` intermedio en formato percent); todos los números de teoría,
ejercicios y quiz provienen de ejecutar el código real sobre los datos versionados.

**Nota de entorno.** Igual que en la fase 2, la verificación se hizo con el entorno conda `ML`
preexistente (Python 3.9), no con `ml-curso`, que aún no está creado. El notebook 06 usa
`optuna`, que no estaba instalado en `ML`; se instaló en una carpeta temporal vía `PYTHONPATH`
(con `--only-binary=:all:`, para evitar que `greenlet` intente compilar desde código fuente)
para poder verificar esa celda sin tocar el entorno del docente. `optuna>=3.6` ya está en
`environment.yml`/`requirements.txt` desde la fase 0, así que `ml-curso` lo traerá de fábrica.

**Revisión de la fase (2026-09-09, posterior al commit `7b54849`).** Se releyó el módulo
completo verificando cada número contra una ejecución nueva. Los datos, las tablas de los
ejercicios y los hallazgos de los notebooks 02, 03 y 04 se reprodujeron exactos. Se corrigió:

- **Notebook 01.** La curva de convergencia submuestreaba el historial de batch (`[::5]`) y lo
  graficaba contra un eje etiquetado "época", cuando en batch 1 paso = 1 época. Batch parecía
  5× más rápido de lo que es, y eso ocultaba justo la lección del notebook: mini-batch llega en
  1 época a donde batch tarda ~20. Se quitó el submuestreo y se añadió una tabla de costos por
  época. También se corrigió la afirmación de que mini-batch coincide con la ecuación normal
  "hasta el tercer o cuarto decimal" (coincide hasta centésimas).
- **Notebook 02.** El hallazgo por cuartiles de precio se afirmaba en prosa sin celda que lo
  calculara; ahora se computa (y se confirma: el modelo en log gana en los cuatro).
- **Notebook 03.** La fórmula de umbral suave del markdown no coincidía con el código (el
  factor $1/n$ iba fuera del umbral en vez de dentro). Se añadió una nota sobre las dos
  convenciones de $\lambda$ —Ridge se valida con `alpha = lam * n` y Lasso con `alpha = lam`—,
  que hacía que las dos trayectorias no fueran comparables punto por punto.
- **Notebook 04.** El RMSE de referencia del notebook 02 estaba pegado a mano (\$37,940); ahora
  se recalcula (da el mismo valor).
- **Notebook 05.** Se corrigió la afirmación de que barras de error solapadas son "exactamente
  la comparación pareada", y se añadió la comparación pareada de verdad entre los grados 5 y 7:
  misma conclusión, pero con un ee (0.0035) menor que el de cada grado por separado (0.0093 y
  0.0065) — que es precisamente el motivo de emparejar.
- **Notebook 06.** Cuatro cambios. (a) `TPESampler` usaba el `n_startup_trials=10` de fábrica,
  así que la corrida de 10 trials era **random search puro** y TPE no intervenía nunca; se bajó
  a 5. (b) La sección 3 concluía superioridad de un método sobre otro a partir de diferencias
  de \$1.5 sobre \$34,377; se reencuadró hacia el costo de la búsqueda, que es lo que sí
  distingue a los métodos aquí. (c) La comparación pareada elegía $\lambda$ con todo `X_train`
  y evaluaba en pliegues de ese mismo `X_train` — la fuga que la sección 4 acababa de enseñar;
  ahora se presentan las dos versiones y se muestra que la conclusión cambia. (d) `X_test` se
  creaba y nunca se usaba: el notebook que cierra el módulo no reportaba ningún número sobre
  datos intocados. Ahora sí (\$37,966, contra \$34,450 de la CV anidada).
- **Fuera de los notebooks.** `04-regularizacion.md` afirmaba que OLS no tiene solución cerrada
  (el contraste correcto es con Lasso); se añadió la advertencia sobre los nombres `alpha`/
  `l1_ratio` de `ElasticNet`. `05-sesgo-varianza-validacion.md` ahora aclara que el ee de
  k-fold subestima la incertidumbre porque los pliegues comparten datos.
  `ej03-validacion-cruzada-sol.md` reportaba $\lambda=7.85$, que sale de una rejilla de 20
  puntos y no de la de 15 que sugiere el
  enunciado (7.20); se recalcularon también los números de CV anidada. `environment.yml`
  registraba el kernel como `ml`, mientras `docs/guia-entorno.md` y los 14 notebooks del repo
  usan `ml-curso`.

**Higiene de código.** Los notebooks 02, 04 y 06 compartían un mismo `ColumnTransformer` entre
varios `Pipeline`. Como `Pipeline` no clona sus pasos, el último `fit` dejaba a los demás con
un preprocesador ajustado sobre datos que no les correspondían — sin lanzar ninguna excepción.
Funcionaba por casualidad (los reajustes caían sobre los mismos datos), pero se rompía al
reejecutar celdas fuera de orden. Los tres usan ahora una función `crear_pipeline()`.

---

### ✅ Fase 4 — Módulo 4: Clasificación y ensambles

**Datasets elegidos (confirmados con el docente antes de construir):** `wine-quality.csv`
como conductor de los notebooks y **Adult Census** como caso más retador para los ejercicios.

- **Wine Quality** (UCI, CC BY 4.0; Cortez et al., 2009): 6497 vinos, 11 medidas
  fisicoquímicas + `tipo` + `quality` (3–9). Se une tinto + blanco con
  `datos/preparar-wine-quality.py`; 430 KB, se versiona. Problema binario del módulo:
  `buena = quality >= 7` (19.7 % positivos). Trae **1177 filas idénticas**, que resultaron
  ser el hallazgo didáctico más útil (ver abajo).
- **Adult Census** (UCI, CC BY 4.0; Kohavi y Becker, 1996): 48 842 personas, 14 variables,
  `ingreso_alto` (23.9 %). ~5 MB, así que **no se versiona**: `datos/descargar-adult-census.py`
  (idempotente) y una entrada en `.gitignore`. Categóricas de alta cardinalidad, nulos,
  variables sesgadas (`ganancia_capital`), y proxies de variables sensibles.
- Además, copia de `rendimiento-estudiantes.csv` (módulos 1 y 3) para el notebook 01, que
  extiende a `aprobo` el descenso del gradiente que M3 hizo sobre `nota_final`.

Producido:

- **Teoría (6):** regresión logística · KNN y SVM · métricas y desbalance (S9); árboles y
  bagging (S10); boosting (AdaBoost, gradient boosting, XGBoost/LightGBM, stacking) ·
  interpretabilidad (MDI, permutación, Shapley/SHAP, PDP/ICE, qué no es una explicación) (S11).
- **Notebooks (7, no 6):** S9 `01-logistica-intuicion` (extiende el bucle de descenso de M3
  sin cambiar una línea: solo cambian costo y gradiente; softmax; separación perfecta) ·
  `02-clasificacion-aplicado`. S10 `03-arboles-intuicion` (árbol recursivo a mano que
  coincide con `DecisionTreeClassifier`; bagging a mano) · `04-arboles-bagging-aplicado`.
  S11 `05-boosting-intuicion` (AdaBoost y gradient boosting a mano, validados contra
  `scikit-learn` hasta $10^{-15}$) · `06-boosting-aplicado` · `07-interpretabilidad-aplicado`.
  La S11 lleva tres porque cubre boosting **e** interpretabilidad; fusionarlos habría dado un
  notebook de 40 celdas.
- **Ejercicios (3 + soluciones)** sobre Adult Census, encadenados, y **quiz** de 10 preguntas.

**Hallazgos que cambiaron el contenido** (todos medidos, no supuestos):

1. **Duplicados como fuga que elige al modelo equivocado.** Con las 1177 filas idénticas
   dentro, KNN con $k=1$ obtiene F1 0.66 —muy por encima de la logística y la SVM (0.40–0.44)—;
   sin ellas, 0.47. El 30 % de las filas de prueba tenía un gemelo exacto en entrenamiento.
   El notebook 02 se construyó alrededor de esto, en contraste con el Titanic (M2), donde
   las filas idénticas **no** eran duplicados. El criterio (plausibilidad de que sean
   observaciones distintas + medir) está en teoría 02 y en el quiz.
2. **Balancear clases = mover el umbral.** Pesos de clase y SMOTE suben el recall en 0.5,
   pero AUC-ROC, AP y el mejor F1 alcanzable no cambian en la logística (también en Adult,
   con 10× más datos). En la SVM sí cambian el modelo — y AUC sube mientras AP baja: las
   métricas discrepan, como RMSE/MAE en M3. `scale_pos_weight` en LightGBM: igual.
3. **Random Forest no siempre gana a bagging.** Con 2 variables informativas de 20
   (notebook 03), el 63 % de los nodos no ve ninguna útil y RF es peor. Sobre Wine (12
   variables con señal), `max_features=12` es la peor fila y `max_features=1` la mejor;
   RF − bagging = 0.016 ± 0.003. `max_features` se afina.
4. **Boosting no gana siempre.** Wine: boosting por defecto (AP 0.54) < RF (0.57) <
   Extra-Trees (0.59); LightGBM tras 40 trials de Optuna (0.57) sigue 0.022 ± 0.004 por debajo
   de Extra-Trees sin afinar. Stacking: +0.006 ± 0.003, detectable, no relevante. **Adult
   (ejercicios): se invierte** — LightGBM por defecto 0.83 frente a RF 0.78; LightGBM − RF
   afinado = 0.026 ± 0.001; y `min_samples_leaf=1` deja de ser lo mejor para RF (0.775 → 0.803
   con 5). La pareja de datasets se eligió para poder mostrar las dos direcciones.
5. **Sesgos de las importancias, medidos.** MDI: una columna de ruido gaussiano queda por
   encima de cuatro variables reales y 6× por encima del ruido binario (misma explicación
   para `age` > sexo en el Titanic de M2). Permutación: con las correlaciones reales (0.5–0.7)
   el punto ciego es de solo un 4 %; con una copia de `alcohol`, su importancia cae de 0.104 a
   0.017. En Adult aparece sin plantar nada: `fnlwgt` es la segunda variable por número de
   particiones y nada por permutación; `relacion` es `sexo × estado_civil`.
6. **Quitar `sexo` no quita el sexo** (ejercicio 03): `Husband`/`Wife` lo codifican al
   100 %; sin la columna, la AP y las tasas de positivos predichos por sexo no cambian. Es la
   entrada del módulo al tema de sesgos (🔵 del README), tratada como medición, no como
   sermón.

**Verificación realizada:** los 7 notebooks se ejecutaron de principio a fin sin errores
(código extraído del `.py` percent, ejecutado desde `notebooks/`, figuras revisadas una a
una); todos los números de teoría, README, ejercicios y quiz provienen de esas ejecuciones y
de los scripts de solución sobre `adult-census.csv`. Optuna con `TPESampler(seed=42,
n_startup_trials=10)` es reproducible corrida a corrida (mismos hiperparámetros); los
hiperparámetros resultantes están copiados a mano en el notebook 07, que no repite la
búsqueda. Enlaces relativos del módulo verificados por script.

**Nota de entorno.** Como en las fases 2 y 3, la verificación se hizo con el entorno conda
`ML` (Python 3.9). `xgboost`, `lightgbm`, `shap`, `imbalanced-learn`, `seaborn` y `optuna` no
estaban instalados; se instalaron con `pip install --only-binary=:all: --target <carpeta
temporal>` y `PYTHONPATH`, sin tocar el entorno del docente. Todos están en
`environment.yml`/`requirements.txt` desde la fase 0. Versiones usadas: scikit-learn 1.6.1,
xgboost 2.1.4, lightgbm 4.6.0, shap 0.49.1, imbalanced-learn 0.12.4.

**Detalles de implementación que conviene conservar:**

- `evaluar_cv()` reporta la AP como **promedio de la AP por pliegue** (con error estándar);
  el notebook 02 la calculaba sobre las probabilidades de `cross_val_predict` juntas (0.517
  vs. 0.526 para la logística). La diferencia está explicada en el notebook 04; no mezclar.
- `shap.plots.scatter(..., color=explicacion)` falla con columnas categóricas (`dtype=
  category`): la selección automática de la variable de color compara `str` con `float`. El
  ejercicio 03 pide colorear por `horas_semana` explícitamente.
- `oob_decision_function_` tiene `nan` para filas que ningún árbol dejó fuera; con $B=10$
  le pasa al 1 %. El notebook 04 las filtra antes de calcular la AP OOB.
- Los notebooks 05 y 06 tardan ~1 y ~2 minutos; el resto, segundos. El más lento es el
  `GradientBoostingClassifier` exacto del notebook 05 (50 s sobre 30 000 filas), que está ahí
  a propósito para medir la diferencia con los histogramas.

---

## 4. Qué sigue — Fase 5 (Módulo 5: No supervisado y deep learning, S12–S13)

Producir en `modulo-5-no-supervisado-deep-learning/`:

- **Teoría (propuesta, 4–5 documentos):** clustering (K-Means/K-Means++, jerárquico,
  DBSCAN) · validación de clusters (codo, silueta, Davies-Bouldin) · reducción de
  dimensionalidad (PCA, t-SNE, 🔵 UMAP) · 🔵 detección de anomalías — S12; perceptrón, MLP,
  activaciones, retropropagación, entrenamiento en PyTorch, cuándo no usar deep learning —
  S13.
- **Notebooks (propuesta, 4–5):** S12 `01-clustering-intuicion` (K-Means a mano: asignación
  y actualización; ver que el resultado depende de la inicialización y qué arregla K-Means++)
  · `02-clustering-aplicado` (comparación de algoritmos y validación sobre el dataset
  conductor) · `03-reduccion-dimensionalidad` (PCA a mano vía la SVD del módulo 1; t-SNE;
  cuándo PCA no aporta — `rendimiento-estudiantes.csv` tiene variables casi incorreladas,
  hallazgo de la fase 1). S13 `04-mlp-intuicion` (perceptrón y retropropagación a mano,
  extendiendo por tercera vez el descenso del gradiente: M1 → M3 → M4 nb01 → aquí) ·
  `05-pytorch-aplicado` (MLP en PyTorch sobre tabular, comparado contra el mejor ensamble de
  M4 sobre los mismos datos, para enseñar cuándo **no** usar deep learning).
- **Dataset conductor:** pendiente de confirmar (decisión 1 abajo). Para el notebook 05
  conviene reutilizar Wine Quality o Adult Census, para que la comparación "MLP vs. LightGBM"
  sea sobre datos ya conocidos y con números ya establecidos (AP 0.59 / 0.83).
- **Ejercicios (2–3) y quiz**, al cierre.

Puntos a cuidar:

- El material previo tiene 5 notebooks de PCA/t-SNE (`Sesion04-*`) y uno de clustering
  (`Sesion10-Clustering`): consolidar, no copiar. Ver mapa de la sección 5.
- S13 es un **puente** (decisión de diseño de la fase 0): un solo notebook de PyTorch, sin
  CNN ni transfer learning más allá de un vistazo 🔵. El criterio "cuándo no usar DL" debe
  salir de una medición, no de una afirmación: un MLP afinado contra LightGBM sobre tabular.
- Patrones a mantener de M3/M4: `.py` percent → `.ipynb`; números de teoría y ejercicios
  desde ejecuciones reales; comparación pareada con error estándar; "detectable vs.
  relevante"; datasets confirmados con el docente antes de construir.

### Decisiones abiertas para consultar con el docente

1. **Dataset conductor del módulo 5** — M2 usa Titanic, M3 Ames Housing, M4 Wine Quality +
   Adult Census (todos confirmados por el docente antes de construir). Para M5 hay dos
   candidatos: reutilizar **Wine Quality** (ya conocido; `tipo` tinto/blanco es una etiqueta
   natural para validar clusters *a posteriori*, y PCA sobre las 11 variables tiene sentido
   porque sí están correlacionadas, a diferencia de `rendimiento-estudiantes.csv`), o un
   dataset nuevo (p. ej. clientes de un centro comercial / segmentación, más "de negocio").
   Para S13, reutilizar Wine Quality o Adult Census en la comparación MLP vs. LightGBM.
2. **Tema del proyecto integrador** — propuesta: predicción de deserción estudiantil con
   dataset sintético realista (nulos, categóricas, desbalance y una fuga de datos plantada a
   propósito). El módulo 1 ya sienta el dominio con `rendimiento-estudiantes.csv`.
   Alternativa: reutilizar el enunciado del trabajo final de la edición anterior si el docente
   lo aporta a `proyecto-integrador/`.
3. **Pesos de evaluación** — los de `docs/programa.md` (60/25/15) son una sugerencia; ajustar
   al reglamento del programa.
4. **Talleres** — la evaluación acordada fue proyecto + quiz, y las entregas parciales del
   proyecto hacen las veces de taller por módulo. Si se prefieren talleres independientes, hay
   que añadirlos a la estructura de cada módulo.

---

## 5. Mapa del material previo → módulos

Referencia para saber qué insumo existe al construir cada módulo. Todo está en
`contenido_anterior/` (no versionado).

| Material previo | Destino | Acción | Estado |
|---|---|---|---|
| PDFs S1–S12 | Teoría de los 6 módulos | Reescribir como texto con LaTeX | parcial (M1–M4 hechos) |
| `Sesion03-Limpieza de datos` (Titanic) | M2/S4 | Reusar dataset; reescribir con EDA más fuerte | ✅ hecho |
| `Sesion03-webscraping` (BeautifulSoup) | M2/S4 🔵 | Reusar; fijar la fuente para que no se rompa | ✅ hecho (fixture local) |
| `Sesion04-PCA*` ×3, `Sesion04-TSNE*` ×2 | M5/S12 | Consolidar 5 → 2 (intuición + aplicado) | pendiente |
| `Sesion05-Ingenieria_caracteristicas` (NYC Taxi) | M2/S5 | Reescrito sobre `Pipeline`/`ColumnTransformer`; se usó Titanic en vez de NYC Taxi para mantener un solo dataset conductor | ✅ hecho |
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 | ✅ hecho |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida | ✅ hecho |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidado 7 → 2; Wine Quality (tinto + blanco, sin duplicados) como caso canónico | ✅ hecho |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividido: CV y GridSearch subieron a S8; árboles y bagging en M4/S10, reescritos sobre Wine Quality en vez de Titanic | ✅ hecho |
| `Sesion10-Clustering` | M5/S12 | Base reutilizable; añadir comparación de algoritmos | pendiente |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidado 4 → 3 (boosting intuición, boosting aplicado, interpretabilidad); Optuna pasó a S8 y aquí solo se usa; Breast Cancer reemplazado por Wine Quality | ✅ hecho |
| *(no existía)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** | M1 hecho |

El módulo 1 no reutilizó ningún notebook previo: no existían para S1 ni S2, y los de S4 sobre
PCA/t-SNE se movieron al módulo 5. El módulo 2 reutilizó el **dataset** de `Sesion03` y la idea
del scraping, pero reescribió por completo el contenido.

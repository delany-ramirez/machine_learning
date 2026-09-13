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
| Entorno | **uv**: `pyproject.toml` + `uv.lock` + `.python-version` (3.11), `.venv` en la raíz del repo; `requirements.txt` solo como respaldo pip. El kernel de Jupyter (y el prompt) se llama `ml-curso`, **no** `ml`: ya existe un entorno `ML` en la máquina del docente y en Windows los nombres no distinguen mayúsculas |

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
| 5 | **Módulo 5** — No supervisado y deep learning (S12–S13) | ✅ hecha | `16dc27d` (S12) · `0d0acec` (S13) |
| 6 | **Módulo 6** — MLOps y despliegue (S14) | ✅ hecha | |
| 7 | **Proyecto integrador** — enunciado, datos, rúbrica, entregas | ⬜ pendiente | |
| 8 | **Recursos generales** — bibliografía, enlaces, glosario, cheatsheets, plantillas | ⬜ pendiente | |
| 9 | **QA global** — ejecutar todos los notebooks, verificar enlaces y coherencia | ⬜ pendiente | |
| 10 | *(opcional)* Slides Slidev por módulo | ⬜ no planificada | |

Cada fase cierra con un commit en español (`Fase N: ...`) que incluye la actualización de este
archivo.

**Fuera de las fases:** `modulo-0-instalacion/` (2026-09-11) — tutorial de instalación para
estudiantes (Git, Miniconda, entorno, VS Code, Colab como plan B, FAQ, tabla de problemas,
glosario, checklist) más `verificar-entorno.py`, que comprueba Python, paquetes, kernel y Git.
`docs/guia-entorno.md` queda como versión corta y enlaza al tutorial. Verificado creando
`ml-curso` desde cero en Windows: el script termina con 34 OK. Hallazgo: la rueda de pip de
`torch` (2.14) se instala pero no importa en Windows dentro de conda (`shm.dll`), así que
`environment.yml` ahora instala `pytorch-cpu` desde conda-forge (más pequeño y funciona).

**Migración a uv** (2026-09-12) — el gestor del curso pasa de Miniconda a
[uv](https://docs.astral.sh/uv/): `environment.yml` se elimina y lo reemplazan
`pyproject.toml` (dependencias, `torch` desde el índice CPU de PyTorch para que en Linux no
baje CUDA, `package = false`), `uv.lock` (258 paquetes resueltos para Windows/Linux/macOS
arm64) y `.python-version` (3.11). Flujo para estudiantes: `uv sync` → `uv run …`, sin
activar nada. `requirements.txt` se conserva como respaldo pip (opción B), en sincronía a
mano. Se reescriben `modulo-0-instalacion/README.md`, `docs/guia-entorno.md`, la puesta en
marcha del `README.md` y `verificar-entorno.py` (ahora comprueba que el intérprete sea el
`.venv` del repo, que `uv` esté en el PATH y que el kernel `ml-curso` apunte a ese `.venv`,
no a otro Python). Verificado en Windows desde cero: `uv sync` instala 248 paquetes
(`.venv` de 1.6 GB) y el script termina con 35 OK. Versiones que trae el lock: numpy 2.4,
pandas 3.0, scikit-learn 1.9, torch 2.14+cpu, mlflow 3.16, xgboost 3.2, lightgbm 4.7.

**Celda de arranque para Google Colab** (2026-09-13) — el portal `ml.delanyr.dev` abre cada
notebook en Colab cargando solo el `.ipynb` desde GitHub, así que las rutas relativas
`../datos/...` no existían allí. Los 29 notebooks de `modulo-*/notebooks/` llevan ahora una
primera celda de código etiquetada `colab-arranque` que, solo si `google.colab` está en
`sys.modules`, clona el repositorio (`--depth 1`) en `/content/machine_learning` y hace `%cd` a
la carpeta del notebook; en local no hace nada. Añade `%pip install -q` únicamente con lo que
el notebook importa y Colab no trae (`optuna` en M3·06 y M4·06, `shap` en M4·07, `umap-learn`
en M5·04, `mlflow` en M6·01) y, en M5·06, ejecuta `descargar-adult-census.py` si el CSV no
existe. La genera `herramientas/celda_colab.py` (idempotente, sin dependencias, respeta
salidas, metadatos y kernel) y `percent2ipynb.py` la inserta al convertir, omitiéndola en
`--solo-codigo`. Verificado: los 29 `.ipynb` siguen siendo JSON válido con la celda en su
sitio, una segunda pasada no cambia ningún byte, M1·01 ejecuta de principio a fin en el kernel
local con la celda como no-op, y las 29 celdas se transforman y compilan en IPython.
Documentado en `docs/convenciones.md` (§4.3) y en el Plan B de `modulo-0-instalacion/README.md`.

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

### ✅ Fase 5 — Módulo 5: No supervisado y deep learning

**Datasets elegidos (confirmados con el docente antes de construir):** **Wine Quality**
como conductor de S12 y S13 (sus 11 variables sí están correlacionadas, `tipo` valida
clusters *a posteriori*, y los números del módulo 4 —AP 0.52 / 0.57 / 0.59— sirven de
referencia para el MLP), `digits` de `scikit-learn` para t-SNE/UMAP, la compresión con PCA
y la 🔵 CNN (sin descarga), **Adult Census** para la comparación MLP vs. LightGBM con 10×
más datos (script copiado del módulo 4, no versionado), y `rendimiento-estudiantes.csv`
como el caso en que PCA no aporta y un MLP no puede ganar a un modelo lineal.

Producido:

- **Teoría (5):** clustering (K-Means, jerárquico, DBSCAN; supuestos y cuál usar) ·
  validación de clusters (codo, silueta, Davies-Bouldin; referencia nula y estabilidad;
  ARI/NMI; protocolo) · reducción de dimensionalidad (PCA por covarianza y SVD, cuándo daña;
  t-SNE; 🔵 UMAP) — S12; redes neuronales (perceptrón, MLP, activaciones, retropropagación,
  aproximación universal) · entrenamiento y límites (PyTorch, optimizadores,
  regularización, la fuga del early stopping, cuándo no usar DL) — S13.
- **Notebooks (6):** S12 `01-clustering-intuicion` (Lloyd, K-Means++, jerárquico y DBSCAN a
  mano, validados contra `scikit-learn` y SciPy; codo y silueta a mano) ·
  `02-clustering-aplicado` (Wine sin etiquetas) · `03-pca-intuicion` (autovectores y SVD
  validados; dígitos; dos límites medidos) · `04-reduccion-dimensionalidad-aplicado`
  (t-SNE/UMAP frente a PCA con *trustworthiness*, KNN y silueta). S13 `05-mlp-intuicion`
  (retropropagación en NumPy verificada por diferencias finitas y contra autograd) ·
  `06-mlp-pytorch-aplicado` (comparación pareada contra los modelos del módulo 4; 🔵 CNN).
  Cuatro en S12 porque cubre tres temas (clustering, validación, reducción); dos en S13.
- **Ejercicios (3 + soluciones)** sobre datos que los notebooks no analizaron (tintos,
  dígitos, estudiantes + Adult) y **quiz** de 10 preguntas.

**Hallazgos que cambiaron el contenido** (todos medidos):

1. **Los criterios internos siempre proponen un $k$.** Sobre puntos uniformes, la silueta
   de K-Means tiene su máximo en $k=4$ con valor 0.41 (con cuatro grupos reales, 0.77).
   La **referencia nula** (columnas permutadas) pasó a ser el centro de la validación:
   Wine Quality da 0.27 frente a 0.10, los tintos solos 0.205 frente a 0.09, y una gaussiana
   en 10D llevada a un mapa t-SNE da grumos con silueta 0.35–0.38 frente a 0.08 en los datos.
2. **El clustering encuentra la estructura dominante, no la que interesa.** K-Means con
   $k=2$ recupera tinto/blanco (ARI 0.93) sin ver `tipo`; dentro de los blancos, dulces/secos;
   y con ningún $k$ dice nada de la calidad (NMI $\leq 0.07$). PCA encuentra exactamente lo
   mismo (PC1 = tinto/blanco, PC2 = dulce/seco) porque ambos buscan la varianza dominante.
3. **Los *linkages* con datos reales.** *Average*, *complete* y *single* cortan un solo
   vino atípico y dejan 5319 juntos; Ward coincide con K-Means (ARI 0.90) en el conjunto
   completo pero **no** en los tintos (0.32), donde no hay una partición claramente mejor.
4. **DBSCAN en 11-D es un detector de anomalías**, no de grupos: solo separa tinto/blanco
   dejando un tercio como ruido; con `eps=2` señala 191 vinos con alguna variable extrema
   (el máximo global de las 11 está entre ellos), y coincide en un tercio con Isolation
   Forest — "anomalía" no tiene una definición única.
5. **PCA no ve $y$.** PC1 (91 %) da accuracy 0.47 y PC2 (9 %) da 0.93 en un ejemplo
   construido; en Wine, PCA completo deja la AP idéntica (rotación) y quitar componentes
   la baja de 0.52 a 0.40. En los dígitos, en cambio, 20 componentes de 64 igualan al KNN
   completo (ejercicio 02): la regla es validar con la métrica del modelo, no con la varianza.
6. **t-SNE conserva vecindarios y nada más.** Un grupo 5× más disperso aparece del mismo
   tamaño; uno 3× más lejano, a la misma distancia; y `init="pca"` (el valor por defecto)
   hace el resultado insensible a la semilla, así que la demostración "otra semilla, otro
   mapa" necesita `init="random"`. Clusterizar el mapa sube el ARI de 0.67 a 0.89 en los
   dígitos, y los subgrupos que dibuja entre los "1" existen en 64D (tres formas de
   escribirlo; silueta 0.35 frente a 0.04 de la nula) — el mapa exagera, no inventa, ahí.
7. **Sobreparametrización benigna.** Sobre 60 puntos del seno, la red de 100 neuronas
   ajusta la función verdadera mejor que la de 10 (ECM 0.011 frente a 0.079); la intuición
   de la S8 no se cumple automáticamente con el ancho. El sobreajuste sí aparece con pocos
   datos y muchas épocas (lunas: validación de 0.22 a 0.29), y con eso se motiva el early
   stopping. El primer borrador diverge con 100 neuronas y tasa fija: la escala $1/\sqrt{h}$
   de la capa de salida es necesaria.
8. **El desvanecimiento del gradiente depende de la inicialización tanto como de la
   activación.** Con la inicialización por defecto de PyTorch, ReLU también pierde dos
   órdenes en 10 capas; con Glorot para sigmoide/tanh y He para ReLU, sigmoide pierde $10^6$
   y tanh/ReLU quedan en cociente 0.3–0.4. El notebook usa la inicialización recomendada.
9. **La red no gana en tabular, y una fuga que la favorece.** Wine: MLP − Extra-Trees
   = −0.046 ± 0.004 (cociente 10), empate con LightGBM por defecto, +0.023 sobre la
   logística, 6× el tiempo de Extra-Trees. Adult: −0.047 ± 0.001 contra LightGBM, y una red
   256-128 no mejora a una de 64 (ejercicio 03). Sobre `rendimiento-estudiantes` (proceso
   lineal), el MLP **pierde** contra la regresión lineal (+0.015 ± 0.005 de RMSE). Hacer el
   early stopping sobre el pliegue evaluado infla la AP 0.017 en Wine y 0.004 en Adult: el
   envoltorio `MLPClasificador` aparta un 15 % del entrenamiento para eso.
10. **La CNN sobre dígitos de 8 × 8 gana poco en accuracy (97.9 % frente a 97.0 % de la
    logística) y mucho en robustez**: con los dígitos corridos un píxel, 0.62 frente a
    0.42–0.51. La primera versión afirmaba "la mitad de los errores con menos parámetros";
    era falso (la CNN tiene 6× más parámetros que el MLP) y se reemplazó por la prueba de
    desplazamiento, que mide el sesgo inductivo directamente.

**Verificación realizada:** los 6 notebooks se ejecutaron de principio a fin sin errores,
primero como `.py` percent con las figuras revisadas una a una y después como `.ipynb` con
`nbconvert --execute` en el `.venv` de `uv`; todos los números de teoría, README, ejercicios
y quiz provienen de esas ejecuciones y de los tres scripts de solución. Tiempos: los
notebooks 01–03 y 05 corren en segundos; 04 en ~50 s (UMAP compila con `numba`); 06 en
~2 min (20 pliegues del MLP en CPU).

**Nota de entorno.** Primera fase verificada con el entorno oficial del curso (`uv sync`,
Python 3.11.15, `uv.lock`): scikit-learn 1.9.1, pandas 3.0.5, numpy 2.4.6, torch 2.14.0+cpu,
umap-learn 0.5.12, lightgbm 4.7.0. `select_dtypes("object")` ya no selecciona texto con
pandas 3 (strings nativos): usar `select_dtypes(exclude="number")`.

**Detalles de implementación que conviene conservar:**

- La referencia nula por permutación de columnas usa el `rng` del notebook; los valores
  son estables a la segunda cifra entre semillas.
- `TSNE(init="pca")` es determinista respecto a `random_state`; para mostrar variabilidad
  hay que usar `init="random"`.
- `umap-learn` emite avisos de versión de `numba`; los notebooks los silencian con
  `warnings.filterwarnings("ignore")`.
- `entrenar_mlp` en el notebook 06 baraja con un `torch.Generator` sembrado y guarda el
  mejor `state_dict`; con `torch.set_num_threads(4)` los tiempos son reproducibles en
  orden de magnitud. El MLP se envuelve en `MLPClasificador` (interfaz `fit`/`predict_proba`)
  para entrar en la misma comparación pareada que los modelos de `scikit-learn`.

### ✅ Fase 6 — Módulo 6: MLOps y despliegue

**Datos:** Wine Quality (copiado de M4/M5) para el notebook de MLflow y la API, y un
dataset nuevo, `cohortes-estudiantes.csv` — 24 meses × 300 estudiantes generados con el
proceso de `rendimiento-estudiantes.csv`, con **drift de datos plantado desde el mes 13**
(fracción que trabaja 0.38 → 0.65, promedio anterior −0.15) y **drift de concepto desde el
19** (coeficiente de horas 0.055 → 0.020, intercepto +0.45 para que la nota media no lo
delate). Como en el módulo 1, conocer el proceso generador permite medir qué detecta cada
herramienta y cuál se queda ciega.

Producido:

- **Teoría (4):** trazabilidad con MLflow · APIs para modelos · empaquetado y despliegue ·
  monitoreo y drift.
- **Notebooks (2):** `01-mlflow-aplicado` (seis candidatos de M4–M5 como corridas con
  hash de datos, commit, versiones, semilla, AP ± ee, **tamaño y latencia**; `search_runs`;
  registro con alias `campeon`/`produccion`; reproducción exacta) · `02-drift-intuicion`
  (PSI/KS por variable, distribución de predicciones, carta de control del RMSE,
  diagnóstico por coeficientes, cuatro estrategias de reentrenamiento).
- **Código de despliegue:** `api/` (FastAPI + Pydantic, modelo en el `lifespan`,
  `/health`, `/predict`, `/predict/lote`; `entrenar_modelo.py` produce
  `modelo-ejemplo.joblib` como paquete con columnas, umbral por costos y metadatos;
  `probar_api.py` con seis pruebas; `requirements-api.txt` con las versiones de
  `uv.lock`), `docker/` (`Dockerfile` sobre `ghcr.io/astral-sh/uv:python3.11-bookworm-slim`,
  README línea a línea) y `.dockerignore`.
- **Ejercicios (2 + soluciones)** y **quiz** de 10 preguntas.

**Hallazgos que cambiaron el contenido** (todos medidos):

1. **Campeón ≠ producción.** Extra-Trees 300 (mejor AP, 0.589) pesa 12 MB y predice 20×
   más lento que el `HistGradientBoostingClassifier` (0.547, 0.15 MB). Tamaño y latencia
   pasaron a ser métricas registradas en cada corrida, y la API sirve el HGB con la razón
   anotada como tag de la versión. En Adult (ejercicio 01) sí coinciden: LightGBM gana en
   AP, tamaño y latencia, y Random Forest (11.6 MB) queda descartado por los tres.
2. **MLflow 3 guarda scikit-learn en skops**, que rechaza tipos no declarados: registrar
   un `LGBMClassifier` con `mlflow.sklearn.log_model` falla; se usa `mlflow.lightgbm`. El
   registro de modelos exige backend de base de datos (`sqlite:///mlflow.db`; el file
   store no lo soporta), y `search_model_versions` no devuelve los alias — hay que
   pedirlos con `get_model_version`.
3. **La métrica no detecta cambios en los datos.** Cambiar una fila de Adult deja la AP de
   LightGBM idéntica hasta el sexto decimal (ejercicio 01, C.2); solo el hash lo ve.
4. **Drift de datos sin daño; drift de concepto sin aviso.** Mes 13: PSI de `trabaja` de 0
   a 0.3–0.4, nota predicha media de 3.42 a 3.16, RMSE **sin cambio** (0.34: el modelo lineal
   es correcto y la región estaba representada; un HGB tampoco se degrada). Mes 19: PSI
   plano, RMSE 0.34 → 0.44. Reajustar sobre los meses en alarma recupera el cambio
   plantado (horas 0.053 → 0.019). Reentrenar tras la alarma: todo el historial 0.42,
   ventana de 6 meses 0.39, solo desde el cambio 0.36 (≈ ruido), sin reentrenar 0.44.
5. **La AP alarma con el drift de datos y no con el de concepto** (ejercicio 02): para el
   clasificador de `aprobo`, la prevalencia baja de 0.74 a 0.65 en el mes 13 y la AP cae
   bajo la carta de control sin que la relación cambie; en el 19 la prevalencia vuelve y
   la AP sube justo cuando el modelo se degrada. El AUC (0.88–0.91 → 0.82–0.87) cuenta la
   historia correcta. La solución del ejercicio y la pregunta 10 del quiz giran sobre eso.
6. **La imagen no instala `pyproject.toml`.** El entorno del curso pesa 1.6 GB; la API
   necesita ~270 MB (`requirements-api.txt`, versiones de `uv.lock`). Verificado creando
   ese entorno mínimo con `uv venv` + `uv pip install` y levantando la API desde él.

**Verificación realizada:** los 2 notebooks ejecutados de principio a fin con `nbconvert`
en el `.venv` de uv (el 01 crea `mlflow.db` y `mlruns/`, ignorados por Git); las seis
pruebas de `api/probar_api.py` pasan; la API levantada con `uvicorn` responde a `curl`
(`/health`, `/predict` → 0.7403, `alcohol: 94` → 422) con mediana 2.7 ms y p95 3.7 ms en
200 peticiones; la API arranca desde un entorno construido solo con
`requirements-api.txt`. **No verificado:** `docker build` (no hay Docker en la máquina del
docente); el `Dockerfile` está documentado en `docker/README.md` con esa salvedad y con
la URL de las etiquetas de la imagen base por si la etiqueta cambia. Enlaces relativos del
módulo verificados por script.

**Detalles de implementación que conviene conservar:**

- Tracking en `sqlite:///mlflow.db` relativo a `notebooks/`; `mlflow ui
  --backend-store-uri sqlite:///mlflow.db` desde esa carpeta. `MLFLOW_DISABLE_AGENT_HINT=1`
  y `logging.getLogger("mlflow").setLevel(logging.ERROR)` silencian los avisos.
- El modelo de la API se guarda como diccionario (modelo, columnas, umbral, metadatos);
  `/health` reporta los metadatos. El umbral (0.22) sale de FN = 3 × FP sobre
  probabilidades de CV, como en M4.
- En Windows, un entorno virtual en una ruta muy larga (> ~200 caracteres) hace fallar la
  carga de las extensiones compiladas de scikit-learn (`ModuleNotFoundError` en
  `_middle_term_computer`); el entorno mínimo de verificación se creó en una ruta corta.
- `api/__init__.py` existe para que `uvicorn api.main:app` y las importaciones relativas
  funcionen igual en local y en el contenedor.

---

## 4. Qué sigue — Fase 7 (Proyecto integrador)

Producir en `proyecto-integrador/`, según lo previsto en `docs/programa.md` y en los
READMEs de los módulos (entregas E1–E6):

- **Enunciado** del caso (decisión abierta 1: deserción estudiantil con dataset sintético
  realista, o el trabajo final de la edición anterior si el docente lo aporta).
- **Datos**: si es sintético, generador con semilla fija que plante nulos, categóricas de
  alta cardinalidad, desbalance, una fuga de datos, y un drift en una cohorte posterior
  (reutilizando `generar-cohortes-drift.py` como base); documentado en el README como en
  los módulos.
- **Entregas E1–E6** con lo que cada módulo ya anuncia en su sección "Entrega del proyecto
  integrador" (E1 encuadre y repo; E2 datos y pipeline; E3 línea base y evaluación; E4
  ensambles con comparación pareada y umbral por costos; E5 exploración no supervisada o
  MLP comparado; E6 MLflow + API + Dockerfile + monitoreo + informe).
- **Rúbrica** única (decisión abierta 2 sobre los pesos) y **plantilla** del informe final.
- Un ejemplo de referencia parcial (no la solución completa) para calibrar la rúbrica.

Puntos a cuidar: coherencia con las secciones "Entrega" de los seis módulos (revisarlas y
ajustar el texto si el enunciado final las contradice); que el caso permita una fuga de
datos *plantada* que E1 deba detectar; que E6 exija el documento de monitoreo de una
página del módulo 6.

### Decisiones abiertas para consultar con el docente

1. **Tema del proyecto integrador** — propuesta: predicción de deserción estudiantil con
   dataset sintético realista (nulos, categóricas, desbalance y una fuga de datos plantada a
   propósito). El módulo 1 ya sienta el dominio con `rendimiento-estudiantes.csv`.
   Alternativa: reutilizar el enunciado del trabajo final de la edición anterior si el docente
   lo aporta a `proyecto-integrador/`.
2. **Pesos de evaluación** — los de `docs/programa.md` (60/25/15) son una sugerencia; ajustar
   al reglamento del programa.
3. **Talleres** — la evaluación acordada fue proyecto + quiz, y las entregas parciales del
   proyecto hacen las veces de taller por módulo. Si se prefieren talleres independientes, hay
   que añadirlos a la estructura de cada módulo.

---

## 5. Mapa del material previo → módulos

Referencia para saber qué insumo existe al construir cada módulo. Todo está en
`contenido_anterior/` (no versionado).

| Material previo | Destino | Acción | Estado |
|---|---|---|---|
| PDFs S1–S12 | Teoría de los 6 módulos | Reescribir como texto con LaTeX | ✅ hecho (M6 no tenía PDF) |
| `Sesion03-Limpieza de datos` (Titanic) | M2/S4 | Reusar dataset; reescribir con EDA más fuerte | ✅ hecho |
| `Sesion03-webscraping` (BeautifulSoup) | M2/S4 🔵 | Reusar; fijar la fuente para que no se rompa | ✅ hecho (fixture local) |
| `Sesion04-PCA*` ×3, `Sesion04-TSNE*` ×2 | M5/S12 | Consolidado 5 → 2 (`03-pca-intuicion`, `04-reduccion-dimensionalidad-aplicado`); `load_wine` (178 filas) reemplazado por Wine Quality, y `digits` conservado para t-SNE | ✅ hecho |
| `Sesion05-Ingenieria_caracteristicas` (NYC Taxi) | M2/S5 | Reescrito sobre `Pipeline`/`ColumnTransformer`; se usó Titanic en vez de NYC Taxi para mantener un solo dataset conductor | ✅ hecho |
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 | ✅ hecho |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida | ✅ hecho |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidado 7 → 2; Wine Quality (tinto + blanco, sin duplicados) como caso canónico | ✅ hecho |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividido: CV y GridSearch subieron a S8; árboles y bagging en M4/S10, reescritos sobre Wine Quality en vez de Titanic | ✅ hecho |
| `Sesion10-Clustering` | M5/S12 | Reescrito: los tres algoritmos a mano y validados (`01`), flujo completo con referencia nula sobre Wine Quality (`02`); `make_blobs`/Iris reemplazados | ✅ hecho |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidado 4 → 3 (boosting intuición, boosting aplicado, interpretabilidad); Optuna pasó a S8 y aquí solo se usa; Breast Cancer reemplazado por Wine Quality | ✅ hecho |
| *(no existía)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** | ✅ hecho |

El módulo 1 no reutilizó ningún notebook previo: no existían para S1 ni S2, y los de S4 sobre
PCA/t-SNE se movieron al módulo 5. El módulo 2 reutilizó el **dataset** de `Sesion03` y la idea
del scraping, pero reescribió por completo el contenido.

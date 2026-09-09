# PLAN — Bitácora de construcción del curso

Este archivo es la **memoria del proyecto entre sesiones de trabajo**. Al retomar el trabajo,
léelo primero: dice qué está hecho, qué sigue y qué decisiones ya se tomaron.

**Última actualización:** 2026-09-09 · **Fase actual:** 3 en curso (S6 hecha, sigue S7).

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
| 3 | **Módulo 3** — Regresión y evaluación (S6–S8) | 🔶 en curso (S6 hecha) | `887ac33` (S6) |
| 4 | **Módulo 4** — Clasificación y ensambles (S9–S11) | ⬜ pendiente | |
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

### 🔶 Fase 3 (en curso) — Módulo 3: Regresión y evaluación

**Dataset conductor elegido:** `ames-housing.csv` — 2930 viviendas vendidas en Ames, Iowa
(2006-2010), dominio público (De Cock, 2011) vía [wblakecannon/ames](https://github.com/wblakecannon/ames).
Confirmado con el docente sobre el candidato heredado de `Sesion07-ames_regresion_ml`. Se
descarga y cura con `datos/preparar-ames-housing.py` (columnas identificadoras eliminadas,
encabezados a snake_case); el CSV resultante pesa 923 KB, bajo el umbral de 1 MB, así que se
versiona directo (no requiere script de descarga en `.gitignore`).

**✅ S6 — Regresión lineal (commit `887ac33`).** Producido:

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
- **Datos:** `ames-housing.csv` + `preparar-ames-housing.py`; copia de
  `rendimiento-estudiantes.csv` y su generador (módulo 1) para el notebook 01.

**Hallazgo empírico que quedó documentado (mismo espíritu "medir, no asumir" del módulo 2).**
En el notebook 02, los residuales del modelo sobre `saleprice` muestran heterocedasticidad
clara (forma de embudo). Modelar $\log(1+\text{precio})$ en vez del precio directo baja el MAE
y el MAPE en los cuatro cuartiles de precio — pero **sube el RMSE global**, porque una sola
vivienda atípica (grande, calidad máxima, vendida muy por debajo de lo esperado) produce un
error de más de 700 mil dólares al revertir la transformación logarítmica. Conclusión que se
dejó explícita para la sesión 8: RMSE y MAE pueden discrepar sobre cuál modelo es mejor, y
elegir la métrica es una decisión, no un trámite.

**Verificación realizada:** el código de ambos notebooks (extraído del `.py` intermedio en
formato percent) se ejecutó de punta a punta sin errores con el entorno conda `ML`
(Python 3.9; `ml-curso` aún no está creado, igual que en la fase 2).

**Ejercicios y quiz del módulo 3 quedan pendientes hasta cerrar S7 y S8** — se construyen al
final de la fase, no por sesión, igual que en los módulos 1 y 2.

⬜ **S7 — Multicolinealidad y regularización (siguiente).** ⬜ **S8 — Evaluación y selección
de modelos.**

---

## 4. Qué sigue — Fase 3, sesión 7 (Multicolinealidad y regularización)

Producir en `modulo-3-regresion-evaluacion/`:

- **Teoría:** `03-multicolinealidad-polinomica.md` · `04-regularizacion.md`.
- **Notebooks:** `03-regularizacion-intuicion` · `04-regularizacion-aplicado`.
- Reusar `ames-housing.csv` (ya preparado). El notebook 02 de S6 ya señaló candidatas a
  multicolinealidad: `gr_liv_area`, `total_bsmt_sf`, `garage_area`, `garage_cars` miden
  aspectos parecidos de "qué tan grande es la casa" — buen punto de partida para el VIF.

Puntos a cuidar:

- La sesión 8 (evaluación) es **nueva**, sin material previo. Es la que da las herramientas
  que los módulos 1 y 2 ya prometieron: validación cruzada repetida e intervalos sobre la
  diferencia entre modelos. Varios notebooks anteriores terminan diciendo "esto se resuelve en
  la sesión 8": hay que cumplirlo.
- Optuna entra en la sesión 8 (venía de `Sesion11-Metodos_ensamble`), no en el módulo 4.

### Decisiones abiertas para consultar con el docente

1. **Dataset conductor de los módulos 4 y 5** — M2 usa Titanic, M3 usa Ames Housing (ambos
   confirmados por el docente). Candidatos pendientes: Wine Quality UCI (M4), Iris/Wine (M5).
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
| PDFs S1–S12 | Teoría de los 6 módulos | Reescribir como texto con LaTeX | parcial (M1 hecho) |
| `Sesion03-Limpieza de datos` (Titanic) | M2/S4 | Reusar dataset; reescribir con EDA más fuerte | ✅ hecho |
| `Sesion03-webscraping` (BeautifulSoup) | M2/S4 🔵 | Reusar; fijar la fuente para que no se rompa | ✅ hecho (fixture local) |
| `Sesion04-PCA*` ×3, `Sesion04-TSNE*` ×2 | M5/S12 | Consolidar 5 → 2 (intuición + aplicado) | pendiente |
| `Sesion05-Ingenieria_caracteristicas` (NYC Taxi) | M2/S5 | Reescrito sobre `Pipeline`/`ColumnTransformer`; se usó Titanic en vez de NYC Taxi para mantener un solo dataset conductor | ✅ hecho |
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 | ✅ hecho |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida | pendiente |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidar 7 → 2; Wine Quality como caso canónico | pendiente |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividir: CV y GridSearch suben a S8 | pendiente |
| `Sesion10-Clustering` | M5/S12 | Base reutilizable; añadir comparación de algoritmos | pendiente |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidar 4 → 2; Optuna pasa a S8 | pendiente |
| *(no existía)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** | M1 hecho |

El módulo 1 no reutilizó ningún notebook previo: no existían para S1 ni S2, y los de S4 sobre
PCA/t-SNE se movieron al módulo 5. El módulo 2 reutilizó el **dataset** de `Sesion03` y la idea
del scraping, pero reescribió por completo el contenido.

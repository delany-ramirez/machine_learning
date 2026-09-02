# PLAN — Bitácora de construcción del curso

Este archivo es la **memoria del proyecto entre sesiones de trabajo**. Al retomar el trabajo,
léelo primero: dice qué está hecho, qué sigue y qué decisiones ya se tomaron.

**Última actualización:** 2026-09-02 · **Fase actual:** 2 completada, sigue la Fase 3.

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
| 3 | **Módulo 3** — Regresión y evaluación (S6–S8) | ⬜ pendiente | |
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

---

## 4. Qué sigue — Fase 3 (Módulo 3: Regresión y evaluación)

Producir en `modulo-3-regresion-evaluacion/`:

- **Teoría:** `01-regresion-lineal.md` · `02-descenso-gradiente.md` ·
  `03-multicolinealidad-polinomica.md` · `04-regularizacion.md` ·
  `05-sesgo-varianza-validacion.md` · `06-seleccion-hiperparametros.md`.
- **Notebooks:** `01-descenso-gradiente-intuicion` · `02-regresion-multiple-aplicado` ·
  `03-regularizacion-intuicion` · `04-regularizacion-aplicado` ·
  `05-sesgo-varianza-intuicion` · `06-seleccion-modelos-aplicado`.
- **Datos:** dataset conductor. Candidato heredado: **Ames Housing** (lo usaba
  `Sesion07-ames_regresion_ml`). Verificar tamaño: si supera 1 MB, va con script de descarga.
- **Ejercicios:** 3 con solución. **Quiz:** 10 preguntas.

Puntos a cuidar:

- El módulo 1 ya implementó el descenso del gradiente a mano
  (`04-gradientes-intuicion.ipynb`). El notebook `01` de este módulo debe **partir de ahí**,
  no repetirlo: extenderlo a múltiples variables, variantes (batch/mini-batch/SGD) y
  diagnóstico de convergencia.
- La sesión 8 (evaluación) es **nueva**, sin material previo. Es la que da las herramientas
  que los módulos 1 y 2 ya prometieron: validación cruzada repetida e intervalos sobre la
  diferencia entre modelos. Varios notebooks anteriores terminan diciendo "esto se resuelve en
  la sesión 8": hay que cumplirlo.
- Optuna entra aquí (venía de `Sesion11-Metodos_ensamble`), no en el módulo 4.

### Decisiones abiertas para consultar con el docente

1. **Dataset conductor de los módulos 3 a 5** — M2 ya usa Titanic (confirmado por el
   docente). Candidatos pendientes: Ames Housing (M3), Wine Quality UCI (M4), Iris/Wine (M5).
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
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 | pendiente |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida | pendiente |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidar 7 → 2; Wine Quality como caso canónico | pendiente |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividir: CV y GridSearch suben a S8 | pendiente |
| `Sesion10-Clustering` | M5/S12 | Base reutilizable; añadir comparación de algoritmos | pendiente |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidar 4 → 2; Optuna pasa a S8 | pendiente |
| *(no existía)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** | M1 hecho |

El módulo 1 no reutilizó ningún notebook previo: no existían para S1 ni S2, y los de S4 sobre
PCA/t-SNE se movieron al módulo 5. El módulo 2 reutilizó el **dataset** de `Sesion03` y la idea
del scraping, pero reescribió por completo el contenido.

# PLAN — Bitácora de construcción del curso

Este archivo es la **memoria del proyecto entre sesiones de trabajo**. Al retomar el trabajo,
léelo primero: dice qué está hecho, qué sigue y qué decisiones ya se tomaron.

**Última actualización:** 2026-09-02 · **Fase actual:** 1 completada, sigue la Fase 2.

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
| 1 | **Módulo 1** — Fundamentos y ciclo de vida (S1–S3) | ✅ hecha | |
| 2 | **Módulo 2** — Datos y características (S4–S5) | ⬜ pendiente | |
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

---

## 4. Qué sigue — Fase 2 (Módulo 2: Datos y características)

Producir en `modulo-2-datos-caracteristicas/`:

- **Teoría:** `01-recoleccion-datos.md` · `02-limpieza-y-calidad.md` ·
  `03-analisis-exploratorio.md` · `04-ingenieria-caracteristicas.md` ·
  `05-seleccion-y-pipelines.md`.
- **Notebooks:** `01-limpieza-eda-aplicado` · `02-webscraping-aplicado` 🔵 ·
  `03-fuga-de-datos-intuicion` · `04-pipeline-caracteristicas-aplicado`.
- **Datos:** elegir el dataset conductor. Candidato heredado: **Titanic** (lo usaba
  `Sesion03-Limpieza de datos`), que tiene nulos, categóricas y outliers reales. Incluirlo
  como CSV versionado (< 1 MB) o con un script de descarga.
- **Ejercicios:** 2 con solución. **Quiz:** 10 preguntas.

Puntos a cuidar en esta fase:

- El notebook `03-fuga-de-datos-intuicion` es el que más valor añade frente a la edición
  anterior: debe **medir** el sobreoptimismo de escalar antes de partir los datos, no solo
  describirlo.
- La ingeniería de características debe reescribirse alrededor de `Pipeline` y
  `ColumnTransformer`, no como pasos sueltos (que es como estaba en `Sesion05`).

### Decisiones abiertas para consultar con el docente

1. **Dataset conductor de los módulos 2 a 5** — candidatos heredados: Titanic (M2), Ames
   Housing (M3), Wine Quality UCI (M4), Iris/Wine (M5). Falta confirmarlos.
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
| `Sesion03-Limpieza de datos` (Titanic) | M2/S4 | Reusar dataset; reescribir con EDA más fuerte | pendiente |
| `Sesion03-webscraping` (BeautifulSoup) | M2/S4 🔵 | Reusar; fijar la fuente para que no se rompa | pendiente |
| `Sesion04-PCA*` ×3, `Sesion04-TSNE*` ×2 | M5/S12 | Consolidar 5 → 2 (intuición + aplicado) | pendiente |
| `Sesion05-Ingenieria_caracteristicas` (NYC Taxi) | M2/S5 | Reescribir sobre `Pipeline`/`ColumnTransformer` | pendiente |
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 | pendiente |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida | pendiente |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidar 7 → 2; Wine Quality como caso canónico | pendiente |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividir: CV y GridSearch suben a S8 | pendiente |
| `Sesion10-Clustering` | M5/S12 | Base reutilizable; añadir comparación de algoritmos | pendiente |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidar 4 → 2; Optuna pasa a S8 | pendiente |
| *(no existía)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** | M1 hecho |

El módulo 1 no reutilizó ningún notebook previo: no existían para S1 ni S2, y los de S4 sobre
PCA/t-SNE se movieron al módulo 5.

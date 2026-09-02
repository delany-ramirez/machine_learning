# PLAN — Bitácora de construcción del curso

Este archivo es la **memoria del proyecto entre sesiones de trabajo**. Al retomar el trabajo,
léelo primero: dice qué está hecho, qué sigue y qué decisiones ya se tomaron.

**Última actualización:** 2026-09-02 · **Fase actual:** 0 completada, sigue la Fase 1.

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
| 0 | Estructura del repo, README, docs (programa, convenciones, entorno), entorno, licencia, READMEs índice de los 6 módulos | ✅ hecha | — |
| 1 | **Módulo 1** — Fundamentos y ciclo de vida (S1–S3) | ⬜ pendiente | |
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
- `environment.yml` (conda, entorno `ml`) y `requirements.txt` (pip).
- `.gitignore` (excluye `contenido_anterior/`, `mlruns/`, datos pesados) y `LICENSE`
  (CC BY 4.0 + MIT).
- README índice de cada uno de los 6 módulos, con el contenido planeado marcado como
  pendiente.

---

## 4. Qué sigue — Fase 1 (Módulo 1)

Al retomar, producir en `modulo-1-fundamentos-ciclo-vida/`:

- **Teoría** (`teoria/`):
  - `01-que-es-machine-learning.md` — definición, IA/ML/DL, tipos de aprendizaje, taxonomía
    de problemas, cuándo NO usar ML.
  - `02-ciclo-de-vida.md` — las 7 etapas, definición del problema, métricas de negocio vs.
    técnicas.
  - `03-versionado-codigo-datos.md` — Git y DVC aplicados a proyectos de ML.
  - `04-algebra-lineal.md` — vectores, matrices, normas, distancias, eigen y SVD.
  - `05-calculo-y-probabilidad.md` — derivadas, gradientes, regla de la cadena,
    distribuciones, Bayes.
- **Notebooks** (`notebooks/`):
  - `01-primer-modelo-aplicado.ipynb` — flujo `fit`/`predict` completo y mínimo, para que en
    la primera sesión ya vean un modelo funcionando de punta a punta.
  - `02-proyecto-reproducible-aplicado.ipynb` — estructura de proyecto, semillas, DVC.
  - `03-algebra-lineal-intuicion.ipynb` — NumPy desde cero, SVD a mano.
  - `04-gradientes-intuicion.ipynb` — derivadas numéricas y descenso, preparando S6.
- **Datos** (`datos/`): dataset conductor del módulo, pequeño y versionable.
- **Ejercicios** (`ejercicios/`): 2 ejercicios con solución.
- **Quiz** (`quiz/`): `quiz-modulo-1.md` + `quiz-modulo-1-sol.md`, 8–12 preguntas.

### Decisiones abiertas para consultar con el docente

1. **Dataset conductor de cada módulo** — falta elegirlos. Candidatos heredados de la edición
   anterior: Titanic (M2), Ames Housing (M3), Wine Quality UCI (M4), Iris/Wine (M5).
2. **Tema del proyecto integrador** — propuesta: predicción de deserción estudiantil con
   dataset sintético realista (nulos, categóricas, desbalance y una fuga de datos plantada a
   propósito). Alternativa: reutilizar el enunciado del trabajo final de la edición anterior
   si el docente lo aporta.
3. **Pesos de evaluación** — los de `docs/programa.md` (60/25/15) son una sugerencia; ajustar
   al reglamento del programa.
4. **Talleres** — la evaluación acordada fue proyecto + quiz, y las entregas parciales del
   proyecto hacen las veces de taller por módulo. Si se prefieren talleres independientes,
   hay que añadirlos a la estructura de cada módulo.

---

## 5. Mapa del material previo → módulos

Referencia para saber qué insumo existe al construir cada módulo. Todo está en
`contenido_anterior/` (no versionado).

| Material previo | Destino | Acción |
|---|---|---|
| PDFs S1–S12 | Teoría de los 6 módulos | Reescribir como texto con LaTeX |
| `Sesion03-Limpieza de datos` (Titanic) | M2/S4 | Reusar dataset; reescribir con EDA más fuerte |
| `Sesion03-webscraping` (BeautifulSoup) | M2/S4 🔵 | Reusar; fijar la fuente para que no se rompa |
| `Sesion04-PCA*` ×3, `Sesion04-TSNE*` ×2 | M5/S12 | Consolidar 5 → 2 (intuición + aplicado) |
| `Sesion05-Ingenieria_caracteristicas` (NYC Taxi) | M2/S5 | Reescribir sobre `Pipeline`/`ColumnTransformer` |
| `Sesion06-Regresion*` ×4 | M3/S6 | Consolidar 4 → 2 |
| `Sesion07-*` ×5 (Ridge, Lasso, ElasticNet, Ames) | M3/S7 | Consolidar 5 → 2; sacar la rúbrica embebida |
| `Sesion08-*` ×7 (LogReg, KNN, SVM, Wine) | M4/S9 | Consolidar 7 → 2; Wine Quality como caso canónico |
| `Sesion09-Clasificacion2` | M4/S10 + M3/S8 | Dividir: CV y GridSearch suben a S8 |
| `Sesion10-Clustering` | M5/S12 | Base reutilizable; añadir comparación de algoritmos |
| `Sesion11-*` ×3 + `03-SHAP_LightGBM` | M4/S11 | Consolidar 4 → 2; Optuna pasa a S8 |
| *(no existe)* | M1/S1, M1/S2, M5/S13, M6/S14 | Contenido **nuevo** |

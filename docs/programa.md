# Programa del curso — Machine Learning

> **Fuente de verdad del curso.** La numeración de sesiones, módulos y contenidos de este
> documento manda sobre cualquier otro archivo del repositorio. Si un README de módulo o un
> notebook contradice esta tabla, se corrige el otro archivo, no este.

## Ficha

| Campo | Valor |
|---|---|
| Programa | Maestría en Ingeniería de Sistemas y Computación |
| Institución | Universidad Tecnológica de Pereira |
| Docente | MSc. Délany Ramírez del Río — `delram@utp.edu.co` |
| Intensidad | **48 horas** — 14 sesiones de 3.5 h |
| Distribución | 2 sesiones por semana durante 7 semanas |
| Modalidad de trabajo | Teoría en `.md` + notebooks Python ejecutables |
| Lenguaje | Python 3.11 (scikit-learn, PyTorch, MLflow, FastAPI) |
| Evaluación | Proyecto integrador transversal + quiz teórico por módulo |

## Objetivo general

Que el estudiante sea capaz de **formular, construir, evaluar y desplegar** soluciones de
Machine Learning sobre datos reales, comprendiendo los fundamentos matemáticos de los
algoritmos, eligiendo el modelo adecuado con criterio y llevando el resultado hasta un
servicio consumible y trazable.

## Objetivos específicos

1. Distinguir los tipos de aprendizaje y encuadrar un problema real como una tarea de ML.
2. Aplicar el ciclo de vida completo de un proyecto de ML con control de versiones de código
   y datos.
3. Preparar datos: recolección, limpieza, análisis exploratorio e ingeniería de
   características, evitando la fuga de datos (data leakage).
4. Implementar y diagnosticar modelos de regresión y clasificación, desde la formulación
   matemática hasta la evaluación honesta.
5. Seleccionar modelos con validación cruzada y optimización de hiperparámetros.
6. Aplicar métodos de ensamble e interpretar sus predicciones.
7. Descubrir estructura con métodos no supervisados y reducción de dimensionalidad.
8. Comprender los fundamentos del deep learning como puente al curso especializado.
9. Desplegar un modelo como API, con trazabilidad de experimentos y monitoreo.

## Malla — 6 módulos, 14 sesiones

| Módulo | Sesiones | Horas | Carpeta |
|---|---|---|---|
| 1. Fundamentos y ciclo de vida | S1–S3 | 10.5 | [`modulo-1-fundamentos-ciclo-vida/`](../modulo-1-fundamentos-ciclo-vida/) |
| 2. Datos: preprocesamiento e ingeniería de características | S4–S5 | 7.0 | [`modulo-2-datos-caracteristicas/`](../modulo-2-datos-caracteristicas/) |
| 3. Supervisado I: regresión y evaluación | S6–S8 | 10.5 | [`modulo-3-regresion-evaluacion/`](../modulo-3-regresion-evaluacion/) |
| 4. Supervisado II: clasificación y ensambles | S9–S11 | 10.5 | [`modulo-4-clasificacion-ensambles/`](../modulo-4-clasificacion-ensambles/) |
| 5. No supervisado y deep learning | S12–S13 | 7.0 | [`modulo-5-no-supervisado-deep-learning/`](../modulo-5-no-supervisado-deep-learning/) |
| 6. MLOps: trazabilidad y despliegue | S14 | 3.5 | [`modulo-6-mlops-despliegue/`](../modulo-6-mlops-despliegue/) |
| | **14** | **49** | |

## Detalle por sesión

### Módulo 1 — Fundamentos y ciclo de vida

| Sesión | Tema | Contenidos |
|---|---|---|
| **S1** | Introducción al Machine Learning | Definición y alcance. IA vs. ML vs. DL. Tipos de aprendizaje: supervisado, no supervisado, por refuerzo. Taxonomía de problemas. Ecosistema Python. Entorno reproducible. Primer flujo `fit`/`predict` de punta a punta. |
| **S2** | Ciclo de vida de un proyecto de ML | Las 7 etapas del ciclo. Definición del problema: métricas de negocio vs. métricas técnicas. Estructura de un proyecto de ML. Control de versiones con **Git**. Versionado de datos con **DVC**. |
| **S3** | Fundamentos matemáticos | Álgebra lineal con NumPy: vectores, matrices, producto punto, normas y distancias. Descomposiciones (eigen, **SVD**). Cálculo: derivadas, gradientes, regla de la cadena. Probabilidad: distribuciones y teorema de Bayes. Conexión con los algoritmos del curso. |

### Módulo 2 — Datos: preprocesamiento e ingeniería de características

| Sesión | Tema | Contenidos |
|---|---|---|
| **S4** | Recolección, limpieza y EDA | Datos estructurados vs. no estructurados. Lectura desde CSV, SQL y API. 🔵 Web scraping con BeautifulSoup. Valores faltantes, duplicados y outliers. Análisis exploratorio y visualización. |
| **S5** | Ingeniería de características | Escalado y normalización. Codificación de variables categóricas. Transformaciones. Selección de características: filtro (`SelectKBest`), envoltura (RFE) y embebidos. **`Pipeline` y `ColumnTransformer`**. **Fuga de datos** (data leakage). |

### Módulo 3 — Supervisado I: regresión y evaluación

| Sesión | Tema | Contenidos |
|---|---|---|
| **S6** | Regresión lineal | Regresión simple y múltiple. Mínimos cuadrados ordinarios. **Descenso del gradiente** implementado a mano. Supuestos y análisis de residuales. Métricas: MSE, RMSE, MAE, $R^2$ y $R^2$ ajustado. |
| **S7** | Regresión avanzada | Multicolinealidad y **VIF**. Regresión polinómica. **Regularización**: Ridge ($L_2$), Lasso ($L_1$) y Elastic Net. Interpretación de coeficientes y selección implícita de variables. |
| **S8** | Evaluación y selección de modelos | Compromiso **sesgo-varianza**. Sobreajuste y subajuste. Validación cruzada: k-fold, estratificada y temporal. Curvas de aprendizaje y de validación. Búsqueda de hiperparámetros: grid, aleatoria y bayesiana (**Optuna**). Reproducibilidad. |

### Módulo 4 — Supervisado II: clasificación y ensambles

| Sesión | Tema | Contenidos |
|---|---|---|
| **S9** | Clasificación | Regresión logística: odds, log-odds, máxima verosimilitud y softmax multiclase. KNN. SVM y kernels. **Métricas**: matriz de confusión, accuracy, precisión, recall, F1, ROC-AUC y curva PR. Ajuste del umbral. **Clases desbalanceadas**. |
| **S10** | Árboles de decisión y bagging | Estructura de un árbol. Medidas de impureza: Gini y entropía. Profundidad, poda y sobreajuste. Bootstrap aggregating. **Random Forest**. Importancia de variables. |
| **S11** | Boosting e interpretabilidad | AdaBoost. Gradient Boosting. **XGBoost** y **LightGBM**. Stacking. Interpretabilidad: permutation importance y **SHAP**. |

### Módulo 5 — No supervisado y deep learning

| Sesión | Tema | Contenidos |
|---|---|---|
| **S12** | Aprendizaje no supervisado | Clustering: K-Means (y K-Means++), jerárquico aglomerativo (dendrograma), DBSCAN. Validación: método del codo, coeficiente de silueta, índice de Davies-Bouldin. **Reducción de dimensionalidad**: PCA, t-SNE, 🔵 UMAP. 🔵 Detección de anomalías. |
| **S13** | Deep learning (puente) | Perceptrón y perceptrón multicapa (**MLP**). Funciones de activación. **Retropropagación**. Entrenamiento en **PyTorch**: optimizadores, batches, early stopping, dropout. Cuándo *no* usar deep learning. 🔵 Vistazo a CNN y transfer learning. |

> **Nota.** Esta sesión es un **puente** hacia el curso especializado de Deep Learning del
> programa; no pretende cubrirlo, sino dar el fundamento y el criterio para decidir cuándo un
> problema tabular no necesita una red neuronal.

### Módulo 6 — MLOps: trazabilidad y despliegue

| Sesión | Tema | Contenidos |
|---|---|---|
| **S14** | De modelo a producto | **MLflow**: tracking, comparación de runs, model registry. Serialización y versionado del modelo. **API con FastAPI**: endpoints `/health` y `/predict`. Empaquetado con **Docker**. Monitoreo y **drift**. Reentrenamiento. Sustentación del proyecto integrador. |

## Evaluación

| Componente | Peso sugerido | Descripción |
|---|---|---|
| Proyecto integrador (6 entregas) | 60 % | Un caso único que crece módulo a módulo hasta desplegarse como API. Ver [`proyecto-integrador/`](../proyecto-integrador/). |
| Quizzes teóricos (6, uno por módulo) | 25 % | Preguntas conceptuales de cierre de módulo. Carpeta `quiz/` de cada módulo. |
| Ejercicios y participación | 15 % | Ejercicios guiados de cada módulo (`ejercicios/`). |

> Los pesos son una sugerencia; ajústalos al reglamento del programa antes de publicar el
> microcurrículo.

## Prerrequisitos

- Programación en Python a nivel intermedio (estructuras de datos, funciones, `pandas` básico).
- Estadística descriptiva e inferencial básica.
- Álgebra lineal y cálculo diferencial a nivel de pregrado en ingeniería.

> La sesión **S3** repasa los fundamentos matemáticos necesarios, pero no los enseña desde
> cero.

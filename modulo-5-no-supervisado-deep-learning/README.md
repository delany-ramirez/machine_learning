# Módulo 5 — No supervisado y deep learning (S12–S13, 7 h)

> Estado: **completo** (Fase 5 de [`../PLAN.md`](../PLAN.md)).

## Objetivos

Al finalizar el módulo, el estudiante será capaz de descubrir estructura en datos sin
etiquetas mediante clustering y reducción de dimensionalidad, **comprobar que esa
estructura existe** antes de interpretarla, y comprender los fundamentos de una red
neuronal —arquitectura, retropropagación y entrenamiento— con un criterio medido para
decidir cuándo un problema tabular no necesita deep learning.

## Contenidos

### ✅ Núcleo

- **S12** — Clustering particional: K-Means y K-Means++; sus supuestos (grupos convexos,
  esféricos, de tamaño parecido) y sus modos de fallo. Clustering jerárquico aglomerativo,
  *linkages* y dendrograma. Clustering por densidad: DBSCAN.
- **S12** — Validación de clusters: método del codo, coeficiente de silueta, índice de
  Davies-Bouldin; **referencia nula** y estabilidad para saber si hay grupos; ARI y NMI para
  validar contra etiquetas externas; interpretación en unidades originales.
- **S12** — Reducción de dimensionalidad: PCA desde la covarianza y la SVD (varianza
  explicada, cargas, scree plot, reconstrucción), cuándo no aporta y cuándo daña; t-SNE:
  qué conserva (vecindarios) y qué no (tamaños, distancias, existencia de grupos).
- **S13** — Perceptrón y perceptrón multicapa (MLP). Funciones de activación y
  desvanecimiento del gradiente.
- **S13** — Retropropagación: la regla de la cadena de S3 aplicada a una red, verificada
  contra diferencias finitas y contra el autograd de PyTorch.
- **S13** — Entrenamiento en PyTorch: optimizadores (SGD, momento, Adam), mini-lotes,
  early stopping, weight decay, dropout.
- **S13** — Cuándo *no* usar deep learning: comparación pareada contra los ensambles de
  S10–S11 sobre Wine Quality y Adult Census.

### 🔵 Opcional

- UMAP como alternativa a t-SNE con `transform` (notebook 04).
- Detección de anomalías: DBSCAN como filtro de ruido e Isolation Forest (notebook 02).
- Vistazo a redes convolucionales sobre los dígitos y por qué ganan en imágenes
  (notebook 06); transfer learning (teoría 05).

## Materiales

### Teoría

| # | Documento | Sesión | Tema |
|---|---|---|---|
| 01 | [`teoria/01-clustering.md`](teoria/01-clustering.md) | S12 | Aprender sin $y$; K-Means (Lloyd, K-Means++, supuestos, preprocesamiento); jerárquico y *linkages*; DBSCAN; cuál usar |
| 02 | [`teoria/02-validacion-clusters.md`](teoria/02-validacion-clusters.md) | S12 | Codo, silueta, Davies-Bouldin; referencia nula y estabilidad; ARI/NMI; interpretación; protocolo |
| 03 | [`teoria/03-reduccion-dimensionalidad.md`](teoria/03-reduccion-dimensionalidad.md) | S12 | PCA (derivación, SVD, reconstrucción, estandarizar, cuántos componentes, cargas, cuándo daña); t-SNE; 🔵 UMAP |
| 04 | [`teoria/04-redes-neuronales.md`](teoria/04-redes-neuronales.md) | S13 | Perceptrón, MLP, activaciones e inicialización, retropropagación, aproximación universal y lo que no dice |
| 05 | [`teoria/05-entrenamiento-y-limites.md`](teoria/05-entrenamiento-y-limites.md) | S13 | Bucle en PyTorch, optimizadores, tasa de aprendizaje, regularización, la fuga del early stopping, cuándo no usar DL, dónde sí |

### Notebooks

| # | Notebook | Sesión | Tipo | Contenido |
|---|---|---|---|---|
| 01 | [`notebooks/01-clustering-intuicion.ipynb`](notebooks/01-clustering-intuicion.ipynb) | S12 | intuición | K-Means (Lloyd) a mano y validado; inicialización y K-Means++ medidos; los supuestos de K-Means en datos que los violan; jerárquico y DBSCAN a mano validados contra SciPy y `scikit-learn`; codo y silueta a mano, y su trampa sobre datos sin grupos |
| 02 | [`notebooks/02-clustering-aplicado.ipynb`](notebooks/02-clustering-aplicado.ipynb) | S12 | aplicado | Wine Quality sin etiquetas: estandarizar, tres criterios y referencia nula, perfil e interpretación, validación contra `tipo` y `quality`, segundo nivel (dulces/secos), Ward y los otros *linkages*, DBSCAN e 🔵 Isolation Forest como detectores de anomalías, estabilidad |
| 03 | [`notebooks/03-pca-intuicion.ipynb`](notebooks/03-pca-intuicion.ipynb) | S12 | intuición | PCA por autovectores y por SVD, validado; estandarizar; scree, cargas y biplot sobre Wine; compresión de dígitos; cuando no aporta (estudiantes) y cuando daña (la clase en la dirección de poca varianza; la calidad del vino) |
| 04 | [`notebooks/04-reduccion-dimensionalidad-aplicado.ipynb`](notebooks/04-reduccion-dimensionalidad-aplicado.ipynb) | S12 | aplicado | PCA, t-SNE y 🔵 UMAP sobre los dígitos con *trustworthiness*, KNN y silueta; perplejidad e inicialización; lo que t-SNE no conserva, medido; grupos inventados; `transform` de UMAP; Wine en el mapa |
| 05 | [`notebooks/05-mlp-intuicion.ipynb`](notebooks/05-mlp-intuicion.ipynb) | S13 | intuición | Perceptrón y su límite; MLP en NumPy con retropropagación verificada por diferencias finitas y contra autograd; fronteras según la anchura; activaciones y desvanecimiento del gradiente medido en 10 capas; aproximación universal y sobreajuste |
| 06 | [`notebooks/06-mlp-pytorch-aplicado.ipynb`](notebooks/06-mlp-pytorch-aplicado.ipynb) | S13 | aplicado | Anatomía del entrenamiento en PyTorch; optimizadores y regularización medidos; comparación pareada MLP vs. logística / Extra-Trees / LightGBM sobre Wine y sobre Adult; 🔵 CNN sobre dígitos y robustez al desplazamiento; conjunto de prueba |

> **Hallazgo del notebook 01.** Codo y silueta proponen un $k$ igual de convencidos
> cuando hay cuatro grupos (silueta 0.77) que cuando no hay ninguno: sobre puntos
> uniformes, la silueta de K-Means tiene su máximo en $k = 4$ con valor 0.41. Los criterios
> internos comparan particiones; no comprueban que exista algo que particionar.
>
> **Hallazgo del notebook 02.** K-Means con $k = 2$ recupera tinto/blanco con ARI 0.93 sin
> haber visto `tipo`, y con ningún $k$ los grupos dicen nada de la calidad (NMI $\leq 0.07$):
> el clustering encuentra la estructura **dominante**, no la que interesa. La referencia
> nula (columnas permutadas: silueta 0.10 frente a 0.27) confirma que la estructura es real
> y la escala de Kaufman y Rousseeuw, que es débil. *Average*, *complete* y *single* cortan
> un solo vino atípico; y DBSCAN en 11 dimensiones no separa grupos completos (distancias
> concentradas), pero señala 191 vinos con alguna variable extrema — y coincide solo en un
> tercio con Isolation Forest: "anomalía" no tiene una definición única.
>
> **Hallazgo del notebook 03.** PCA no ve $y$: en un ejemplo construido, PC1 (91 % de la
> varianza) da accuracy 0.47 y PC2 (9 %) da 0.93. En Wine Quality, con los 11 componentes la
> AP de la logística es idéntica a la del modelo sin PCA (una rotación), y quitar
> componentes la baja de 0.52 a 0.40. Y sobre `rendimiento-estudiantes.csv`, cuyos
> predictores son independientes por construcción, el scree es plano: no hay nada que
> comprimir.
>
> **Hallazgo del notebook 04.** t-SNE conserva los vecindarios (*trustworthiness* 0.99;
> un KNN sobre dos coordenadas clasifica dígitos con 0.97) y nada más: un grupo 5× más
> disperso aparece del mismo tamaño, uno 3× más lejano a la misma distancia, y una sola
> gaussiana en 10D produce un mapa con grumos cuya silueta (0.35–0.38) cuadruplica la de
> los datos (0.08). Clusterizar el mapa funciona cuando los grupos existen (dígitos: ARI
> 0.89 frente a 0.67 en 64D) y engaña cuando no.
>
> **Hallazgo del notebook 05.** El gradiente a mano coincide con diferencias finitas y con
> el autograd de PyTorch a $10^{-10}$. En 10 capas con sigmoide, la primera recibe un
> gradiente $10^6$ veces menor que la última; con tanh y ReLU bien inicializadas, del mismo
> orden. Y un resultado que contradice la intuición de la S8: sobre 60 puntos del seno, la
> red de 100 neuronas ajusta la función verdadera **mejor** que la de 10 (ECM 0.011 frente
> a 0.079); el sobreajuste aparece con pocos datos y muchas épocas (lunas: la validación
> sube de 0.22 a 0.29), no automáticamente con el ancho.
>
> **Hallazgo del notebook 06.** Sobre Wine Quality, el MLP gana a la logística (+0.023 de
> AP), empata con LightGBM por defecto y pierde con Extra-Trees (−0.046 ± 0.004, cociente
> 10) costando 6× más; sobre Adult Census, con 10× más datos, LightGBM 0.83 frente a MLP
> 0.78 (−0.047 ± 0.001) a una décima del tiempo. Hacer el early stopping sobre el pliegue
> evaluado infla la AP 0.017 en Wine y 0.004 en Adult. Sobre los dígitos, la CNN es la mejor
> y la única que resiste un desplazamiento de un píxel (0.62 frente a 0.42–0.51): gana el
> modelo cuyo sesgo inductivo encaja con la estructura de los datos.

### Datos

**Dataset conductor del módulo:** `wine-quality.csv` (S12 y S13) · **Secundarios:**
`digits` de `scikit-learn` (S12, 🔵 S13), `adult-census.csv` (S13), `rendimiento-estudiantes.csv` (S12)

| Archivo | Descripción | Por qué este |
|---|---|---|
| [`datos/wine-quality.csv`](datos/wine-quality.csv) | Los mismos 6497 vinos del módulo 4 (5320 sin duplicados), 11 medidas fisicoquímicas, `tipo` y `quality`. Cortez et al. (2009), UCI, CC BY 4.0 | Sus 11 variables sí están correlacionadas (PCA tiene sentido); `tipo` es una etiqueta natural para validar clusters *a posteriori*; y la comparación MLP vs. ensambles se hace sobre números ya establecidos en el módulo 4 (AP 0.52 / 0.57 / 0.59) |
| [`datos/preparar-wine-quality.py`](datos/preparar-wine-quality.py) | Descarga y une los dos CSV de UCI (copiado del módulo 4) | Idempotente; documenta la procedencia |
| `digits` (`sklearn.datasets.load_digits`, sin archivo) | 1797 imágenes de 8 × 8 de dígitos manuscritos (64 píxeles, 0–16), 10 clases | Un caso con estructura de variedad (t-SNE luce), correlación entre variables (PCA comprime) e imágenes (la CNN tiene sentido), sin descarga |
| `datos/adult-census.csv` (**no versionado**, ~5 MB) | 48 842 personas, 14 variables, `ingreso_alto`; el dataset de los ejercicios del módulo 4 | La comparación MLP vs. LightGBM con 10× más datos y categóricas de alta cardinalidad, sobre la AP 0.83 ya conocida |
| [`datos/descargar-adult-census.py`](datos/descargar-adult-census.py) | Descarga y prepara Adult (copiado del módulo 4) | Se ejecuta una vez: `uv run datos/descargar-adult-census.py` |
| [`datos/rendimiento-estudiantes.csv`](datos/rendimiento-estudiantes.csv) | Dataset sintético de los módulos 1, 3 y 4 (400 estudiantes) | Predictores independientes por construcción: el caso en que PCA no aporta (notebook 03) y en que un MLP no puede ganar a un modelo lineal (ejercicio 03) |
| [`datos/generar-rendimiento-estudiantes.py`](datos/generar-rendimiento-estudiantes.py) | Generador con semilla fija | Reproducible byte a byte |

### Ejercicios

| # | Enunciado | Solución | Sesión | Duración |
|---|---|---|---|---|
| 01 | [`ejercicios/ej01-clustering.md`](ejercicios/ej01-clustering.md) | [`ej01-clustering-sol.md`](ejercicios/ej01-clustering-sol.md) | S12 | 75 min |
| 02 | [`ejercicios/ej02-pca-tsne.md`](ejercicios/ej02-pca-tsne.md) | [`ej02-pca-tsne-sol.md`](ejercicios/ej02-pca-tsne-sol.md) | S12 | 60 min |
| 03 | [`ejercicios/ej03-mlp.md`](ejercicios/ej03-mlp.md) | [`ej03-mlp-sol.md`](ejercicios/ej03-mlp-sol.md) | S13 | 75 min |

Los tres ejercicios usan datos que los notebooks **no** analizaron: el 01 repite el flujo
completo de clustering sobre los 1359 **tintos** y encuentra una estructura real pero muy
débil (silueta 0.205 frente a 0.09 de la referencia nula, solo $k = 2$ estable, Ward no
coincide con K-Means) que correlaciona con la calidad sin predecirla; el 02 valida PCA
con la métrica de un KNN sobre los **dígitos** (20 componentes de 64 bastan), mide qué
recupera K-Means sin etiquetas (el 8 no tiene grupo propio; el 1 tiene tres) y comprueba
que los subgrupos que t-SNE dibuja entre los "1" existen en los 64 píxeles (tres formas de
escribirlo); el 03 extiende la retropropagación a dos capas ocultas, mide que un MLP
**pierde** contra la regresión lineal sobre un proceso generador lineal (+0.015 ± 0.005 de
RMSE), y que en Adult una red más grande no acorta la distancia con LightGBM
(−0.049 ± 0.001).

### Quiz

| Archivo | Clave | Preguntas | Duración |
|---|---|---|---|
| [`quiz/quiz-modulo-5.md`](quiz/quiz-modulo-5.md) | [`quiz-modulo-5-sol.md`](quiz/quiz-modulo-5-sol.md) | 10 | 30 min |

## Entrega del proyecto integrador

**E5 — Exploración no supervisada.** Segmentación del caso con validación honesta —tres
criterios, referencia nula, estabilidad, perfil en unidades originales— y qué aporta (o
no) al problema original; o, como variante, un MLP comparado de forma pareada contra el
mejor ensamble de E4, con el early stopping sobre datos apartados del entrenamiento. Ver
[`../proyecto-integrador/`](../proyecto-integrador/).

---

> **Nota sobre el alcance de S13.** Esta sesión es un **puente** hacia el curso especializado
> de Deep Learning del programa. Da el fundamento (arquitectura, retropropagación,
> entrenamiento) y el criterio para decidir cuándo usarlo, no una cobertura completa del área.

> Los notebooks se ejecutan de principio a fin con el entorno de
> [`../pyproject.toml`](../pyproject.toml). Reglas de estilo en
> [`../docs/convenciones.md`](../docs/convenciones.md).

# 06 · Búsqueda de hiperparámetros y validación cruzada anidada

**Módulo 3 · Sesión 8** — Evaluación y selección de modelos

## Objetivos

- Comparar grid search, random search y optimización bayesiana (Optuna) como estrategias para
  recorrer un espacio de hiperparámetros.
- Entender por qué elegir el hiperparámetro y reportar el error de generalización sobre las
  mismas particiones produce una estimación optimista — y cómo lo evita la **validación
  cruzada anidada**.
- Fijar las semillas que hacen reproducible una búsqueda de hiperparámetros, no solo un ajuste.

## 1. El problema: un hiperparámetro no se aprende ajustando

$\lambda$ en Ridge/Lasso, el grado de un polinomio, el número de vecinos en KNN (módulo 4):
ninguno se puede elegir minimizando el error de entrenamiento —eso siempre favorece al modelo
más complejo posible, hasta el sobreajuste total—. Se eligen minimizando el error de
**validación**, y con validación cruzada repetida (`05-sesgo-varianza-validacion.md`) en vez
de un solo split, por la misma razón de siempre: un solo número es ruidoso.

## 2. Tres formas de recorrer el espacio de búsqueda

### Grid search (búsqueda exhaustiva)

Se define una rejilla de valores para cada hiperparámetro y se evalúan **todas** las
combinaciones. Exhaustivo y fácil de razonar, pero el costo crece exponencialmente con el
número de hiperparámetros: 10 valores para cada uno de 3 hiperparámetros son $10^3=1000$
ajustes, cada uno con su propia validación cruzada. Además, si un hiperparámetro no importa
mucho, grid search gasta el mismo esfuerzo explorándolo que en el que sí importa.

### Random search (búsqueda aleatoria)

En vez de una rejilla fija, se muestrean combinaciones al azar de una distribución para cada
hiperparámetro, con un número fijo de intentos. Sorprende la primera vez que se ve, pero es un
resultado establecido (Bergstra & Bengio, 2012): con presupuesto fijo, random search suele
encontrar una combinación igual de buena o mejor que grid search, porque no desperdicia
evaluaciones repitiendo el mismo valor de un hiperparámetro poco influyente mientras varía
apenas el que sí importa.

### Optimización bayesiana (Optuna)

Grid y random search tratan cada evaluación como independiente de las anteriores. La
optimización bayesiana no: construye un modelo probabilístico de "qué combinaciones
funcionan bien" a partir de las evaluaciones ya hechas, y lo usa para decidir dónde probar a
continuación — balanceando explorar zonas desconocidas y explotar las que ya lucen
prometedoras. `Optuna` implementa esto con un sampler llamado **TPE** (*Tree-structured Parzen
Estimator*). La ventaja aparece con presupuestos moderados y espacios de búsqueda grandes:
converge a buenas combinaciones con menos evaluaciones que random search, porque cada
evaluación informa a la siguiente.

| Método | Escala con # hiperparámetros | Usa el historial | Cuándo preferirlo |
|---|---|---|---|
| Grid search | Mal (exponencial) | No | Pocos hiperparámetros (1-2), rejilla ya intuida |
| Random search | Bien | No | Presupuesto fijo, varios hiperparámetros, sin intuición previa |
| Optuna (bayesiana) | Bien | Sí | Presupuesto ajustado, espacio grande, cada evaluación es costosa |

## 3. La fuga que nadie llama fuga: tunear y evaluar sobre las mismas particiones

`03-fuga-de-datos-intuicion.ipynb` (módulo 2) midió que la fuga más grave del curso era
**seleccionar características mirando los datos que después se usan para validar**. Elegir un
hiperparámetro es estructuralmente el mismo problema: si $\lambda$ se elige por el error de
validación cruzada más bajo, y **ese mismo error de validación cruzada** se reporta como el
desempeño esperado del modelo, se está reportando el mejor resultado de una búsqueda —
optimista casi por definición, aunque no haya habido ninguna fuga de variables.

La **validación cruzada anidada** (*nested cross-validation*) separa las dos preguntas:

- **Bucle interno**: sobre cada partición de entrenamiento del bucle externo, hace su propia
  validación cruzada para elegir el mejor hiperparámetro.
- **Bucle externo**: evalúa el modelo —ya con su hiperparámetro elegido— sobre un pliegue que
  el bucle interno **nunca vio**, ni para entrenar ni para elegir $\lambda$.

$$
\underbrace{\text{CV externo}}_{\text{estima el error de generalización}}
\left(\underbrace{\text{CV interno}}_{\text{elige el hiperparámetro}}\right)
$$

El costo es computacional: si el bucle externo tiene 5 pliegues y el interno otros 5, el
modelo se entrena $5 \times 5 \times (\text{tamaño de la rejilla})$ veces. Se paga esa factura
cuando lo que importa es reportar un número de desempeño defendible (el proyecto integrador,
un artículo, una decisión de negocio). Para simplemente elegir el mejor $\lambda$ y seguir
iterando, un solo nivel de CV basta.

## 4. Reproducibilidad de la búsqueda

`02-proyecto-reproducible-aplicado.ipynb` (módulo 1) fijó la semilla del modelo. Una búsqueda
de hiperparámetros tiene **dos** fuentes adicionales de aleatoriedad que también hay que
fijar:

- El particionado de la validación cruzada (`random_state` de `KFold`/`StratifiedKFold`):
  sin fijarlo, dos ejecuciones de la misma búsqueda pueden elegir hiperparámetros distintos.
- El muestreador de `Optuna` (`sampler=TPESampler(seed=SEMILLA)`): sin semilla, la secuencia
  de combinaciones probadas cambia entre ejecuciones, y con ella el resultado final de la
  búsqueda.

## Resumen

| Método | Idea | Dónde reaparece |
|---|---|---|
| Random search | Mejor que grid con presupuesto fijo | Módulo 4 (SVM, ensambles) |
| Optuna / TPE | Usa el historial para decidir dónde buscar | Módulos 4 y 5 |
| CV anidada | Separa "elegir el hiperparámetro" de "reportar el desempeño" | Proyecto integrador, cualquier número que se vaya a defender |
| Semillas de la búsqueda | Reproducibilidad va más allá de `random_state` del modelo | `02-proyecto-reproducible-aplicado.ipynb` (módulo 1) |

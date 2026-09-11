# 03 · Métricas de clasificación, umbral y clases desbalanceadas

**Módulo 4 · Sesión 9** — Clasificación

## Objetivos

- Construir todas las métricas de clasificación binaria a partir de la matriz de confusión,
  y saber cuál responde a qué pregunta.
- Entender por qué la **accuracy engaña** con clases desbalanceadas, con números.
- Leer las curvas **ROC** y **precisión-recall**, y saber cuándo cada una es la adecuada.
- Separar dos decisiones que `predict` mezcla: qué tan bien **ordena** el modelo y dónde se
  corta con el **umbral**.
- Conocer las tres estrategias frente al desbalance —umbral, pesos, remuestreo— y qué gana
  realmente cada una.
- Extender las métricas a más de dos clases.

Este documento es el primer marco de evaluación nuevo desde `05-sesgo-varianza-validacion.md`:
la validación cruzada, la comparación pareada y la CV anidada del módulo 3 siguen valiendo
tal cual; lo que cambia es **qué número** se calcula en cada pliegue.

## 1. La matriz de confusión

Con un objetivo binario y una predicción binaria, solo hay cuatro resultados posibles:

| | Predicho positivo | Predicho negativo |
|---|---|---|
| **Real positivo** | Verdadero positivo (VP) | Falso negativo (FN) |
| **Real negativo** | Falso positivo (FP) | Verdadero negativo (VN) |

Todas las métricas de esta sección son cocientes entre estas cuatro celdas. Cuál conviene
depende de **qué error cuesta más**, y esa es una pregunta del dominio, no del modelo:

| Métrica | Fórmula | Pregunta que responde |
|---|---|---|
| Accuracy | $\dfrac{VP + VN}{n}$ | ¿Qué fracción de todo acerté? |
| Precisión | $\dfrac{VP}{VP + FP}$ | De los que declaré positivos, ¿cuántos lo son? |
| Recall (sensibilidad) | $\dfrac{VP}{VP + FN}$ | De los positivos reales, ¿cuántos encontré? |
| Especificidad | $\dfrac{VN}{VN + FP}$ | De los negativos reales, ¿cuántos dejé en paz? |
| $F_1$ | $\dfrac{2 \cdot P \cdot R}{P + R}$ | Media armónica de precisión y recall |
| $F_\beta$ | $\dfrac{(1+\beta^2) \cdot P \cdot R}{\beta^2 P + R}$ | $F_1$ con el recall pesando $\beta$ veces más |

Precisión y recall están en **tensión**: subir uno suele bajar el otro. Un detector de
fraude que marca todo como fraude tiene recall 1 y precisión igual a la prevalencia; uno que
solo marca los casos obvios tiene precisión alta y recall bajo. $F_1$ resume los dos en un
número, pero pesándolos por igual, lo que rara vez refleja los costos reales; por eso existe
$F_\beta$, y por eso lo más honesto es reportar ambos.

## 2. Por qué la accuracy engaña

Con un 19 % de positivos (Wine Quality, "buena" = calidad $\geq 7$), un modelo que predice
"no" para todos los vinos tiene **accuracy 0.81**. En `02-clasificacion-aplicado.ipynb`,
la logística, KNN y la SVM obtienen entre 0.82 y 0.84 — indistinguibles de la referencia
trivial— y una SVM lineal obtiene 0.81 sin predecir **ni un solo positivo**. La accuracy
mide sobre todo cuánto se acierta en la clase grande.

Los mismos tres modelos, mirados con la matriz de confusión, muestran una precisión de
≈0.6 y un recall de ≈0.3: se les escapan dos de cada tres vinos buenos. Ese es el número que
la accuracy escondía. Regla práctica: **si la prevalencia está lejos de 0.5, la accuracy no
es una métrica, es una distracción**; y en cualquier caso hay que compararla contra la
referencia trivial, no contra cero.

## 3. Del umbral a las curvas

`predict` devuelve la clase 1 cuando $\hat{p} \geq 0.5$. Ese 0.5 no lo eligió nadie. Toda
la tabla de la sección 1 depende de él; para ver cómo se comporta el modelo **para todos los
umbrales a la vez** se usan dos curvas.

### Curva ROC

Recorre el umbral de 1 a 0 y grafica la tasa de verdaderos positivos (recall) contra la
**tasa de falsos positivos** $FP / (FP + VN)$. Un clasificador aleatorio da la diagonal; uno
perfecto pasa por la esquina superior izquierda. El **área bajo la curva (AUC-ROC)** tiene
una interpretación exacta: es la probabilidad de que un positivo tomado al azar reciba una
puntuación mayor que un negativo al azar. Mide **qué tan bien ordena** el modelo, sin
referencia a ningún umbral.

### Curva precisión-recall

Grafica precisión contra recall para cada umbral. Su área (**average precision**, AP) tiene
como referencia aleatoria la **prevalencia** — 0.19 aquí — y no 0.5.

### Cuál usar

Las dos miran los mismos cuatro números, pero la ROC normaliza los falsos positivos por el
total de **negativos**, y la PR los compara con los **verdaderos positivos**. Con clases
desbalanceadas la diferencia es enorme. En Wine Quality (4256 vinos de entrenamiento, 807
buenos, 3449 no buenos): 900 falsos positivos mueven la tasa de falsos positivos apenas
a 0.26 —la ROC sigue pareciendo buena—, pero frente a los ≈650 verdaderos positivos que
hacen falta para un recall de 0.8, hunden la precisión a 0.4. Por eso en el notebook 02
los tres modelos tienen un AUC-ROC de 0.80–0.83, que "parece bien", y una AP de 0.50–0.53
sobre una referencia de 0.19, que muestra el problema real.

> **Regla.** Con prevalencia baja, reportar AP junto al AUC-ROC, y mirar la curva PR antes
> de prometer recall. El AUC-ROC sigue siendo útil para comparar modelos —es independiente
> de la prevalencia—; la AP es la que dice si el modelo sirve para el problema.

## 4. Elegir el umbral

El umbral es donde la **métrica de negocio entra en el modelo**. Tres formas de elegirlo,
de menos a más explícita:

1. **Maximizar $F_1$** (o $F_\beta$) sobre la curva umbral-vs-métrica. En el notebook 02,
   bajar el umbral de la logística de 0.5 a 0.27 sube el $F_1$ de 0.40 a 0.55 — recall de
   0.31 a 0.67, precisión de 0.59 a 0.47.
2. **Fijar un requisito** y optimizar el otro: "necesito recall $\geq 0.8$; ¿cuál es la
   mayor precisión posible?" (0.34–0.41 en Wine Quality).
3. **Minimizar el costo esperado** con costos explícitos por tipo de error:
   $\text{costo}(u) = c_{FP} \cdot FP(u) + c_{FN} \cdot FN(u)$. Con $c_{FN} = 3\,c_{FP}$, el
   umbral óptimo de los tres modelos del notebook cae entre 0.19 y 0.27, y usar 0.5 sale
   entre un 21 y un 32 % más caro.

Cualquiera de las tres exige **probabilidades honestas**: las de `cross_val_predict` sobre el
conjunto de entrenamiento (cada fila predicha por un modelo que no la vio), nunca las del
conjunto de prueba, que se reserva para reportar el resultado final con el umbral ya fijado.
Elegir el umbral sobre el test es la misma fuga de selección que `06-seleccion-modelos-aplicado.ipynb`
midió para $\lambda$.

## 5. Clases desbalanceadas: tres estrategias, medidas

| Estrategia | Qué hace | Qué cambia |
|---|---|---|
| **Mover el umbral** | Nada en el modelo; corta las probabilidades en otro punto | Solo la decisión |
| **Pesos de clase** (`class_weight="balanced"`) | Cada error en la minoritaria pesa $n / (K \cdot n_k)$ veces más en la pérdida | La función objetivo; en modelos lineales, casi solo el intercepto |
| **Remuestreo**: sub-muestreo de la mayoritaria, sobre-muestreo de la minoritaria, o **SMOTE** (positivos sintéticos interpolados entre vecinos) | Cambia la distribución de entrenamiento | El modelo; y los datos |

Lo que `02-clasificacion-aplicado.ipynb` mide sobre Wine Quality:

- En la **regresión logística**, pesos y SMOTE disparan el recall en 0.5 (de 0.31 a ≈0.78) y
  el $F_1$ en 0.5, pero **no cambian** AUC-ROC (0.83), AP (0.52) ni el mejor $F_1$ alcanzable
  moviendo el umbral (0.55). Equivalen a mover el umbral: reordenan poco o nada a los vinos.
  Si el umbral se va a elegir de todos modos, no aportan nada.
- En la **SVM**, los pesos sí producen un modelo distinto (cambian qué puntos son vectores
  de soporte), y las métricas **discrepan** sobre si es mejor: AUC-ROC sube de 0.80 a 0.83,
  AP baja de 0.53 a 0.51. Igual que RMSE y MAE en el módulo 3, dos métricas razonables pueden
  no estar de acuerdo.

La regla que sale de medir, en orden: **primero mover el umbral**; si no basta, pesos de
clase (gratis, sin datos inventados); remuestreo como último recurso. Y evaluar cualquiera de
ellas con AP o AUC — nunca con el $F_1$ en 0.5, que es la métrica que siempre "mejora" al
balancear y por eso es la que se cita.

Dos reglas de higiene:

- El remuestreo va **dentro** del pipeline, solo sobre los pliegues de entrenamiento. SMOTE
  antes de partir crea positivos sintéticos que caen en validación interpolados desde
  positivos de entrenamiento — fuga. `imblearn.pipeline.Pipeline` lo garantiza; el
  `Pipeline` de `scikit-learn` no admite remuestreadores.
- La validación cruzada debe ser **estratificada** (`StratifiedKFold`): con 19 % de
  positivos y 5 pliegues, sin estratificar un pliegue puede quedar con la mitad de los
  positivos que otro por azar.

## 6. Más de dos clases

Con $K$ clases, la matriz de confusión es $K \times K$ y precisión/recall/$F_1$ se calculan
**por clase** (cada una como "esta clase contra el resto"). Para resumirlas:

| Promedio | Cómo | Cuándo |
|---|---|---|
| **Macro** | Media simple de la métrica de cada clase | Todas las clases importan igual, sin importar su tamaño |
| **Ponderado** (*weighted*) | Media pesada por el número de ejemplos de cada clase | Refleja el desempeño global; vuelve a premiar la clase grande |
| **Micro** | Suma VP, FP, FN de todas las clases y calcula una sola vez | Coincide con la accuracy en multiclase |

Sobre las siete calidades de Wine Quality, softmax da accuracy 0.55, $F_1$ ponderado 0.52 y
**macro-$F_1$ 0.25** — el único de los tres que refleja que las clases 8 y 9 tienen recall
cero. La matriz de confusión añade lo que ningún promedio muestra: el 88 % de los errores
están a **un punto** de la calidad real. Cuando el objetivo es **ordinal**, softmax
desperdicia esa estructura; a veces la formulación correcta es binaria (como en el resto
del módulo) o de regresión (módulo 3), y esa decisión es anterior a la elección del modelo.

Las curvas ROC y PR se extienden a multiclase por *one-vs-rest* (una curva por clase) y se
promedian con las mismas convenciones macro/ponderado.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Matriz de confusión | Los cuatro números de los que sale todo | Cada modelo del módulo, y el proyecto |
| Accuracy vs. referencia trivial | Con desbalance, no distingue nada | — |
| Precisión / recall / $F_\beta$ | Cuál error cuesta más es una pregunta del dominio | Métrica de negocio del proyecto (S2) |
| AUC-ROC vs. AP | Ordenar bien vs. servir para el problema; con desbalance, AP | Comparación de ensambles (S10–S11) |
| Umbral | Se elige con probabilidades de CV, según costos | Endpoint `/predict` del módulo 6 debe exponerlo |
| Pesos / SMOTE | En modelos lineales, equivalen a mover el umbral | `scale_pos_weight` en XGBoost/LightGBM (S11) |
| Macro-$F_1$ | El promedio que no premia a la clase grande | — |

**Notebook:** `02-clasificacion-aplicado.ipynb`.

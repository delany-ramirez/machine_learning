# Quiz · Módulo 4 — Supervisado II: clasificación y ensambles

**Sesiones 9–11** · 10 preguntas · Tiempo sugerido: **30 min** · Sin material de consulta

> Responde de forma breve y justificada. Se evalúa el razonamiento, no la extensión.

---

**1.** Una regresión logística estima $\beta_{\text{horas}} = 0.7$ para las horas de estudio
semanales (sin estandarizar).

- a) ¿Cómo se interpreta $e^{0.7} \approx 2$? ¿Qué se duplica exactamente?
- b) Un compañero dice: "cada hora adicional sube la probabilidad de aprobar un 100 %". ¿Es
  correcto? Justifica con la forma de la sigmoide.

---

**2.** Explica por qué la entropía cruzada, y no el error cuadrático medio, es la función de
costo de la regresión logística. Menciona dos propiedades concretas.

---

**3.** Entrenas una regresión logística con `penalty=None` sobre un dataset pequeño y el
solucionador nunca converge; los coeficientes crecen sin parar. La accuracy en entrenamiento
es 1.0.

- a) ¿Qué está pasando con los datos?
- b) ¿Por qué `scikit-learn` regulariza por defecto, más allá del sobreajuste?

---

**4.** Un clasificador de fraude tiene accuracy 0.99 sobre un conjunto con 1 % de fraudes.

- a) ¿Qué accuracy tiene la referencia trivial? ¿Qué se puede concluir del modelo?
- b) Un compañero propone reportar AUC-ROC, que da 0.95, y concluye que el modelo "funciona
  muy bien". Explica por qué la curva precisión-recall puede contar una historia distinta,
  con la aritmética de los falsos positivos.

---

**5.** Tienes las probabilidades de validación cruzada de un modelo y una estructura de
costos en la que un falso negativo cuesta cuatro veces más que un falso positivo.

- a) Describe cómo eliges el umbral de decisión.
- b) ¿Por qué no debes elegirlo con el conjunto de prueba? ¿Qué fuga del módulo 3 es la
  misma?
- c) Un compañero prefiere `class_weight="balanced"` sobre una regresión logística en vez
  de mover el umbral. Con lo medido en el módulo, ¿qué cambia y qué no cambia con esa
  decisión?

---

**6.** En Wine Quality, KNN con $k=1$ obtenía un F1 de 0.66 con los datos originales y 0.47
tras eliminar 1177 filas idénticas; la regresión logística apenas cambiaba.

- a) Explica el mecanismo por el que los duplicados favorecen a KNN con $k=1$.
- b) En el Titanic (módulo 2) se decidió **no** eliminar las 107 filas idénticas. ¿Qué
  criterio permite decidir distinto en cada caso?

---

**7.** Sobre árboles de decisión:

- a) ¿Por qué los árboles crecen con Gini o entropía y no con el error de clasificación,
  que es la métrica que al final importa?
- b) Un árbol sin límite de profundidad alcanza accuracy 1.0 en entrenamiento. ¿Qué
  esperas en prueba, y qué dos formas hay de controlarlo?
- c) ¿Por qué un árbol no necesita variables estandarizadas, mientras que KNN, SVM y la
  logística regularizada sí?

---

**8.** Bagging y Random Forest.

- a) Bagging promedia árboles **sin podar**. Explica por qué, en términos de sesgo y
  varianza, y por qué "más árboles" nunca empeora.
- b) ¿Qué añade Random Forest sobre bagging y qué término de la varianza del promedio
  ataca?
- c) En el módulo se midieron dos casos: uno en que Random Forest **no** superó a bagging
  (2 variables informativas de 20) y otro en que sí (Wine Quality, 12 variables). Explica
  la diferencia.

---

**9.** Boosting.

- a) ¿En qué se diferencia estructuralmente de bagging, y por qué **sí** sobreajusta con el
  número de árboles?
- b) En gradient boosting para clasificación, ¿a qué se ajusta cada árbol? Conecta con el
  gradiente de la regresión logística.
- c) Con valores por defecto, XGBoost y LightGBM no alcanzaron a Random Forest en Wine
  Quality, y en Adult Census le sacaron cinco puntos de AP. ¿Qué sugiere eso sobre cuándo
  conviene cada familia, y sobre "XGBoost gana siempre"?

---

**10.** Interpretabilidad. Un Random Forest reporta que una columna de números aleatorios
tiene más importancia por impureza (MDI) que tres variables reales.

- a) Explica el mecanismo.
- b) ¿Qué medida usarías en su lugar y qué punto ciego tiene esa medida con variables
  correlacionadas?
- c) SHAP dice que `alcohol` es la variable que más contribuye a que un vino se prediga como
  "bueno". ¿Qué **no** se puede concluir de eso, y por qué?

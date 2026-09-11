# Clave · Quiz Módulo 4 — Clasificación y ensambles

> **Material del docente.** Se indica lo mínimo exigible y, cuando aplica, el error típico que
> conviene comentar en la retroalimentación.

---

**1. Razón de momios**

**a)** $e^{\beta_j}$ es la **razón de momios** (*odds ratio*): por cada hora adicional de
estudio, los **momios** de aprobar ($p / (1-p)$) se multiplican por 2. Se duplican los
momios, no la probabilidad (`01-regresion-logistica.md`, sección 2).

**b)** **No.** El efecto sobre la probabilidad depende de dónde se esté en la sigmoide: de
$p = 0.5$ (momios 1) se pasa a momios 2, $p = 0.67$ (+17 puntos); de $p = 0.9$ (momios 9) a
momios 18, $p = 0.947$ (+5 puntos). El efecto es constante en log-momios, multiplicativo en
momios, y **variable** en probabilidad. Error típico: leer $\beta$ como pendiente sobre $p$.

---

**2. Entropía cruzada vs. MSE**

Dos propiedades (basta con dos, bien explicadas):

- Es la **negativa de la log-verosimilitud** de un modelo Bernoulli: minimizarla es hacer
  máxima verosimilitud, lo que le da fundamento estadístico.
- Es **convexa** en $\boldsymbol{\beta}$: un único mínimo que el descenso del gradiente
  encuentra siempre. El MSE aplicado tras la sigmoide **no** es convexo (se aplana lejos del
  óptimo; el notebook 01 lo grafica).
- **Castiga la confianza equivocada sin cota**: $-\log(0.001) \approx 6.9$; el MSE nunca
  cuesta más de 1 por observación.
- Su gradiente es $\mathbf{X}^\top(\hat{\mathbf{p}} - \mathbf{y})/n$, el mismo patrón de la
  regresión lineal — lo que permite reutilizar el mismo descenso.

---

**3. Separación perfecta**

**a)** Los datos son **linealmente separables** (accuracy 1.0 en entrenamiento es la pista).
Con separación perfecta, la entropía cruzada puede hacerse tan pequeña como se quiera
escalando $\boldsymbol{\beta}$: el estimador de máxima verosimilitud **no existe** (está "en
el infinito"), y el solucionador persigue un mínimo que no está (notebook 01, sección 7).

**b)** Porque la penalización $L_2$ **garantiza que exista una solución finita**, además de
proteger contra el sobreajuste. Con `penalty=None` sobre datos (casi) separables aparece la
advertencia de no convergencia y coeficientes enormes. Consecuencia práctica: los
coeficientes de una logística de `scikit-learn` están encogidos, y `C` es el inverso de
$\lambda$.

---

**4. Accuracy 0.99 con 1 % de fraudes**

**a)** La referencia trivial ("nada es fraude") tiene accuracy **0.99**. Del modelo no se
puede concluir **nada**: puede no haber detectado ni un solo fraude.

**b)** La ROC normaliza los falsos positivos por el total de **negativos** (99 % de los
datos), y la PR los compara con los **verdaderos positivos** (a lo sumo el 1 %). Con
10 000 casos y 100 fraudes: 500 falsos positivos son una tasa de falsos positivos de 0.05
—la ROC apenas se mueve— pero, frente a 80 fraudes detectados, una precisión de 0.14.
Un AUC-ROC de 0.95 es compatible con una precisión muy baja a cualquier recall útil; la
curva PR (y la AP, cuya referencia aleatoria es la prevalencia, 0.01) es la que muestra si
el modelo sirve (`03-metricas-clasificacion.md`, sección 3).

---

**5. Umbral con costos**

**a)** Para cada umbral candidato $u$, clasificar con $\hat{p} \geq u$, contar FP y FN sobre
las probabilidades de **validación cruzada**, calcular $\text{costo}(u) = FP + 4 \cdot FN$
y elegir el $u$ que lo minimiza. Con un falso negativo más caro, el umbral óptimo queda por
debajo de 0.5.

**b)** Porque el conjunto de prueba se reserva para reportar el resultado final con todas
las decisiones ya tomadas; elegir el umbral sobre él es usar el test para seleccionar, y su
número final quedaría optimista. Es la **fuga de selección** que
`06-seleccion-modelos-aplicado.ipynb` midió al elegir $\lambda$ y evaluar sobre los mismos
pliegues (CV anidada).

**c)** En una logística, `class_weight="balanced"` **sube el recall y el F1 en el umbral
0.5** —porque desplaza las probabilidades— pero **no cambia** AUC-ROC, AP ni el mejor F1
alcanzable moviendo el umbral: el orden de los casos es el mismo. Es mover el umbral con
otro nombre (notebook 02, sección 7; ejercicio 01, parte D). Si el umbral se va a elegir con
costos de todos modos, no aporta nada.

---

**6. Duplicados y KNN**

**a)** Si una fila aparece en entrenamiento y en validación, su vecino más cercano está a
distancia **cero** y KNN con $k=1$ acierta gratis. La fuga favorece sistemáticamente a los
modelos que **memorizan** (KNN con $k$ pequeño, árboles sin podar) sobre los que
generalizan (la logística, con frontera lineal, apenas cambia). No solo inflaba un número:
**elegía al modelo equivocado**.

**b)** La plausibilidad de que filas idénticas sean **observaciones distintas**. En el
Titanic, con pocas columnas de valores gruesos (clase, sexo, edad redondeada, tarifa), dos
pasajeros distintos con el mismo perfil son perfectamente posibles; en Wine Quality, 11
mediciones de laboratorio con decimales idénticos son casi con certeza el mismo vino
registrado varias veces. Y ante la duda, **medir**: si eliminar los duplicados cambia
drásticamente a un modelo que memoriza, había fuga.

---

**7. Árboles**

**a)** Gini y entropía son **estrictamente cóncavas**: una partición que lleva un nodo 50/50
a dos nodos 70/30 las reduce, pero **no** reduce el error de clasificación (lineal por
tramos). El árbol necesita una medida que premie el progreso parcial para poder crecer; se
evalúa después con la métrica que importa.

**b)** Peor accuracy en prueba que un árbol podado (en el notebook 03, 0.867 frente a 0.887;
en Wine Quality, AP 0.29 frente a 0.42): memoriza el ruido. Se controla con poda **a
priori** (`max_depth`, `min_samples_leaf`) o **a posteriori** por costo-complejidad
(`ccp_alpha`, que penaliza el número de hojas como Lasso penaliza coeficientes).

**c)** Cada partición compara **una** variable con un umbral, y el orden de los valores no
cambia con una transformación monótona: el árbol es invariante al escalado. KNN y SVM usan
**distancias** (dominadas por la variable de mayor escala) y la logística regularizada
penaliza $\|\boldsymbol{\beta}\|$, que depende de las unidades.

---

**8. Bagging y Random Forest**

**a)** Bagging reduce la **varianza** y no toca el **sesgo**: el promedio de árboles
profundos es tan flexible como cada uno, pero mucho más estable. Por eso conviene usar
árboles de sesgo mínimo (sin podar) y dejar que el promedio se ocupe de la varianza. Más
árboles solo acercan el promedio a su límite —nunca lo empeoran—; el costo es tiempo.

**b)** En cada nodo, busca la mejor partición entre un **subconjunto aleatorio** de
`max_features` variables. La varianza de un promedio de $B$ árboles con correlación $\rho$
es $\rho\sigma^2 + (1-\rho)\sigma^2/B$; $B$ solo elimina el segundo término, y Random Forest
ataca el primero, $\rho$, haciendo los árboles menos parecidos.

**c)** Decorrelacionar ayuda si los árboles siguen viendo la señal. Con 2 variables útiles
de 20 y `max_features=4`, el 63 % de los nodos no recibe **ninguna** variable útil y parte
por ruido: árboles peores sin ser mejor promedio. Con 12 variables que casi todas llevan
señal, restringir la elección diversifica sin cegar. `max_features` se afina; no es una
mejora automática (`04-arboles-y-bagging.md`, sección 5).

---

**9. Boosting**

**a)** Bagging entrena árboles **independientes** en paralelo y los promedia; boosting los
entrena **en secuencia**, cada uno ajustado a lo que los anteriores dejaron sin explicar.
Como cada árbol nuevo sigue reduciendo el error de entrenamiento, pasado cierto punto
ajusta **ruido**: el error de prueba tiene un mínimo y luego sube (notebook 05, ronda 45).
El número de rondas es un hiperparámetro de complejidad, y se elige por early stopping.

**b)** Al **gradiente negativo de la pérdida** respecto a la predicción actual. Con entropía
cruzada y $F$ en log-momios, ese gradiente es $y - \hat{p}$: el mismo residual que aparece en
$\mathbf{X}^\top(\hat{\mathbf{p}} - \mathbf{y})$ en la regresión logística. Boosting para
clasificación es una logística donde los árboles hacen el papel de
$\mathbf{X}\boldsymbol{\beta}$.

**c)** Boosting tiende a ganar con **muchos datos** y **variables heterogéneas** (Adult:
39 000 filas, categóricas de alta cardinalidad, numéricas sesgadas), y necesita afinarse;
los bosques funcionan casi sin afinar y pueden ganar en datasets pequeños y ruidosos
(Wine: 4 000 filas, techo de ruido alto). "XGBoost gana siempre" no es una ley: la única
forma de saberlo es medir con comparación pareada sobre los mismos pliegues.

---

**10. Interpretabilidad**

**a)** La MDI acumula la reducción de impureza de cada partición **sobre entrenamiento**.
Una variable continua ofrece miles de umbrales candidatos, y por puro azar alguno reduce la
impureza; con árboles sin podar esos cortes se usan. Premia la **cardinalidad**, no la
información (notebook 07: ruido continuo por encima de cuatro variables reales y 6× por
encima del ruido binario).

**b)** La **importancia por permutación** sobre un conjunto de validación: barajar una
columna y medir cuánto cae la métrica. No premia la cardinalidad (el ruido queda en cero).
Su punto ciego: con variables **casi redundantes**, barajar una deja la información en la
otra y la importancia se **reparte mal** (una copia de `alcohol` la baja de 0.104 a 0.017);
la lectura honesta es permutar por grupos.

**c)** Que **añadir alcohol mejore el vino** — ni ninguna afirmación causal. SHAP explica
**el modelo**: dice que el modelo usa `alcohol` para separar los vinos que los catadores
puntuaron alto, no por qué esos vinos gustan. El alcohol correlaciona con la madurez de la
uva, la región y la técnica; el modelo no distingue cuál actúa. Y una importancia alta
también puede ser la firma de una **fuga** (`alive` en el Titanic): la interpretabilidad
sirve para auditar, no para intervenir (`06-interpretabilidad.md`, sección 5).

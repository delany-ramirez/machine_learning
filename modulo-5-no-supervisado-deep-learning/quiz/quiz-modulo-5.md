# Quiz · Módulo 5 — No supervisado y deep learning

**Sesiones 12–13** · 10 preguntas · Tiempo sugerido: **30 min** · Sin material de consulta

> Responde de forma breve y justificada. Se evalúa el razonamiento, no la extensión.

---

**1.** Un compañero ejecuta K-Means con $k = 3$ sobre un dataset de clientes sin
estandarizar, donde `ingreso_anual` está en pesos (varianza $\sim 10^{14}$) y `edad` en
años. Obtiene tres grupos muy nítidos.

- a) ¿Qué encontró K-Means, casi con seguridad?
- b) ¿Qué habría que hacer antes, y por qué eso afecta también a DBSCAN y al jerárquico
  pero **no** a un árbol de decisión?

---

**2.** Explica por qué el algoritmo de Lloyd converge siempre, y por qué eso no garantiza
que el resultado sea bueno. ¿Qué dos medidas prácticas se toman contra el segundo
problema?

---

**3.** Sobre datos uniformes en un cuadrado —sin ningún grupo— la silueta de K-Means tiene
un máximo en $k = 4$ con valor 0.41.

- a) ¿Por qué el método del codo y la silueta proponen un $k$ aunque no haya grupos?
- b) Describe una forma de comprobar si la estructura encontrada en un dataset real es más
  que eso.

---

**4.** Sobre las 11 variables estandarizadas de Wine Quality, K-Means con $k = 2$ recupera
tinto/blanco con ARI 0.93, y con ningún $k$ la partición dice algo de la calidad
(NMI $\leq 0.07$). Un gerente concluye: "el clustering no funciona en estos datos".
Corrige la conclusión y explica qué encuentra un clustering y qué no.

---

**5.** Para cada situación, indica qué algoritmo de clustering usarías (K-Means, jerárquico
con algún *linkage*, DBSCAN) y **una** razón:

- a) Dos grupos con forma de media luna entrelazados.
- b) 200 000 clientes con variables numéricas, grupos aproximadamente convexos.
- c) Un dataset con puntos atípicos que se quieren identificar y apartar.
- d) 500 observaciones y se quiere explorar la jerarquía sin fijar $k$.

---

**6.** PCA sobre un dataset con dos clases da que PC1 explica el 91 % de la varianza y PC2
el 9 %. Una regresión logística sobre PC1 tiene accuracy 0.47; sobre PC2, 0.93.

- a) ¿Cómo es posible? ¿Qué supuesto implícito de "reducir a los componentes que explican
  el 90 %" falla?
- b) ¿Cómo se decide entonces cuántos componentes conservar antes de un modelo
  supervisado?

---

**7.** Un mapa t-SNE de un dataset muestra dos grupos: uno grande y difuso, otro pequeño y
compacto, muy separados entre sí. Di, para cada afirmación, si el mapa la respalda o no,
y por qué: (i) "hay dos grupos"; (ii) "el primer grupo es más disperso que el segundo";
(iii) "los dos grupos están muy lejos uno de otro"; (iv) "estos dos puntos, que están
juntos en el mapa, se parecen".

---

**8.** Explica por qué un MLP sin función de activación (o con activación lineal) es
equivalente a una regresión lineal por muchas capas que tenga, y qué hace la
retropropagación con la derivada de la activación en cada capa. A partir de eso, explica
por qué la sigmoide es una mala activación para capas ocultas en una red profunda.

---

**9.** En PyTorch, un compañero entrena un MLP durante 100 épocas fijas y reporta la AP
sobre el conjunto de validación de la última época. Otro entrena con *early stopping*
mirando ese mismo conjunto de validación y reporta la AP de la mejor época. Un tercero
hace early stopping sobre un 15 % apartado del entrenamiento y reporta sobre validación.
Ordena los tres reportes de más a menos optimista, y di cuál es el que se debe usar y
por qué.

---

**10.** Sobre Wine Quality y Adult Census, un MLP quedó por debajo de Extra-Trees y de
LightGBM (−0.046 y −0.047 de AP, con cocientes de 10 y 36), y sobre los dígitos una CNN
mínima fue la mejor y la más robusta a un desplazamiento de un píxel. Da la explicación
común a los dos resultados en términos de **sesgo inductivo**, y di qué comparación
exigirías antes de adoptar una red neuronal en un proyecto tabular.

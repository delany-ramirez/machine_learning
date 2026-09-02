# Clave · Quiz Módulo 1 — Fundamentos y ciclo de vida

> **Material del docente.** Se indica lo mínimo exigible para dar el punto completo y, cuando
> aplica, el error típico que conviene comentar en la retroalimentación.

---

**1. Definición $T$, $P$, $E$**

*Mínimo exigible:* las tres piezas identificadas de forma coherente entre sí, con $P$ medible.
Ejemplo válido: $T$ = predecir si un equipo fallará en las próximas 48 h; $P$ = recall sobre
fallas reales del histórico no usado en entrenamiento; $E$ = registros de sensores con fallas
etiquetadas de los últimos dos años.

*El contraste con programación tradicional:* allí una persona escribe las reglas ("si la
temperatura supera X y la vibración supera Y..."); en ML se aportan ejemplos etiquetados y el
algoritmo infiere las reglas. La dirección se invierte: **datos + respuestas → reglas**, en
lugar de **datos + reglas → respuestas**.

*Error típico:* proponer una $P$ no medible ("que funcione bien") o evaluada sobre los datos
de entrenamiento.

---

**2. Deep learning sobre 3.000 × 25**

Dos razones bastan, de entre estas:

- **Son datos tabulares**, donde los ensambles de árboles (Random Forest, XGBoost, LightGBM)
  suelen igualar o superar a las redes neuronales.
- **3.000 filas son pocas** para una red: el deep learning necesita gran volumen de datos para
  compensar su número de parámetros; con esa cantidad, el riesgo de sobreajuste es alto.
- **Costo y complejidad**: más cómputo, más hiperparámetros que ajustar y más tiempo de
  desarrollo para, probablemente, peor resultado.
- **Interpretabilidad**: un modelo de árboles se explica mucho mejor, y en muchos contextos
  eso es un requisito, no un lujo.

*Nota:* la respuesta correcta no es "el deep learning es malo", sino que **la elección se
justifica por el tipo y el volumen de datos**.

---

**3. Tipos de aprendizaje**

| | Respuesta |
|---|---|
| a) Tiempo hasta graduarse | Supervisado · **regresión** (valor continuo) |
| b) Agrupar artículos sin categorías | **No supervisado** (clustering) |
| c) Pieza defectuosa con 5.000 fotos etiquetadas | Supervisado · **clasificación binaria** |
| d) Decidir contenido para maximizar aprendizaje acumulado | **Por refuerzo** (decisiones secuenciales, recompensa diferida) |

*Error típico:* marcar (d) como supervisado. La clave está en que la recompensa es **diferida
y acumulada**, y que las decisiones afectan a los estados futuros.

---

**4. Separar antes de transformar**

*Mínimo exigible:* si se transforma antes de separar, la información del conjunto de prueba
entra en el proceso de entrenamiento y la evaluación deja de ser honesta. Es una forma de
**fuga de datos**.

*Ejemplo concreto (cualquiera de estos):*

- Estandarizar con la media y la desviación de **todo** el dataset: esas estadísticas
  contienen información de las filas de prueba, así que el modelo "ya sabe algo" de ellas.
- Imputar valores faltantes con la mediana global.
- Seleccionar características evaluando su correlación con el objetivo sobre el dataset
  completo.

*Consecuencia:* la métrica de prueba sale **optimista**, y el modelo rinde peor en producción
de lo prometido. Lo correcto es ajustar la transformación **solo** con el conjunto de
entrenamiento (`fit` en entrenamiento, `transform` en ambos), que es exactamente lo que
garantiza un `Pipeline`.

---

**5. Consultas de urgencias posteriores al alta**

**No es aceptable: es fuga de datos.** La variable se mide en la misma ventana temporal que se
quiere predecir (los 30 días posteriores al alta). En el momento real de la predicción —cuando
el paciente recibe el alta— ese dato **no existe todavía**.

Consecuencias: métricas excelentes en el experimento y modelo inservible en producción,
porque la variable no puede alimentarse.

*Regla que debe aparecer:* solo se admiten variables disponibles **en el momento de predecir**.

*Bonus:* si el estudiante añade que una métrica sospechosamente alta debe hacer sospechar de
fuga antes que celebrar, dar la respuesta por sobresaliente.

---

**6. 97 % de accuracy con prevalencia del 2 %**

**No es un buen modelo; probablemente es inútil.** Un clasificador trivial que responda
siempre "sano" acierta el **98 %**, así que el modelo con 97 % está *por debajo* de la
referencia trivial.

Con clases desbalanceadas la accuracy está dominada por la clase mayoritaria y no informa
sobre lo que interesa: detectar los casos raros.

*Qué reportar en su lugar:*

- Matriz de confusión completa.
- **Recall** de la clase positiva (¿cuántos enfermos detectamos?) y **precisión** (de los
  marcados, ¿cuántos lo estaban?).
- F1 o, mejor, la **curva precisión-recall** y su área; ROC-AUC es menos informativa con
  desbalance severo.
- Siempre, la comparación contra el clasificador trivial.

*Conexión:* es el mismo fenómeno del teorema de Bayes con clases raras visto en la teoría; se
retoma en la sesión 9.

---

**7. Predicción lineal como producto punto**

Para una observación: $\hat{y} = \beta_0 + \boldsymbol{\beta} \cdot \mathbf{x}$ — cada
variable se multiplica por su coeficiente y se suman los productos, que es la definición del
producto punto.

Para todo el conjunto:

$$
\hat{\mathbf{y}} = \beta_0\mathbf{1} + \mathbf{X}\boldsymbol{\beta}
$$

| Término | Nombre | Dimensiones |
|---|---|---|
| $\mathbf{X}$ | Matriz de diseño | $n \times p$ |
| $\boldsymbol{\beta}$ | Vector de coeficientes | $p \times 1$ |
| $\beta_0$ | Intercepto | escalar |
| $\hat{\mathbf{y}}$ | Vector de predicciones | $n \times 1$ |

*Se valora* que mencione la ventaja práctica: una sola operación matricial reemplaza un bucle
sobre $n$ filas y se ejecuta en código optimizado.

---

**8. Distancias con escalas dispares**

**a)** La distancia euclidiana suma diferencias al cuadrado. Como `asistencia_pct` varía en un
rango ~20 veces mayor que `promedio`, sus diferencias dominan la suma: la distancia es
prácticamente la distancia en asistencia, y el promedio académico casi no interviene. La
variable más informativa queda anulada por una cuestión de unidades.

**b)** **Estandarizar** antes de calcular distancias: $z = (x - \mu)/\sigma$, lo que deja todas
las variables en media 0 y desviación 1. (También se acepta normalización min-max, indicando
que es más sensible a outliers.) Importante: la media y la desviación se calculan **solo con
el conjunto de entrenamiento**.

**c)** Dos de: **KNN**, **SVM**, **K-Means**, **DBSCAN**, **PCA**, redes neuronales,
regresión regularizada (Ridge/Lasso, porque la penalización castiga por igual coeficientes de
escalas distintas).

---

**9. Descenso del gradiente**

**a)** El gradiente apunta en la dirección de **máximo ascenso** de la función. Como queremos
**minimizar** la pérdida, avanzamos en la dirección opuesta.

**b)**
- *Demasiado pequeña*: converge, pero muy lentamente; puede agotarse el presupuesto de
  iteraciones sin haber llegado (la curva de aprendizaje aún está bajando, sin meseta).
- *Demasiado grande*: cada paso se pasa de largo del mínimo. Puede oscilar sin converger o,
  si es lo bastante grande, **divergir** con la pérdida creciendo hasta desbordarse.

**c)** El primer sospechoso es la **tasa de aprendizaje demasiado alta**. Después
comprobaría, en este orden:

1. Si las variables están **estandarizadas** (escalas dispares provocan divergencia con tasas
   perfectamente razonables).
2. Si hay valores faltantes, infinitos o extremos en los datos de entrada.
3. Si hay una división por cero o un logaritmo de cero en la función de pérdida.
4. La inicialización de los parámetros.

---

**10. Git y DVC**

- **Git** versiona el **código** y todo archivo de texto pequeño: scripts, notebooks,
  configuración, `requirements.txt`, documentación. Está diseñado para hacer diff de texto.
- **DVC** versiona los **datos** (y otros artefactos binarios grandes). Guarda el archivo en
  un almacenamiento aparte y deja en Git un **puntero de texto con el hash**, que sí se
  versiona.

*Por qué no basta una sola:* Git no soporta archivos grandes ni binarios —el historial crece
sin control y no puede hacer diff—, pero sin versionar los datos un experimento no es
reproducible: el mismo código con otros datos da otro modelo. Con las dos juntas,
`git checkout` + `dvc checkout` reconstruyen el estado exacto de código y datos.

*Dos archivos que nunca van a un commit de Git* (dos de estos):

- Credenciales, tokens o contraseñas (quedan en el historial para siempre).
- Datasets grandes.
- Modelos entrenados (`.joblib`, `.pkl`).
- Entornos virtuales (`.venv/`), cachés (`__pycache__/`), salidas regenerables.

*Bonus:* mencionar que los notebooks deben commitearse **con las salidas limpias**.

---

## Distribución de puntos

| Pregunta | Puntos | Evalúa |
|---|---|---|
| 1 | 0.5 | Definición operativa de ML |
| 2 | 0.5 | Criterio para elegir familia de modelos |
| 3 | 0.5 | Tipos de aprendizaje |
| 4 | 0.5 | Fuga de datos por preprocesamiento |
| 5 | 0.5 | Fuga de datos temporal |
| 6 | 0.5 | Métricas con clases desbalanceadas |
| 7 | 0.5 | Álgebra lineal aplicada |
| 8 | 0.5 | Efecto de la escala |
| 9 | 0.5 | Optimización y diagnóstico |
| 10 | 0.5 | Versionado de código y datos |
| **Total** | **5.0** | |

> Las preguntas **4, 5 y 6** son las que mejor discriminan: apuntan a los errores que de
> verdad arruinan proyectos. Si el grupo falla en ellas, conviene reforzarlas antes de entrar
> al módulo 2.

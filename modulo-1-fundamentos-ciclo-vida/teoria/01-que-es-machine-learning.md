# 01 · Qué es el Machine Learning

**Módulo 1 · Sesión 1**

> **Objetivos.** Definir el Machine Learning y delimitarlo frente a la Inteligencia
> Artificial y el Deep Learning; distinguir los tres tipos de aprendizaje; clasificar un
> problema real en la categoría que le corresponde; y —lo más importante— reconocer cuándo
> **no** conviene usar Machine Learning.

## 1. Una definición operativa

La definición clásica es la de Tom Mitchell (1997), y sigue siendo la más útil porque es
verificable:

> Se dice que un programa **aprende** de la experiencia $E$ respecto a una tarea $T$ y una
> medida de desempeño $P$, si su desempeño en $T$, medido por $P$, mejora con la experiencia
> $E$.

Lo valioso de esta definición es que obliga a nombrar las tres piezas. Si no puedes decir
cuáles son $T$, $P$ y $E$ en tu problema, todavía no tienes un problema de Machine Learning.

| Pieza | Nombre | Ejemplo: predecir la nota final de un estudiante |
|---|---|---|
| $T$ | Tarea | Predecir la nota final a partir del perfil académico |
| $P$ | Desempeño | Error absoluto medio (MAE) sobre estudiantes no vistos |
| $E$ | Experiencia | Histórico de 400 estudiantes con perfil y nota conocidos |

### El contraste con la programación tradicional

La diferencia esencial no es de tecnología, es de dirección:

| | Programación tradicional | Machine Learning |
|---|---|---|
| **Entrada** | Datos + reglas escritas por una persona | Datos + respuestas conocidas |
| **Salida** | Respuestas | **Reglas** (el modelo) |
| **Quién define la lógica** | El programador | El algoritmo, a partir de los datos |

Detectar correo no deseado con reglas escritas a mano exige enumerar todas las formas de
escribir un mensaje sospechoso, y actualizarlas cada vez que alguien inventa una nueva. Con
Machine Learning se le muestran al algoritmo miles de correos etiquetados y él infiere el
patrón. Esa es la razón de ser de todo el campo: **hay problemas cuyas reglas nadie sabe
escribir, pero de los que sí tenemos ejemplos**.

### Los tres componentes de todo sistema de ML

- **Datos.** La materia prima. Ningún algoritmo compensa datos que no contienen la
  información necesaria.
- **Algoritmo.** El procedimiento que busca patrones en esos datos.
- **Modelo.** El resultado: una función, con parámetros ya ajustados, capaz de predecir.

> Conviene no confundir *algoritmo* y *modelo*. La regresión lineal es un algoritmo; la
> ecuación $\hat{y} = -0.15 + 0.62 x_1 + 0.055 x_2$, con esos números concretos, es un modelo.

## 2. IA, ML y Deep Learning

Los tres términos se usan como sinónimos en la prensa, y no lo son. La relación es de
contenencia:

$$
\text{Deep Learning} \subset \text{Machine Learning} \subset \text{Inteligencia Artificial}
$$

- **Inteligencia Artificial (IA).** El campo amplio: cualquier técnica que permita a una
  máquina realizar tareas que asociamos con la inteligencia humana. Incluye cosas que no
  aprenden de datos, como los sistemas expertos basados en reglas o los algoritmos de
  búsqueda y planificación.
- **Machine Learning (ML).** El subconjunto de la IA en el que el comportamiento se **aprende
  de datos** en lugar de programarse.
- **Deep Learning (DL).** El subconjunto del ML que usa **redes neuronales profundas**: con
  muchas capas, capaces de aprender por sí mismas la representación adecuada de los datos.

### ¿Cuándo deep learning y cuándo no?

Esta distinción es práctica, no académica, y conviene tenerla clara desde el primer día:

| Situación | Elección razonable |
|---|---|
| Datos tabulares (filas y columnas), miles de registros | ML clásico — **ensambles de árboles** suelen ganar |
| Imágenes, audio, video | Deep learning |
| Texto libre, traducción, generación | Deep learning (transformers) |
| Pocos datos (cientos de ejemplos) | ML clásico |
| Se exige explicar cada decisión | ML clásico, o DL con herramientas de interpretabilidad |

En datos tabulares —el caso más frecuente en la industria y en este curso— **el deep learning
no suele ser la mejor opción**: los métodos de boosting (sesión 11) le ganan con menos datos,
menos cómputo y más facilidad de interpretación. Es un resultado consistentemente reportado
en la literatura y lo comprobaremos empíricamente en la sesión 13.

## 3. Tipos de aprendizaje

### 3.1 Aprendizaje supervisado

Se dispone de datos **etiquetados**: para cada observación se conoce la respuesta correcta.
El objetivo es aprender una función $f$ tal que $\hat{y} = f(\mathbf{x})$ generalice a casos
nuevos.

Se divide según el tipo de respuesta:

- **Regresión** — la respuesta es un número continuo.
  Ejemplos: nota final de un estudiante, precio de una vivienda, consumo eléctrico de mañana.
- **Clasificación** — la respuesta es una categoría.
  Ejemplos: aprueba o no aprueba (binaria), tipo de falla de una máquina (multiclase).

Es el tipo de aprendizaje más común y el que ocupa la mayor parte del curso: módulos 3 y 4.

### 3.2 Aprendizaje no supervisado

No hay etiquetas. El algoritmo busca estructura en los datos por sí mismo.

- **Agrupamiento (clustering)** — encontrar grupos de observaciones parecidas.
  Ejemplo: segmentar estudiantes por perfil de rendimiento.
- **Reducción de dimensionalidad** — describir los datos con menos variables sin perder lo
  esencial. Ejemplo: resumir 50 indicadores académicos en 3 componentes.
- **Detección de anomalías** — identificar observaciones que no se parecen a las demás.

Lo estudiamos en la sesión 12. Su dificultad característica es que **no hay una respuesta
correcta contra la cual comparar**: evaluar un agrupamiento es mucho más ambiguo que evaluar
una predicción.

### 3.3 Aprendizaje por refuerzo

Un **agente** aprende a tomar decisiones interactuando con un **entorno**, guiado por
recompensas y castigos. No hay respuestas correctas dadas de antemano: hay consecuencias.

Ejemplos: control de robots, juego automático, optimización de políticas de inventario.

> Este curso **no cubre aprendizaje por refuerzo**. Se menciona para completar el mapa.

### Resumen

| Tipo | ¿Hay etiquetas? | Qué busca | Sesiones |
|---|---|---|---|
| Supervisado | Sí | Predecir la etiqueta de casos nuevos | S6–S11, S13 |
| No supervisado | No | Descubrir estructura oculta | S12 |
| Por refuerzo | No, hay recompensas | Una política de decisión | — |

## 4. Cómo encuadrar un problema real

Ante un problema nuevo, cuatro preguntas en orden:

1. **¿Qué decisión va a cambiar este modelo?** Si la respuesta es "ninguna", el proyecto no
   debería existir. Un modelo que nadie usa es un costo, no un activo.
2. **¿Qué se quiere predecir exactamente?** Definir la variable objetivo con precisión.
   "Riesgo de deserción" no es una variable; "no se matricula en el semestre siguiente" sí.
3. **¿Qué información estará disponible en el momento de predecir?** Esta pregunta previene
   la **fuga de datos**: si una variable solo se conoce después del hecho a predecir, no
   puede usarse, por mucho que mejore las métricas.
4. **¿Contra qué se compara el éxito?** Siempre hay una referencia: la regla que se usa hoy,
   el criterio de un experto, o al menos predecir siempre el valor promedio.

### Ejemplo de encuadre

| Pregunta | Respuesta |
|---|---|
| Decisión | A qué estudiantes ofrecer tutoría temprana |
| Variable objetivo | Nota final $< 3.0$ al terminar el semestre |
| Tipo de tarea | Clasificación binaria supervisada |
| Información disponible | Perfil de ingreso, promedio previo, asistencia de las primeras semanas |
| Referencia | La regla actual: "citar a quien haya perdido el primer parcial" |
| Métrica | Recall (no dejar fuera a quien necesita ayuda), con un límite de falsas alarmas |

## 5. Cuándo NO usar Machine Learning

Tan importante como saber aplicarlo:

- **Cuando una regla simple basta.** Si un umbral resuelve el 95 % de los casos, un modelo
  añade complejidad, mantenimiento y riesgo sin aportar nada.
- **Cuando no hay datos suficientes o representativos.** Con 40 observaciones no se aprende
  gran cosa. Y si los datos históricos reflejan un sesgo, el modelo lo reproducirá y lo
  amplificará.
- **Cuando se exige una explicación jurídica o clínica completa** y no se acepta un modelo
  aproximado.
- **Cuando el costo de un error es inasumible** y no hay supervisión humana en el circuito.
- **Cuando el problema es en realidad de causalidad.** El ML predice correlaciones, no
  responde "¿qué pasaría si intervenimos?". Para eso hacen falta diseño experimental o
  inferencia causal.

> **Una advertencia que vale para todo el curso.** Un modelo aprende de datos históricos, y
> los datos históricos registran cómo se ha decidido hasta ahora, con todos sus sesgos. Si el
> sistema histórico discriminaba, el modelo aprenderá a discriminar con eficiencia. La
> responsabilidad de detectarlo es de quien modela, no del algoritmo.

## 6. El ecosistema de Python

| Biblioteca | Para qué | Sesiones |
|---|---|---|
| **NumPy** | Arreglos y álgebra lineal | Todo el curso |
| **pandas** | Tablas: cargar, limpiar, transformar | Todo el curso |
| **matplotlib** / **seaborn** | Visualización | Todo el curso |
| **scikit-learn** | Modelos clásicos, preprocesamiento, evaluación | S5–S12 |
| **statsmodels** | Regresión con enfoque inferencial | S6, S7 |
| **XGBoost** / **LightGBM** | Boosting de alto rendimiento | S11 |
| **PyTorch** | Redes neuronales | S13 |
| **MLflow** / **FastAPI** | Trazabilidad y despliegue | S14 |

La razón por la que scikit-learn domina el ML clásico es su **interfaz uniforme**: todo
modelo se crea, se ajusta con `.fit(X, y)` y predice con `.predict(X)`. Cambiar de algoritmo
cuesta una línea, lo que hace barato comparar alternativas — y comparar es, en la práctica,
la mayor parte del trabajo.

## Para recordar

- El ML aprende **reglas a partir de ejemplos**, en lugar de recibirlas escritas.
- Definir $T$, $P$ y $E$ antes de programar nada.
- DL ⊂ ML ⊂ IA. En datos tabulares, el ML clásico suele ser la mejor opción.
- Tres tipos de aprendizaje: supervisado (la mayor parte del curso), no supervisado y por
  refuerzo.
- Encuadrar bien el problema importa más que elegir el algoritmo.
- Saber cuándo no usar ML es parte del criterio profesional.

## Notebooks relacionados

- [`../notebooks/01-primer-modelo-aplicado.ipynb`](../notebooks/01-primer-modelo-aplicado.ipynb)
  — el flujo completo de un problema supervisado de regresión.

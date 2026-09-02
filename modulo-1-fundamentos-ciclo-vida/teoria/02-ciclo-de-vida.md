# 02 · El ciclo de vida de un proyecto de Machine Learning

**Módulo 1 · Sesión 2**

> **Objetivos.** Recorrer las siete etapas de un proyecto de ML y entender por qué es un
> ciclo y no una secuencia; formular la definición de un problema con métricas verificables;
> distinguir métrica de negocio de métrica técnica; y reconocer los puntos donde los
> proyectos fracasan con más frecuencia.

## 1. Por qué un ciclo

El diagrama habitual muestra siete cajas en fila. La realidad es que se vuelve atrás
constantemente: el análisis exploratorio revela que faltan datos, la evaluación muestra que
la variable objetivo estaba mal definida, el monitoreo detecta que el mundo cambió.

$$
\text{Problema} \to \text{Datos} \to \text{EDA} \to \text{Modelo} \to \text{Evaluación}
\to \text{Despliegue} \to \text{Monitoreo} \to \text{Problema}
$$

Un dato conocido del oficio, y que conviene interiorizar temprano: **la mayor parte del
esfuerzo de un proyecto de ML se va en entender y preparar datos**, no en entrenar modelos.
El modelado es la parte visible y la más corta.

| # | Etapa | Sesiones del curso |
|---|---|---|
| 1 | Definición del problema | S1, S2 |
| 2 | Recolección y preparación de datos | S4 |
| 3 | Análisis exploratorio (EDA) | S4 |
| 4 | Construcción y entrenamiento | S5–S13 |
| 5 | Evaluación | S8, S9 |
| 6 | Implementación y despliegue | S14 |
| 7 | Monitoreo y mantenimiento | S14 |

## 2. Etapa 1 — Definición del problema

Es la etapa más barata de hacer bien y la más cara de hacer mal. Un error aquí no se corrige
con un modelo mejor: invalida todo lo que venga después.

### Las preguntas obligatorias

**¿Qué decisión va a apoyar el modelo?**
Si ninguna decisión cambia con la predicción, el proyecto no tiene razón de ser. Esta
pregunta descarta más proyectos de los que parece, y siempre es mejor descartarlos al
principio.

**¿Cuál es exactamente la variable objetivo?**
Debe ser observable y medible sin ambigüedad. "Riesgo de deserción" no lo es; "no formaliza
matrícula en el periodo siguiente" sí. La diferencia se paga en la etapa 2, cuando haya que
construir la etiqueta.

**¿Qué información habrá disponible en el momento de predecir?**
Esta es la pregunta que previene la **fuga de datos** (*data leakage*), el error más
frecuente y más difícil de detectar en ML aplicado. Si una variable solo se conoce después
del hecho que se quiere predecir, no puede usarse — aunque mejore espectacularmente las
métricas. Precisamente porque las mejora, engaña.

> **Ejemplo.** Para predecir deserción, la variable "número de cursos matriculados el
> semestre siguiente" predeciría casi perfecto. Y sería inútil: cuando se conoce ese dato,
> el estudiante ya desertó o no. La sesión 5 vuelve sobre esto con más casos.

**¿Cuál es la referencia actual?**
Alguien está tomando esa decisión hoy, aunque sea con una regla informal. Esa es la marca a
superar. Un modelo que no le gana a la regla actual no debe desplegarse.

**¿Qué restricciones hay?**
Tiempo de respuesta, presupuesto de cómputo, requisitos legales de explicabilidad,
disponibilidad de los datos en producción. Estas restricciones acotan qué modelos son
viables, y conocerlas antes evita construir algo que no se puede desplegar.

### Métrica de negocio y métrica técnica

Es una distinción que separa a quien hace modelos de quien resuelve problemas.

| | Métrica técnica | Métrica de negocio |
|---|---|---|
| Qué mide | Calidad estadística de la predicción | Valor generado por la decisión |
| Ejemplos | MAE, $R^2$, F1, ROC-AUC | Estudiantes retenidos, costo de tutorías, horas ahorradas |
| Quién la entiende | El equipo técnico | Quien financia el proyecto |

El trabajo consiste en **traducir** entre las dos, y esa traducción debe hacerse al
principio, no al final:

> "Un recall del 80 % con 30 % de falsas alarmas significa que detectamos a 8 de cada 10
> estudiantes en riesgo, al costo de citar a 3 estudiantes que no lo necesitaban por cada 10
> citados. Con un cupo de 200 tutorías al semestre, eso equivale a..."

Los costos rara vez son simétricos. No detectar a un estudiante que abandona cuesta mucho
más que citar a uno que no lo necesitaba. Esa asimetría debe decidir la métrica y el umbral
del modelo (sesión 9), no al revés.

## 3. Etapa 2 — Recolección y preparación

De dónde salen los datos, con qué calidad, y bajo qué condiciones se pueden usar.

- **Fuentes**: bases de datos internas, archivos, APIs, web scraping, datos de terceros.
- **Preguntas de gobierno**: ¿quién es el dueño del dato? ¿hay información personal? ¿qué
  exige la normativa de protección de datos?
- **Preparación**: valores faltantes, duplicados, outliers, unificación de formatos.

Regla no negociable: **los datos crudos son de solo lectura**. Toda transformación produce un
archivo nuevo. Perder el original es perder la capacidad de rehacer el trabajo.

Todo esto se desarrolla en la sesión 4.

## 4. Etapa 3 — Análisis exploratorio

Antes de modelar hay que saber qué hay en los datos: distribuciones, relaciones, valores
extraños, cuánta señal hay realmente. El EDA no es un trámite: es donde se detectan los
problemas que arruinarían el modelo, y donde se decide qué características construir.

Sesión 4.

## 5. Etapa 4 — Construcción y entrenamiento

Aquí se elige la representación de los datos (ingeniería de características, S5), el
algoritmo y sus hiperparámetros. Ocupa la mayor parte del curso, pero conviene recordar su
proporción real dentro de un proyecto.

Dos ideas que gobiernan esta etapa:

- **Empezar simple.** Una regresión lineal o un árbol pequeño como línea base. Solo se
  justifica complicar el modelo si mejora de forma medible sobre esa base.
- **Separar los datos antes de tocarlos.** El conjunto de prueba se aparta al principio y no
  se mira hasta el final.

## 6. Etapa 5 — Evaluación

Medir el desempeño sobre datos no vistos, con la métrica que se definió en la etapa 1, y
compararlo contra la referencia.

Los errores clásicos de esta etapa:

- Evaluar sobre los datos de entrenamiento (mide memorización, no aprendizaje).
- Usar el conjunto de prueba muchas veces para ir ajustando. Después de veinte decisiones
  tomadas mirándolo, ese conjunto ya no es "no visto": por eso existen los conjuntos de
  validación y la validación cruzada (sesión 8).
- Reportar un solo número sin intervalo ni variabilidad.
- Elegir la métrica después de ver los resultados.

## 7. Etapa 6 — Despliegue

> "Sin despliegue no hay valor."

Un modelo en un notebook no sirve a nadie. Desplegar significa exponerlo de forma que otros
sistemas o personas puedan consumirlo: típicamente una **API** (sesión 14), a veces un
proceso por lotes que corre cada noche.

Consideraciones: tiempo de respuesta, escalabilidad, seguridad, y sobre todo **coherencia
entre entrenamiento y producción**. Si en entrenamiento se escaló con la media del dataset
histórico, en producción hay que aplicar exactamente esa misma transformación. Los
`Pipeline` de scikit-learn (sesión 5) existen en buena medida por esto.

## 8. Etapa 7 — Monitoreo y mantenimiento

> "Sin monitoreo no hay garantía."

Un modelo desplegado se degrada. No porque el código se rompa, sino porque **el mundo
cambia**:

- **Drift de datos** — la distribución de las entradas cambia. Cambió el perfil de los
  estudiantes admitidos, y el modelo ve datos distintos de los que aprendió.
- **Drift de concepto** — cambia la relación entre entradas y salida. La misma asistencia
  significa algo diferente tras un cambio de metodología.

Hay que vigilar tanto las métricas técnicas como las de negocio, y definir de antemano el
criterio de reentrenamiento. Sesión 14.

## 9. Dónde fracasan los proyectos

| Fallo | Etapa | Cómo se evita |
|---|---|---|
| Resolver el problema equivocado | 1 | Definir la decisión que cambia, antes de modelar |
| Fuga de datos | 1, 4 | Preguntar qué se sabe en el momento de predecir |
| Datos insuficientes o sesgados | 2 | EDA honesto; auditar representatividad |
| Sobreajuste al conjunto de prueba | 5 | Validación cruzada; tocar la prueba una sola vez |
| El modelo nunca se despliega | 6 | Pensar el despliegue desde el principio |
| Se degrada en silencio | 7 | Monitoreo con alertas y umbrales definidos |

Vale la pena notar que **cinco de los seis fallos ocurren fuera del modelado**. Es la razón
por la que este curso dedica un módulo entero a los datos y otro al despliegue.

## Para recordar

- Es un ciclo: se vuelve atrás constantemente, y eso es normal.
- La definición del problema es la etapa más determinante.
- Métrica técnica y métrica de negocio no son lo mismo; hay que traducir entre ellas.
- "¿Qué sabré en el momento de predecir?" es la pregunta que previene la fuga de datos.
- Sin despliegue no hay valor; sin monitoreo no hay garantía.

## Notebooks relacionados

- [`../notebooks/02-proyecto-reproducible-aplicado.ipynb`](../notebooks/02-proyecto-reproducible-aplicado.ipynb)
  — estructura de proyecto y los cuatro niveles de reproducibilidad.

## Documento siguiente

- [`03-versionado-codigo-datos.md`](03-versionado-codigo-datos.md) — Git y DVC.

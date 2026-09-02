# Clave · Quiz Módulo 2 — Datos y características

> **Material del docente.** Se indica lo mínimo exigible y, cuando aplica, el error típico que
> conviene comentar en la retroalimentación.

---

**1. `dropna()` con 30 % de faltantes**

Dos razones (bastan dos de estas):

- **Se pierde el 30 % de los datos**, o más si otras columnas también tienen faltantes en
  filas distintas.
- **Puede sesgar la muestra.** Si la ausencia no es MCAR, las filas que quedan no representan a
  la población: se eliminan sistemáticamente ciertos perfiles.
- **Se pierde la información contenida en la ausencia misma**, que a menudo es predictiva.

Qué haría antes: diagnosticar el mecanismo — calcular la tasa de faltantes por grupos de las
demás variables y comparar el objetivo entre quienes tienen y no tienen el dato. Solo con eso
se puede elegir la estrategia.

---

**2. MCAR, MAR, MNAR**

| Mecanismo | Definición | Ejemplo aceptable |
|---|---|---|
| MCAR | La ausencia no depende de nada | Un sensor falló aleatoriamente |
| MAR | Depende de otras variables **observadas** | La edad falta más en tercera clase, y la clase se conoce |
| MNAR | Depende del **valor ausente** | Quien tiene ingresos muy altos no los declara |

**Para MAR:** imputar **condicionando** a la variable de la que depende la ausencia (por
ejemplo, la mediana por clase). **Incorrecto:** imputar con la media o mediana global, que
asigna a un subgrupo el valor típico de toda la población e introduce un sesgo sistemático.

---

**3. Colesterol medido solo a pacientes de riesgo**

**a)** **MNAR.** El valor falta por una razón relacionada con el propio valor esperado: se midió
precisamente a quienes se sospechaba que lo tenían alto.

**b)** La mediana se calcula sobre los **medidos**, que son la subpoblación de riesgo y por
tanto tienen valores más altos de lo normal. Imputar con esa mediana asignaría a los pacientes
sanos un colesterol artificialmente elevado. El sesgo va en dirección contraria a la realidad.

**c)** No imputar el valor. Crear la binaria `midieron_colesterol`, que además es
**informativa por sí misma**: indica que el médico vio motivo de sospecha.

> **Matiz que merece punto extra.** Esa variable puede ser una fuga por retroalimentación:
> refleja una decisión clínica previa. Si el modelo pretende sustituir ese juicio, aprenderá a
> imitarlo en lugar de a diagnosticar.

---

**4. 340 filas idénticas**

Procedimiento:

1. Comprobar si existe una **columna identificadora** (id de registro, documento, número de
   transacción).
2. Si la hay: mirar si el **id** se repite. Si se repite, son duplicados reales. Si no, son
   observaciones distintas que coinciden en todos los valores.
3. Si no hay identificador: investigar el origen del dataset y el proceso de carga.
4. Evaluar el impacto: ¿qué perfil tienen las filas repetidas? Eliminarlas puede sesgar hacia
   un grupo concreto.

**Cuándo no eliminarlas:** cuando **no hay identificador** y las variables son pocas o de baja
cardinalidad, de modo que coincidir en todas es plausible. El caso del Titanic: dos hombres de
tercera clase de 25 años que viajaban solos y pagaron lo mismo producen filas idénticas siendo
personas distintas. Eliminarlas descartaría pasajeros reales y sesgaría hacia el perfil más
común.

---

**5. 200 outliers legítimos en el ingreso**

**a)** **No.** Son valores reales, no errores. Los ingresos tienen naturalmente una
distribución muy asimétrica, y eliminar la cola derecha equivale a borrar un segmento real de
la población y sesgar todas las conclusiones.

**b)** Dos de: transformación **logarítmica**; **winsorización** (recorte a los percentiles 1 y
99); usar **modelos robustos** a extremos; modelar el logaritmo del objetivo.

**c)** Afectados: regresión lineal y logística, KNN, K-Means, SVM, PCA — todos los basados en
distancias, medias o mínimos cuadrados. **No afectados:** árboles de decisión, Random Forest y
Gradient Boosting, que solo comparan ordenamientos dentro de cada variable.

---

**6. KNN con escalas dispares**

**a)** La distancia euclidiana suma diferencias al cuadrado. El salario varía en millones y la
edad en decenas: la distancia queda **completamente dominada por el salario**, y la edad y la
antigüedad dejan de influir. El modelo ignora dos de las tres variables, por unidades y no por
utilidad.

**b)** **Estandarizar** (`StandardScaler`) o normalizar, siempre **dentro de un `Pipeline`** y
aprendiendo los parámetros solo del conjunto de entrenamiento.

**c)** **Sí cambiaría.** Un Random Forest **no necesita escalado**: cada división compara
valores dentro de una sola variable (`salario > 3.500.000`), y ese umbral es indiferente a la
escala. Escalar no le perjudica, pero tampoco aporta.

---

**7. One-hot vs. ordinal**

**One-hot** crea una columna binaria por categoría; no impone ningún orden. Es la opción para
variables **nominales**.

**Ordinal** asigna un entero a cada categoría, imponiendo un orden y una distancia.

- **Correcta:** `nivel_educativo` = {primaria, secundaria, pregrado, posgrado} → 0, 1, 2, 3.
  Hay un orden real.
- **Incorrecta:** `ciudad` = {Bogotá, Cali, Pereira} → 0, 1, 2.

Qué le dice al modelo la codificación incorrecta: que Cali (1) está **entre** Bogotá (0) y
Pereira (2), y que la distancia de Bogotá a Pereira es el doble que la de Bogotá a Cali. Un
modelo lineal ajustará un único coeficiente asumiendo ese orden inventado.

---

**8. El flujo con 300 filas y 8.000 columnas**

**a)** Dos errores:

1. `StandardScaler` ajustado sobre todo `X` antes de la validación cruzada.
2. `SelectKBest` ajustado sobre todo `X` **usando `y`** antes de la validación cruzada.

**El segundo es muchísimo más grave.** El primero filtra dos números por variable que no dicen
nada sobre `y`; el segundo filtra *qué variables se parecen a la respuesta*, que es información
directa sobre el objetivo.

**b)** Con **8.000 columnas y solo 300 filas**, por puro azar habrá columnas que se parezcan a
`y` en esas 300 observaciones concretas. `SelectKBest` las encuentra —es su función—, pero al
mirar el dataset completo, esas coincidencias incluyen las filas que después harán de
validación. La validación cruzada ya no evalúa nada: las variables se eligieron *sabiendo* las
respuestas de los pliegues de validación.

Es el problema de las comparaciones múltiples convertido en fuga: con 8.000 pruebas al 1 %,
unas 80 salen "significativas" solo por azar.

**c)**

```python
flujo = Pipeline([
    ("escalar", StandardScaler()),
    ("seleccionar", SelectKBest(f_classif, k=30)),
    ("modelo", modelo),
])
puntajes = cross_val_score(flujo, X, y, cv=5)
```

Ahora ambos pasos se ajustan **por separado en cada pliegue**, con sus datos de entrenamiento.

> Punto extra si el estudiante anticipa que la accuracy real caerá drásticamente, o si señala
> que con $p \gg n$ este es exactamente el escenario donde la fuga es devastadora.

---

**9. Fuga en la predicción de cancelación**

| | Variable | ¿Fuga? | Por qué |
|---|---|---|---|
| a) | Reclamos en los últimos 6 meses | **No** | Información pasada, disponible al predecir |
| b) | Fecha de solicitud de cancelación | **Sí** | *Es* el evento a predecir. Si existe, el cliente ya canceló |
| c) | Uso promedio del mes a predecir | **Sí** | Temporal: pertenece al futuro respecto al momento de decidir |
| d) | Antigüedad en meses | **No** | Conocida en el momento de predecir |
| e) | Contacto del equipo de retención | **Sí**, por retroalimentación | Es consecuencia de que el sistema ya lo marcó como riesgo. El modelo aprendería a imitar la decisión previa, y en producción esa variable no existe antes de decidir |

> El caso **e)** es el valioso. Las fugas b) y c) son evidentes una vez señaladas; la de
> retroalimentación aparece constantemente en sistemas reales y no se detecta mirando las
> métricas — que además mejoran.

---

**10. Qué garantiza el `Pipeline`**

- Al llamar a **`.fit(X, y)`**, cada paso ejecuta `fit_transform` **usando únicamente los datos
  de entrenamiento**: ahí aprende las medianas de imputación, las medias y desviaciones del
  escalado, las categorías del codificador y las variables seleccionadas.
- Al llamar a **`.predict(X)`**, cada paso ejecuta solo `transform`, aplicando lo que aprendió
  antes. No vuelve a aprender nada.
- Dentro de `cross_val_score`, todo ese ciclo ocurre **por separado en cada pliegue**, lo que
  hace que la evaluación sea honesta.

Aplicar los pasos por separado no garantiza nada de eso: hay que acordarse de aplicar
exactamente las mismas transformaciones, con los mismos parámetros, al conjunto de prueba y en
producción. Es fácil equivocarse y el error **no avisa**.

**Por qué se despliega el pipeline completo:** el modelo por sí solo no sabe imputar, escalar ni
codificar. Los parámetros del preprocesamiento —medianas, medias, desviaciones, categorías—
forman parte de lo aprendido y son necesarios para transformar un dato nuevo exactamente igual
que en el entrenamiento. Sin ellos, en producción se aplicaría un preprocesamiento distinto y
las predicciones serían inválidas.

---

## Distribución de puntos

| Pregunta | Puntos | Evalúa |
|---|---|---|
| 1 | 0.5 | Criterio frente a la receta automática |
| 2 | 0.5 | Mecanismos de datos faltantes |
| 3 | 0.5 | MNAR y por qué imputar es engañoso |
| 4 | 0.5 | Duplicados reales vs. aparentes |
| 5 | 0.5 | Outliers legítimos; qué modelos se afectan |
| 6 | 0.5 | Escalado y qué modelos lo necesitan |
| 7 | 0.5 | Codificación de categóricas |
| 8 | 0.5 | Fuga por selección: la grave |
| 9 | 0.5 | Fuga temporal y por retroalimentación |
| 10 | 0.5 | `Pipeline` y artefacto de despliegue |
| **Total** | **5.0** | |

> Las preguntas **8, 9e y 3** son las que mejor discriminan. Si el grupo falla en la 8, conviene
> repasar el notebook 03 antes de entrar al módulo 3, porque toda la evaluación de modelos
> descansa sobre ese punto.

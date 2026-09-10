# 05 · Sesgo-varianza, validación cruzada y comparación honesta de modelos

**Módulo 3 · Sesión 8** — Evaluación y selección de modelos

## Objetivos

- Descomponer el error esperado de un modelo en sesgo, varianza y ruido irreducible, y usar
  esa descomposición para definir sobreajuste y subajuste sin ambigüedad.
- Reemplazar la "partición afortunada" de las sesiones anteriores por validación cruzada, y
  entender qué gana la versión **repetida**.
- **Cuantificar la incertidumbre** de una métrica y la diferencia entre dos modelos — la
  herramienta que `02-proyecto-reproducible-aplicado.ipynb` (módulo 1) y `ej02-pipeline-sol.md`
  (módulo 2) prometieron y no entregaron todavía.
- Leer curvas de aprendizaje y de validación como diagnóstico.

## 1. La descomposición sesgo-varianza

Para un punto $x$, el error cuadrático esperado de un modelo $\hat{f}$ entrenado sobre datos
aleatorios se descompone en tres partes:

$$
\mathbb{E}\left[(y - \hat{f}(x))^2\right] = \underbrace{\left(\mathbb{E}[\hat{f}(x)] -
f(x)\right)^2}_{\text{sesgo}^2} + \underbrace{\text{Var}[\hat{f}(x)]}_{\text{varianza}} +
\underbrace{\sigma^2}_{\text{ruido irreducible}}
$$

donde $f(x)$ es la función verdadera y la esperanza es sobre el muestreo aleatorio del
conjunto de entrenamiento —si se reentrenara el modelo mil veces con mil muestras distintas
de la misma población, ¿qué tan lejos está el promedio de esas predicciones de la verdad
(sesgo), y qué tanto varían esas predicciones entre sí (varianza)?—.

- **Sesgo**: error por usar un modelo demasiado simple para la relación real. Una regresión
  lineal sobre una relación curva tiene sesgo, sin importar cuántos datos se le den.
- **Varianza**: error por la sensibilidad del modelo a la muestra específica de
  entrenamiento. Un polinomio de grado 15 sobre 30 puntos cambia radicalmente si se cambian
  unos pocos puntos — alta varianza. Es la misma inestabilidad que
  `03-multicolinealidad-polinomica.md` y `04-regularizacion.md` mostraron para los
  coeficientes bajo colinealidad, ahora vista como propiedad general de cualquier modelo.
- **Ruido irreducible** ($\sigma^2$): variabilidad de $y$ que ningún modelo, por bueno que
  sea, puede explicar. Ningún ajuste lo reduce.

### El compromiso

Sesgo y varianza se mueven en direcciones opuestas al cambiar la complejidad del modelo:

| Complejidad | Sesgo | Varianza | Síntoma |
|---|---|---|---|
| Muy baja (subajuste) | Alto | Baja | Error de entrenamiento **y** de prueba altos, parecidos entre sí |
| Muy alta (sobreajuste) | Bajo | Alta | Error de entrenamiento bajo, error de prueba mucho mayor |
| Apropiada | Moderado | Moderada | Error de entrenamiento y de prueba bajos y cercanos |

El error total (la curva que de verdad importa) tiene forma de **U** en función de la
complejidad: al principio baja porque el sesgo cae más rápido de lo que sube la varianza;
después de cierto punto, sube porque la varianza domina. $\lambda$ en Ridge/Lasso, el grado de
un polinomio, y la profundidad de un árbol (módulo 4) son todos, en el fondo, la misma perilla
sesgo-varianza vista desde ejes distintos.

## 2. Validación cruzada (k-fold)

Un solo split entrenamiento/prueba da **un** número. Ese número tiene su propia varianza —
`04-regularizacion-aplicado.ipynb` (sesión 7) terminó reconociéndolo explícitamente: Lasso con
$\lambda=50$ pareció ganarle a OLS en *ese* test set, pero la curva de validación decía que el
$\lambda$ óptimo estaba cerca de cero. Un resultado así no se puede distinguir de la suerte del
split sin repetir el experimento.

**K-fold** reparte los datos en $k$ partes (*folds*) del mismo tamaño. Se entrena $k$ veces,
cada vez usando $k-1$ partes para entrenar y la restante para validar, rotando cuál parte se
deja fuera. El resultado no es un número: son $k$ números, uno por pliegue, de los que se
puede calcular una media y una desviación estándar.

$$
\overline{\text{error}} = \frac{1}{k}\sum_{i=1}^k \text{error}_i \qquad\qquad
\text{ee} = \frac{\text{desviación estándar de los } k \text{ errores}}{\sqrt{k}}
$$

$k=5$ o $k=10$ son las opciones habituales: suficientes pliegues para estimar la variabilidad
sin que cada uno se quede con muy pocos datos.

> **Una advertencia sobre ese error estándar.** La fórmula $\text{ee} = s/\sqrt{k}$ supone que
> los $k$ errores son independientes entre sí, y no lo son: los conjuntos de entrenamiento de
> dos pliegues cualesquiera comparten la mayoría de sus datos. En consecuencia, el ee así
> calculado **subestima** la incertidumbre real. Se usa igual en este curso porque es simple y
> el orden de magnitud es informativo — pero conviene leerlo como una cota optimista, no como
> un intervalo exacto.

### Variantes

- **K-fold estratificado**: para clasificación (módulo 4), conserva la proporción de cada
  clase en cada pliegue. Sin esto, un pliegue podría quedarse casi sin ejemplos de la clase
  minoritaria por azar.
- **K-fold temporal** (o *walk-forward*): cuando los datos tienen orden cronológico, los
  pliegues aleatorios entrenan con el futuro y validan con el pasado — exactamente la fuga
  temporal que `03-fuga-de-datos-intuicion.ipynb` (módulo 2) advirtió. La versión correcta
  siempre valida con datos posteriores a los de entrenamiento de ese pliegue.

### K-fold repetido: de un número a una distribución

Ejecutar k-fold varias veces, cada vez con una partición aleatoria distinta (semillas
distintas), da $k \times r$ mediciones del error en vez de $k$. No reduce el sesgo de la
estimación, pero sí retrata mejor la variabilidad — la varianza *de la estimación del error*,
no de las predicciones— y dos ejecuciones del experimento completo dan conclusiones más
parecidas entre sí. Es la respuesta directa a la advertencia de `02-proyecto-reproducible-aplicado.ipynb`
(módulo 1): "en la sesión 8 mediremos esa variabilidad a propósito con validación cruzada, en
vez de esconderla detrás de una sola partición afortunada".

## 3. Comparar dos modelos con honestidad

`04-pipeline-caracteristicas-aplicado.ipynb` (módulo 2) ya usó, sin nombrarla formalmente,
la herramienta que resuelve esto: comparar dos modelos **sobre los mismos pliegues** (no en
particiones independientes) y mirar la diferencia pliegue por pliegue, no solo el promedio.

$$
d_i = \text{error}_i(\text{modelo A}) - \text{error}_i(\text{modelo B}), \qquad i=1,\dots,k
$$

La comparación pareada tiene una ventaja clave sobre comparar promedios sueltos: si ambos
modelos son igual de sensibles a qué datos caen en cada pliegue, esa sensibilidad se cancela
en la resta $d_i$, y lo que queda aísla mejor la diferencia real entre A y B. Con la media
$\bar{d}$ y el error estándar de los $d_i$, una regla práctica y suficiente para este curso:

> Si $|\bar{d}|$ es menor a, aproximadamente, dos errores estándar, la diferencia observada es
> indistinguible del ruido de muestreo — exactamente lo que concluyó el módulo 2: "la
> desviación entre pliegues es cinco veces mayor que la diferencia: lo único que se puede
> concluir es que no hay diferencia detectable".

Esta no es una prueba de hipótesis formal (eso pertenece a un curso de estadística inferencial), pero
captura la idea correcta con las herramientas que ya se tienen: **antes de preferir un modelo
sobre otro, hay que saber si la diferencia observada sobrevive a repetir el experimento.**

## 4. Curvas de aprendizaje y de validación

Dos diagnósticos visuales, con ejes distintos:

- **Curva de aprendizaje**: error de entrenamiento y de validación en el eje $y$, **tamaño de
  la muestra de entrenamiento** en el eje $x$, con la complejidad del modelo fija. Responde
  "¿me ayudaría conseguir más datos?".
  - Si ambas curvas convergen a un error alto: sesgo alto — más datos no van a ayudar, hace
    falta un modelo más complejo (o mejores variables).
  - Si hay una brecha grande entre ambas que se va cerrando lentamente: varianza alta — más
    datos sí ayudan, o hace falta regularizar más.
- **Curva de validación**: error de entrenamiento y de validación en el eje $y$,
  **complejidad del modelo** ($\lambda$, grado del polinomio, profundidad) en el eje $x$, con
  el tamaño de muestra fijo. Es la curva en forma de U de la sección 1, vista directamente.
  Es la misma curva que `04-regularizacion-aplicado.ipynb` ya dibujó para $\lambda$ — aquí se
  le pone nombre y se generaliza a cualquier hiperparámetro de complejidad.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Sesgo² + varianza + ruido | Marco para diagnosticar sub/sobreajuste | Se ve directamente en las curvas de validación de la sección 4 |
| K-fold repetido | Un número → una distribución | Selección de hiperparámetros (`06-seleccion-hiperparametros.md`) |
| Comparación pareada por pliegue | Formaliza lo que el módulo 2 hizo de manera informal | Notebook 06, comparación final de modelos |
| Curva de aprendizaje vs. de validación | Ejes distintos: tamaño de muestra vs. complejidad | Diagnóstico estándar en el proyecto integrador |

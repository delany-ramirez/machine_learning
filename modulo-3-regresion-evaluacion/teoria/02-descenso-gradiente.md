# 02 · Descenso del gradiente aplicado a regresión múltiple

**Módulo 3 · Sesión 6** — Regresión lineal

## Objetivos

- Retomar el descenso del gradiente de `04-gradientes-intuicion.ipynb` (módulo 1) y
  extenderlo a regresión múltiple, en forma vectorizada.
- Distinguir batch, mini-batch y SGD, y cuándo conviene cada uno.
- Diagnosticar convergencia con la curva de aprendizaje y elegir la tasa de aprendizaje.
- Entender por qué, para OLS, el descenso del gradiente es una alternativa de cómputo a la
  ecuación normal, y no un método distinto.

> Este documento **no repite** qué es una derivada, un gradiente o la regla de la cadena: eso
> está en `05-calculo-y-probabilidad.md` y en el notebook `04-gradientes-intuicion.ipynb`,
> ambos del módulo 1. Aquí se asume ese vocabulario y se aplica al caso concreto de la
> regresión lineal con varios predictores.

## 1. La función de costo en forma vectorizada

Para regresión múltiple con matriz de diseño $\mathbf{X} \in \mathbb{R}^{n \times (p+1)}$ (la
primera columna, de unos, absorbe el intercepto), el costo de OLS es:

$$
\mathcal{L}(\boldsymbol{\beta}) = \frac{1}{n} \lVert \mathbf{y} - \mathbf{X}\boldsymbol{\beta}
\rVert_2^2
$$

y su gradiente respecto a $\boldsymbol{\beta}$ —la generalización directa de lo que el
notebook 04 del módulo 1 dedujo para $\beta_0$ y $\beta_1$ por separado— es:

$$
\nabla_{\boldsymbol{\beta}} \mathcal{L} = -\frac{2}{n} \mathbf{X}^{\top} (\mathbf{y} -
\mathbf{X}\boldsymbol{\beta})
$$

La regla de actualización es la misma de siempre, ahora sobre un vector completo de
parámetros:

$$
\boldsymbol{\beta} \leftarrow \boldsymbol{\beta} - \eta \, \nabla_{\boldsymbol{\beta}}
\mathcal{L}
$$

Nótese que esto **no es un algoritmo nuevo**: es el mismo `descenso_2d` del notebook 04,
donde el "punto" ahora tiene $p+1$ coordenadas en vez de 2, y el gradiente se calcula con
álgebra matricial en lugar de derivar cada término a mano.

## 2. ¿Para qué usar descenso si la ecuación normal es exacta?

Para OLS puro, con pocos predictores, la ecuación normal (`01-regresion-lineal.md`) es más
rápida y no tiene hiperparámetros que ajustar. El descenso del gradiente se vuelve necesario
o preferible cuando:

- **$p$ es grande.** Invertir $\mathbf{X}^{\top}\mathbf{X}$ cuesta $O(p^3)$; un paso de
  descenso cuesta $O(np)$.
- **$n$ es demasiado grande para caber en memoria.** La ecuación normal necesita todos los
  datos a la vez; el descenso puede procesar los datos por lotes (sección 3).
- **El modelo no tiene solución cerrada.** Regresión logística (módulo 4), redes neuronales
  (módulo 5) y las versiones regularizadas con penalización $L_1$ (sesión 7) no siempre la
  tienen. El descenso del gradiente —o variantes como Adam— es el método general que funciona
  en todos esos casos. Aprenderlo aquí, sobre el problema más simple donde se puede comparar
  contra la respuesta exacta, es lo que lo vuelve transferible.

## 3. Batch, mini-batch y estocástico (SGD)

La pregunta es: ¿sobre cuántas observaciones se calcula el gradiente en cada paso?

| Variante | Gradiente calculado sobre | Pasos por época | Ventaja | Costo |
|---|---|---|---|---|
| **Batch** | Las $n$ observaciones completas | 1 | Dirección exacta del gradiente; converge de forma suave | Un paso cuesta $O(np)$; lento si $n$ es grande |
| **Estocástico (SGD)** | 1 observación, elegida al azar | $n$ | Un paso es casi gratis; puede escapar de mínimos locales poco profundos | Dirección ruidosa: la trayectoria oscila y nunca se asienta exactamente en el mínimo |
| **Mini-batch** | Un subconjunto de tamaño $b$ (p. ej. 32, 64) | $n/b$ | Compromiso: menos ruido que SGD, más rápido que batch; aprovecha operaciones vectorizadas | Introduce un hiperparámetro más ($b$) |

Para OLS con datasets del tamaño de este curso (miles de filas), la diferencia práctica es
pequeña y batch suele bastar. La razón para estudiar las tres variantes aquí es que **mini-batch
es el estándar de facto para entrenar redes neuronales** (módulo 5): este es el lugar del curso
donde conviene entender el compromiso, sobre un problema donde también existe la respuesta
exacta para comparar.

Una **época** es una pasada completa por los $n$ datos. Con batch, una época es un paso; con
SGD, son $n$ pasos; con mini-batch, $n/b$ pasos.

## 4. Diagnóstico de convergencia

La curva de aprendizaje —costo vs. iteración, la misma gráfica que cierra el notebook 04 del
módulo 1— es la herramienta principal:

- **Desciende y se aplana**: convergió. El número de iteraciones adicionales ya no ayuda.
- **Desciende muy despacio, sin aplanarse**: $\eta$ demasiado pequeña, o hacen falta más
  iteraciones.
- **Oscila sin bajar, o diverge (sube)**: $\eta$ demasiado grande.
- **Con SGD o mini-batch, la curva es ruidosa por diseño** — cada paso usa datos distintos.
  Se diagnostica sobre una versión suavizada (promedio móvil) o sobre el costo evaluado en
  los datos completos cada cierto número de pasos.

### El escalado no es opcional

El notebook 04 del módulo 1 ya lo señaló para dos variables: si los predictores tienen
escalas muy distintas (p. ej. área en pies cuadrados, de cientos a miles, y número de baños,
de 1 a 4), la superficie de costo es un valle alargado y elíptico. El gradiente apunta casi
perpendicular al eje largo del valle, y el descenso avanza en zigzag en vez de ir directo al
mínimo — necesita muchas más iteraciones, o una $\eta$ tan pequeña que se vuelve
impracticable. **Estandarizar cada predictor** ($z = (x - \bar{x})/s$) antes de correr el
descenso vuelve la superficie de costo aproximadamente circular y acelera la convergencia de
forma drástica. La ecuación normal no tiene este problema porque resuelve el sistema de forma
exacta, sin importar la geometría de la superficie.

## Resumen

| Concepto | Idea | Dónde reaparece |
|---|---|---|
| Gradiente vectorizado | $\nabla \mathcal{L} = -\frac{2}{n}\mathbf{X}^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\beta})$ | Regularización (sesión 7): se le suma el gradiente de la penalización |
| Mini-batch | Compromiso entre batch y SGD | Entrenamiento de redes neuronales (módulo 5) |
| Curva de aprendizaje | Diagnóstico de convergencia | Curvas de aprendizaje vs. tamaño de muestra (sesión 8, distinto eje x) |
| Escalado antes de descender | Evita zigzag en la convergencia | Cualquier modelo entrenado por gradiente en el resto del curso |

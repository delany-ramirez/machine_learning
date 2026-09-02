# Solución · Ejercicio 02 · Álgebra lineal y gradientes con NumPy

> **Material del docente.** Todos los números de este documento se obtuvieron ejecutando el
> código con `rendimiento-estudiantes.csv` generado con `SEMILLA = 42`. Si el estudiante
> regeneró el dataset, deben coincidir exactamente.

## Parte A — Producto punto y similitud

### A.1 Predicción vectorizada

```python
beta_0, beta = -0.15, np.array([0.62, 0.055, 0.011])
pred = beta_0 + X @ beta
```

| Resultado | Valor |
|---|---|
| Primeras 5 predicciones | `[3.168, 4.410, 2.599, 3.802, 3.661]` |
| Media de las predicciones | 3.4761 |
| Media real de `nota_final` | 3.3947 |
| MAE | 0.2864 |

> Nota: estos coeficientes son los del proceso generador, pero **falta el término
> `trabaja`**, cuyo efecto es $-0.22$. Por eso las predicciones quedan sistemáticamente altas
> (3.48 frente a 3.39). Un buen estudiante lo detecta; conviene señalarlo aunque no se pida.

### A.2 Similitud coseno

```python
def similitud_coseno(u, v):
    return (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))
```

| | E0001 | E0002 | Similitud |
|---|---|---|---|
| Crudo | `[3.66, 2.7, 81.8]` | `[4.14, 18.2, 90.2]` | **0.9863** |
| Estandarizado | `[0.174, -1.173, -0.285]` | `[1.170, 1.829, 0.670]` | **−0.7695** |

**Explicación esperada.** Con datos crudos, la tercera componente (asistencia, ~80–90) es
mucho mayor que las otras dos. Ambos vectores están dominados por ella y apuntan casi en la
misma dirección: la similitud es alta **por las unidades, no por parecido real**.

Al estandarizar, cada variable se mide en desviaciones respecto a la media, y aparece la
verdad: E0001 estudia mucho **menos** que el promedio ($-1.17\sigma$) y E0002 mucho **más**
($+1.83\sigma$). Son estudiantes opuestos, y la similitud negativa lo refleja.

> **Este contraste —de 0.99 a −0.77— es el punto central del ejercicio.** Vale la pena
> discutirlo en clase: una métrica de similitud sin estandarizar puede decir exactamente lo
> contrario de la realidad.

## Parte B — Distancias y escalado

### B.1–B.2 Vecinos más cercanos de E0001

Consulta: `E0001` → `[3.66, 2.7, 81.8]`, nota real **3.23**.

**Sin estandarizar:**

| Vecino | Valores | Distancia | Nota |
|---|---|---|---|
| E0134 | `[3.57, 3.3, 81.6]` | 0.639 | 2.97 |
| E0285 | `[3.96, 3.7, 81.8]` | 1.044 | 2.70 |
| E0063 | `[3.65, 2.9, 80.7]` | 1.118 | 2.54 |

**Estandarizado:**

| Vecino | Valores | Distancia | Nota |
|---|---|---|---|
| E0063 | `[3.65, 2.9, 80.7]` | 0.133 | 2.54 |
| E0134 | `[3.57, 3.3, 81.6]` | 0.221 | 2.97 |
| E0092 | `[3.65, 3.6, 80.6]` | 0.222 | 2.87 |

**Los conjuntos no coinciden**: E0285 sale y entra E0092. Además cambia el orden. Con un $k$
pequeño, un cambio así modifica la predicción.

### B.3 Predicción por promedio de vecinos

| Método | Predicción | Nota real |
|---|---|---|
| 3 vecinos, crudo | 2.737 | 3.23 |
| 3 vecinos, estandarizado | 2.793 | 3.23 |

Ambas subestiman. Es esperable y vale la pena comentarlo: `E0001` tiene una nota alta para su
perfil (estudia poco y asiste poco), así que sus vecinos "reales" no lo predicen bien. Es el
ruido irreducible del proceso generador, no un fallo del método.

### B.4 Qué domina la distancia

| Variable | Desviación estándar |
|---|---|
| `promedio_anterior` | ≈ 0.48 |
| `horas_estudio_semana` | ≈ 5.17 |
| `asistencia_pct` | ≈ 8.81 |

La distancia euclidiana suma diferencias al cuadrado. Como `asistencia_pct` varía en una
escala ~18 veces mayor que `promedio_anterior`, sus diferencias al cuadrado son ~340 veces
mayores. **La distancia es prácticamente la distancia en asistencia**, y el promedio académico
—la variable más correlacionada con la nota— casi no interviene.

Estandarizar iguala la contribución potencial de cada variable.

## Parte C — Componentes principales

### C.1 Matriz de covarianza de los datos estandarizados

|  | promedio | horas | asistencia |
|---|---|---|---|
| **promedio** | 1.003 | 0.036 | 0.065 |
| **horas** | 0.036 | 1.003 | 0.127 |
| **asistencia** | 0.065 | 0.127 | 1.003 |

> **Detalle numérico que suele generar preguntas.** La diagonal da 1.003 y no 1.000 porque
> `np.std` divide por $n$ y la fórmula de la covarianza divide por $n-1$. La diferencia es el
> factor $400/399 = 1.0025$. No es un error; conviene aclararlo si alguien lo nota.

### C.2 Valores propios y varianza explicada

| Componente | Valor propio | Varianza explicada | Acumulada |
|---|---|---|---|
| PC1 | 1.1614 | 38.6 % | 38.6 % |
| PC2 | 0.9740 | 32.4 % | 71.0 % |
| PC3 | 0.8720 | 29.0 % | 100.0 % |

Primer vector propio: `[-0.413, -0.623, -0.665]`.

### C.3 Ortogonalidad

$\mathbf{v}_1 \cdot \mathbf{v}_2 = 0$ (del orden de $10^{-17}$, cero numérico).

Lo garantiza que **la matriz de covarianza es simétrica**: el teorema espectral asegura que
toda matriz real simétrica tiene vectores propios ortogonales y valores propios reales. Por eso
`np.linalg.eigh` (para matrices hermíticas) es la función correcta, y no `eig`.

### C.4 ¿Aporta algo la reducción de dimensionalidad aquí?

**No, y esa es la respuesta valiosa.** Las tres correlaciones fuera de la diagonal son muy
bajas (0.036, 0.065, 0.127): las variables son casi independientes entre sí. Cuando no hay
redundancia, no hay nada que comprimir.

El síntoma es que los tres valores propios son parecidos (1.16, 0.97, 0.87) y la primera
componente explica apenas el 38.6 %, muy cerca del 33.3 % que daría un dataset sin ninguna
estructura. Quedarse con una sola componente perdería más del 60 % de la información.

> **PCA es útil cuando las variables están correlacionadas.** Este dataset sirve justamente
> para mostrar el caso contrario, y previene el error de aplicar PCA por costumbre. Se retoma
> en la sesión 12.

## Parte D — Descenso del gradiente

### D.1–D.2 Efecto de la tasa de aprendizaje

Con 500 pasos, dos variables estandarizadas:

| $\eta$ | MSE final | $\beta_0$ | $\boldsymbol{\beta}$ |
|---|---|---|---|
| 0.001 | 1.7256 | 2.1471 | `[0.2074, 0.2086]` |
| 0.01 | 0.1357 | 3.3946 | `[0.3212, 0.3232]` |
| 0.1 | 0.1357 | 3.3947 | `[0.3213, 0.3232]` |
| 0.5 | 0.1357 | 3.3947 | `[0.3213, 0.3232]` |

Con $\eta = 0.001$ **no ha convergido**: 500 pasos no bastan. El MSE sigue en 1.73 frente a
0.136 del óptimo, y los coeficientes van a mitad de camino. No es que la tasa pequeña sea
incorrecta, es que resulta demasiado lenta para el presupuesto de pasos.

Las otras tres llegan al mismo óptimo. Aquí no aparece divergencia porque los datos están
estandarizados; ese es justamente el punto de D.4.

### D.3 Comparación con la solución exacta

| | $\beta_0$ | $\beta_1$ | $\beta_2$ |
|---|---|---|---|
| Ecuación normal | 3.3947 | 0.3213 | 0.3232 |
| Descenso ($\eta=0.1$) | 3.3947 | 0.3213 | 0.3232 |

Diferencia máxima: $1.78 \times 10^{-15}$ — precisión de máquina.

> **Pregunta para clase:** si existe solución exacta, ¿para qué el descenso del gradiente? La
> respuesta: la ecuación normal exige invertir $\mathbf{X}^\top\mathbf{X}$, con costo
> $O(p^3)$, imposible con muchas variables; y no existe forma cerrada para la regresión
> logística ni para una red neuronal. El descenso funciona en todos esos casos.

### D.4 Sin estandarizar

Con $\eta = 0.1$ y las variables crudas, el entrenamiento **diverge**: los coeficientes se
desbordan (`inf`) y NumPy emite `RuntimeWarning: overflow encountered in matmul`.

**Explicación.** `horas_estudio_semana` llega a 29.5 y `asistencia_pct` a 100. El gradiente
respecto a esos coeficientes es proporcional a esos valores, así que con la misma tasa el
paso es enorme en unas direcciones y minúsculo en otras. Geométricamente, las curvas de nivel
de la pérdida son elipses extremadamente alargadas y cada paso se pasa de largo, amplificando
el error en cada iteración.

Es el mismo fenómeno de la Parte B —las escalas dispares distorsionan la geometría del
espacio—, ahora afectando a la optimización en lugar de a las distancias. **Estandarizar
resuelve las dos cosas a la vez.**

Para que converja sin estandarizar habría que bajar $\eta$ a un valor del orden de $10^{-4}$,
y entonces las variables de escala pequeña avanzarían lentísimo.

### D.5 Curva de aprendizaje

En escala logarítmica, $\eta = 0.1$ y $\eta = 0.5$ caen abruptamente en las primeras
decenas de pasos y se aplanan; $\eta = 0.01$ desciende más despacio pero llega;
$\eta = 0.001$ todavía está bajando cuando se acaban los 500 pasos — su curva no ha llegado
a la meseta, que es la firma visual de "faltan iteraciones".

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A: vectorización correcta sin bucles; explica el cambio de similitud | 1.0 |
| B: vecinos correctos en ambos casos; explica qué variable domina | 1.0 |
| C: covarianza a mano, varianza explicada, ortogonalidad justificada | 1.0 |
| C.4: concluye que PCA **no** aporta aquí, con la correlación como evidencia | 0.5 |
| D: descenso implementado, coincide con la solución exacta | 1.0 |
| D.4: explica la divergencia conectándola con las escalas | 0.5 |
| **Total** | **5.0** |

> Las partes C.4 y D.4 valen aparte a propósito: son las que distinguen a quien entendió de
> quien solo ejecutó el código.

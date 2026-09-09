# Solución · Ejercicio 02 · VIF, y Ridge/Lasso/Elastic Net

> **Material del docente.** Todos los números provienen de ejecutar el código sobre
> `ames-housing.csv` con `random_state=42`, sobre las variables de `ej01-residuales.md`.

## Parte A — VIF

**A.1**

| Variable | VIF |
|---|---|
| `1st_flr_sf` | 4.20 |
| `total_bsmt_sf` | 3.25 |
| `2nd_flr_sf` | 3.17 |
| `full_bath` | 2.42 |
| `half_bath` | 2.13 |
| `year_built` | 1.89 |
| `fireplaces` | 1.36 |
| `lot_frontage` | 1.33 |
| `lot_area` | 1.24 |
| `open_porch_sf` | 1.15 |
| `wood_deck_sf` | 1.14 |

**A.2 — El punto central del ejercicio.** **Ninguna** variable supera 5; la más alta
(`1st_flr_sf` = 4.20) ni siquiera se acerca. Y sin embargo, `ej01-residuales.md` (D.2) ya
mostró que `full_bath` y `half_bath` tienen coeficientes de signo contraintuitivo. La lección:
el umbral de VIF > 5 es una convención sobre **una** variable a la vez, comparada contra
**todas** las demás juntas. No protege contra la colinealidad *moderada mutua* entre varios
predictores de tamaño (`total_bsmt_sf`, `1st_flr_sf`, `2nd_flr_sf`, `full_bath`, `half_bath`),
cada uno con VIF individual aceptable, que en conjunto siguen desplazándose entre sí lo
suficiente como para invertir un signo. "VIF bajo" no es sinónimo de "cada coeficiente es
interpretable con confianza" — es una condición necesaria, no suficiente.

## Parte B — Ridge y Lasso

**B.1–B.2**

| $\lambda$ | RMSE val. Ridge | RMSE val. Lasso |
|---|---|---|
| 0.01 | 33,768 | 33,768 |
| 1 | 33,766 | 33,768 |
| 10 | 33,793 | **33,763** |
| 50 | 33,988 | 33,763 |
| 100 | 34,242 | 33,767 |
| 300 | 35,152 | 33,869 |

Ridge empeora de forma monótona casi desde el principio. Lasso, en cambio, tiene un mínimo
suave alrededor de $\lambda \in [10, 50]$ — muy ligeramente mejor que en $\lambda$ cercano a
cero. Un $\lambda$ razonable: **Ridge ≈ 1** (el punto antes de que empiece a subir claramente)
y **Lasso ≈ 10-50**. Se acepta cualquier elección justificada con la curva del estudiante.

**B.3**

| $\lambda$ | `full_bath` | `half_bath` |
|---|---|---|
| 0.01 | −3,687 | −2,342 |
| 1 | −3,614 | −2,292 |
| 10 | −3,077 | −1,919 |
| 50 | −1,287 | −684 |
| **100** | **+396** | **+459** |
| 300 | +4,317 | +3,033 |
| 1000 | +8,168 | +5,258 |

El signo se corrige recién hacia $\lambda \approx 100$ — muy por encima de los $\lambda$ que
minimizan el RMSE de validación en B.2 (≈1 para Ridge). Es el hallazgo que conecta con
`03-multicolinealidad-polinomica.md`, sección 2: **arreglar el signo del coeficiente cuesta
más regularización de la que conviene para predecir**. Con el $\lambda$ que RMSE recomienda,
el coeficiente sigue siendo poco confiable para interpretación, aunque el modelo prediga bien.

## Parte C — Elastic Net

**C.1** Con `alpha=50`, Ridge alcanzó RMSE ≈ 33,988 y Lasso ≈ 33,763 — apenas se movieron de
su óptimo. `ElasticNet` con `alpha=50` da RMSE entre **54,384 y 70,551** según `l1_ratio`: un
desastre comparado con Ridge o Lasso en el mismo `alpha`. La razón (a anticipar en la
discusión): `ElasticNet` de `scikit-learn` combina ambas penalizaciones dentro del mismo
`alpha` (ver `04-regularizacion.md`, sección 4), así que un `alpha` que es "suave" para Ridge o
Lasso solos es mucho más agresivo para Elastic Net. Nunca hay que reutilizar la misma rejilla
de $\lambda$ entre métodos sin comprobarlo primero.

**C.2** Mejor combinación: `alpha=0.01`, `l1_ratio=0.9` (RMSE val ≈ 33,767) — prácticamente
sin regularización efectiva, coherente con C.1.

## Parte D — Comparación final

**D.1**

| Modelo | RMSE de prueba |
|---|---|
| OLS | \$43,342 |
| Ridge ($\lambda=50$) | \$43,394 |
| Lasso ($\lambda=10$) | **\$43,339** |
| Elastic Net (α=0.01, l1=0.9) | \$43,336 |

**D.2** Ninguno le gana a OLS de forma contundente — las diferencias son de unos pocos
dólares sobre un RMSE de 43 mil, dentro de lo que cualquier ruido de muestreo explicaría (el
notebook 06, sesión 8, da la herramienta formal para confirmarlo con una comparación pareada).
Tiene pleno sentido dado el VIF bajo de la parte A: `03-multicolinealidad-polinomica.md`
predice justamente esto — con $n$ grande frente a $p$ y sin colinealidad severa, la
regularización no tiene mucho que corregir en la predicción. Su valor aquí fue otro:
diagnosticar (parte A) y, parcialmente, estabilizar (parte B) los coeficientes, no mejorar el
error de prueba.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A.1: VIF calculado correctamente, con imputación solo desde el entrenamiento | 0.8 |
| A.2: explica por qué VIF bajo no garantiza coeficientes confiables | 1.2 |
| B: curvas de Ridge y Lasso correctas; $\lambda$ elegido y justificado | 1.0 |
| B.3: identifica que el signo se corrige con un $\lambda$ mayor al que minimiza RMSE | 1.0 |
| C.1: detecta que la escala de `alpha` de Elastic Net no es comparable a Ridge/Lasso | 0.5 |
| D.2: conecta la ausencia de mejora predictiva con el VIF bajo medido en A | 0.5 |
| **Total** | **5.0** |

> La pregunta que mejor discrimina es **A.2**: separa a quien aplicó la regla de VIF > 5 como
> receta de quien entendió qué mide realmente el VIF.

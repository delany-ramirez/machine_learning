# Solución · Ejercicio 01 · Ajuste, métricas y diagnóstico de residuales

> **Material del docente.** Todos los números provienen de ejecutar el código sobre
> `ames-housing.csv` con `random_state=42`, con las variables indicadas en el enunciado.

## Parte A — Ajuste y métricas

**A.1** RMSE de la línea base: **\$90,222**.

**A.2**

| Métrica | Valor |
|---|---|
| RMSE base | \$90,222 |
| MSE | 1.879 × 10⁹ |
| RMSE | **\$43,342** |
| MAE | \$26,821 |
| $R^2$ | 0.766 |
| $R^2$ ajustado | 0.759 |

El modelo baja el RMSE a menos de la mitad de la línea base.

**A.3** La matriz de diseño tiene **16 columnas** (11 numéricas + 5 de `foundation`
codificada, con una categoría de referencia eliminada por `drop="first"`). $R^2$ (0.766) y
$R^2$ ajustado (0.759) están cerca porque $n \approx 2340$ (80 % de 2930) es grande frente a
$p=16$ — la penalización de `01-regresion-lineal.md`, $\frac{n-1}{n-p-1}$, es casi 1 cuando
$n \gg p$. Se espera que el estudiante lo relacione explícitamente con la fórmula, no solo que
reporte los números.

## Parte B — Diagnóstico de residuales

**B.1–B.2** El gráfico de residuales vs. ajustados muestra el mismo patrón de embudo que
`02-regresion-multiple-aplicado.ipynb`: la dispersión de los residuales crece con el precio
ajustado. Es una violación del supuesto de **homocedasticidad** (supuesto 3). El modelo se
equivoca poco en viviendas baratas y mucho, en dólares absolutos, en las caras.

**B.3** Correlación entre $|\text{residual}|$ y el valor ajustado: **≈ 0.50** — más fuerte
incluso que la que puede verse en el notebook 02 sobre su propio conjunto de variables. Es
razonable que el estudiante concluya que el problema de heterocedasticidad es, si acaso, más
marcado con este subconjunto de variables (más ligado al tamaño físico bruto, con menos
variables de calidad que capturen mejor las viviendas de gama alta).

## Parte C — ¿Ayuda modelar en log(precio)?

| Métrica | Modelo directo | Modelo en log(precio) |
|---|---|---|
| RMSE | **\$43,342** | \$47,341 |
| MAE | \$26,821 | **\$24,373** |
| MAPE | 14.3 % | **13.0 %** |

**C.2** El patrón es **el mismo** que en `02-regresion-multiple-aplicado.ipynb`: modelar en
log(precio) mejora MAE y MAPE (el error típico), pero **empeora el RMSE**. La causa es la
misma — al revertir la transformación logarítmica, un error moderado en escala log se
convierte en un error grande en dólares para las viviendas más caras, y el RMSE es
extremadamente sensible a esos pocos errores grandes. Vale aceptar una respuesta que solo
reporte el patrón sin reproducir la causa exacta, pero la mejor respuesta la conecta con la
sección 6 del notebook 02.

> Si algún estudiante obtiene el patrón inverso (RMSE mejora con el log), no es un error: con
> otra semilla de split es posible que el conjunto de prueba no incluya una vivienda atípica
> tan extrema como la del notebook 02. Lo que se evalúa es que **reporte lo que realmente
> obtuvo**, no que reproduzca el número del notebook.

## Parte D — Interpretación con cautela

**D.1** Los tres coeficientes de mayor magnitud (estandarizados):

| Variable | β |
|---|---|
| `2nd_flr_sf` | +29,732 |
| `1st_flr_sf` | +28,955 |
| `year_built` | +25,015 |

Todos con signo positivo y sentido de negocio razonable: más área por piso y una construcción
más reciente suben el precio.

**D.2 — El hallazgo central del ejercicio.** `full_bath` tiene $\beta=-3{,}688$ y `half_bath`
tiene $\beta=-2{,}343$: **ambos negativos**, a pesar de que más baños debería, si acaso, subir
el precio. Es la firma de inestabilidad por colinealidad de
`03-multicolinealidad-polinomica.md`: el número de baños está correlacionado con el tamaño de
la vivienda (`1st_flr_sf`, `2nd_flr_sf`, `total_bsmt_sf`), que ya está en el modelo. El
coeficiente no mide "el efecto de un baño adicional" de forma aislada — mide el efecto de un
baño adicional *manteniendo el tamaño fijo*, lo cual invierte el signo. Son candidatos
naturales para el cálculo de VIF en el ejercicio 02.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A: `Pipeline` correcto (imputación + escalado + codificación) y las 5 métricas | 1.0 |
| A.3: relaciona $R^2$ vs. $R^2$ ajustado con $n$ y $p$, no solo reporta números | 0.5 |
| B: identifica la heterocedasticidad con evidencia (gráfico + correlación) | 1.0 |
| C.2: reporta el patrón real obtenido, con o sin la explicación causal completa | 1.0 |
| D.2: detecta el signo contraintuitivo de baños y lo conecta con multicolinealidad, sin "corregirlo" a mano | 1.5 |
| **Total** | **5.0** |

> La pregunta que mejor discrimina es **D.2**: quien no revisa los signos de todos los
> coeficientes, solo los tres más grandes, se la pierde por completo.

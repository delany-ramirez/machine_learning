# Solución · Ejercicio 03 · Interpretar el modelo de Adult Census

> **Material del docente.** Números obtenidos con la partición del ejercicio 01, el modelo
> `LGBMClassifier(n_estimators=335, learning_rate=0.03, random_state=42)` ajustado sobre
> cuatro pliegues y evaluado sobre el primero (7 815 personas), categóricas nativas. Los
> valores SHAP están en log-momios. El valor base es −2.33.

## Parte A — Tres importancias, dos ganancias

**A.1** Ordenado por SHAP:

| Variable | Ganancia | Particiones | Permutación (ΔAP) | SHAP (media $\lvert\phi\rvert$) |
|---|---|---|---|---|
| `edad` | 0.078 | 0.194 | 0.063 | 0.72 |
| `relacion` | **0.288** | 0.024 | 0.040 | 0.65 |
| `estado_civil` | 0.093 | 0.022 | 0.030 | 0.63 |
| `ganancia_capital` | 0.189 | 0.125 | **0.246** | 0.56 |
| `anos_educacion` | 0.133 | 0.102 | 0.052 | 0.44 |
| `ocupacion` | 0.077 | 0.071 | 0.033 | 0.39 |
| `horas_semana` | 0.036 | 0.110 | 0.019 | 0.29 |
| `sexo` | 0.005 | 0.017 | 0.002 | 0.15 |
| `perdida_capital` | 0.062 | 0.113 | 0.045 | 0.15 |
| `fnlwgt` | 0.021 | **0.154** | 0.003 | 0.06 |
| `raza` | 0.002 | 0.010 | 0.001 | 0.06 |
| `tipo_empleo` | 0.010 | 0.033 | 0.006 | 0.06 |
| `pais_origen` | 0.008 | 0.026 | 0.005 | 0.05 |

**A.2** `fnlwgt` es la **segunda variable por número de particiones** (15 % de todas las
particiones del modelo) y, a la vez, la décima por ganancia, la penúltima por permutación
(0.003, indistinguible de cero) y la décima por SHAP. Es el sesgo de cardinalidad de
`06-interpretabilidad.md`, sección 2, sin necesidad de plantar ruido: una variable continua
con decenas de miles de valores distintos ofrece un umbral que reduce la pérdida un poco en
casi cualquier nodo, así que el modelo parte por ella **muchas veces** con **poca ganancia
cada vez** — y nada de eso generaliza. Contar particiones es la peor de las cuatro medidas;
la ganancia lo corrige en parte; permutación y SHAP lo detectan por completo.

**A.3** `Husband` es `Male` en el **100 %** de los casos y `Wife` es `Female` en el 99.9 %;
`Husband` y `Wife` son `Married-civ-spouse` en el 100 % y el 99 %. `relacion` es, en buena
medida, `sexo × estado_civil`. Por ganancia es la primera (el modelo la usa en las
particiones de arriba porque resume dos variables en una), pero al permutarla, el modelo
recupera casi todo con `estado_civil` y `sexo`, que siguen intactas: la caída de AP es
pequeña. Es la redundancia de la sección 3 de `06-interpretabilidad.md`, con un giro: SHAP
sí le da a `relacion` una contribución grande (0.65), porque SHAP reparte entre las
variables redundantes y la permutación se la quita a todas.

**A.4** Solo el **8.2 %** de las personas tiene `ganancia_capital > 0`. Su contribución SHAP
media: **−0.24** log-momios para quienes la tienen en cero, **+2.70** para quienes la tienen
positiva, y **+5.17** para quienes tienen 5 000 o más. Es una variable que casi nunca actúa,
pero cuando actúa decide sola la predicción — y no tiene sustituto: al permutarla, ninguna
otra variable puede recuperar esa información, de ahí que sea la primera por permutación
con mucha diferencia (0.246, cuatro veces la siguiente). SHAP promedia $|\phi|$ sobre todas
las personas, y el 92 % de ceros con contribución pequeña diluye a la minoría con
contribuciones enormes. Ninguna de las dos está mal: la permutación mide **cuánto perdería
el modelo sin la variable**; la media de $|\phi|$ mide **cuánto mueve la predicción de una
persona típica**.

## Parte B — Lectura global y local con SHAP

**B.1** Enjambre: `edad` alta empuja hacia ingreso alto (y baja, muy fuerte hacia abajo);
en `relacion`, las categorías `Husband`/`Wife` empujan hacia arriba y `Own-child`,
`Not-in-family` y `Unmarried` hacia abajo (para categóricas, el color no es un gradiente:
hay que leer las categorías); `estado_civil` `Married-civ-spouse` empuja hacia arriba y
`Never-married` hacia abajo; `ganancia_capital` alta empuja muy fuerte hacia arriba, con la
cola de puntos más larga de todo el gráfico. Se acepta cualquier lectura coherente con los
signos.

**B.2** El efecto de `edad` **no es monótono**. Contribución media por tramo:

| Edad | 17–25 | 26–30 | 31–35 | 36–40 | 41–45 | 46–50 | 51–55 | 56–60 | 61–65 | > 65 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\phi_{\text{edad}}$ | −1.65 | −0.19 | +0.18 | +0.43 | +0.61 | +0.80 | +0.80 | +0.76 | +0.57 | +0.47 |

Sube con fuerza hasta los 45–55 años y después **baja**: la jubilación reduce el ingreso. Un
coeficiente logístico solo puede describir una recta; los árboles capturan la joroba sin
que nadie la pida. Colorear por `horas_semana` muestra una interacción **débil**: solo entre
los menores de 25 años, quienes trabajan 45 horas o más reciben una penalización menor por
su edad (−1.24 frente a −1.71); a partir de los 30, el color apenas separa nada. No toda
variable interactúa con todas — y el gráfico lo dice.

**B.3** El falso negativo más claro: 20 años, 8 años de educación, `Never-married`,
`Own-child`, ocupación `Other-service`, 35 horas por semana, sin ganancias de capital —
probabilidad predicha **0.002**. Contribuciones más negativas: `edad` −1.84, `relacion`
−0.72, `estado_civil` −0.58, `ocupacion` −0.43. Cada variable, por separado, dice "ingreso
bajo", y todas juntas lo dicen con mucha confianza. El modelo no tenía forma de acertar: la
persona es una excepción a un patrón que en los datos se cumple casi siempre, y ninguna de
las variables disponibles la distingue de las miles que no lo son. Se acepta cualquier caso
similar si el estudiante usó otra semilla.

## Parte C — `sexo`: qué hace el modelo y qué pasa si se quita

**C.1** Contribución SHAP media de `sexo`: **−0.22** log-momios para mujeres, **+0.12** para
hombres. Sobre el pliegue de validación con umbral 0.15:

| | n | Prevalencia real | Predichos positivos | Recall | Precisión |
|---|---|---|---|---|---|
| Hombres | 5 224 | 0.304 | 0.526 | 0.938 | 0.541 |
| Mujeres | 2 591 | 0.109 | 0.176 | 0.855 | 0.531 |

El modelo reproduce la brecha de los datos (30 % frente a 11 % de ingresos altos) y la
amplifica ligeramente en las decisiones: recibe la oferta el 53 % de los hombres y el 18 %
de las mujeres, y el recall es 8 puntos menor para ellas — a igual precisión.

**C.2** Sin `sexo`: AP 0.831 frente a 0.832 (**sin cambio**). Predichos positivos: hombres
0.521, mujeres 0.191; recall: hombres 0.933, mujeres 0.873. Las tasas se mueven uno o dos
puntos; la brecha sigue casi intacta.

**C.3** Porque `relacion` contiene el sexo: `Husband` es hombre en el 100 % de los casos y
`Wife` mujer en el 99.9 % (A.3), y `relacion` es la segunda variable por SHAP. Quitar la
columna `sexo` no quita la información — el modelo la lee en un **proxy**, y la
importancia de `sexo` era baja (0.15) justamente porque ya la tenía por otra vía. Para que
el modelo *no pudiera* usar el sexo haría falta, como mínimo, eliminar o recodificar
`relacion` (fusionar `Husband`/`Wife` en `Spouse`), y después comprobar que ninguna otra
variable ni combinación lo predice (se puede medir: entrenar un modelo para predecir `sexo`
a partir de las demás variables; si su AUC es alto, la información sigue ahí). Y aun
así, la brecha en las **decisiones** puede persistir porque las demás variables
(ocupación, horas) correlacionan con el sexo en los datos de 1994. Se acepta cualquier
respuesta que identifique el proxy y proponga medirlo; no se exige conocer la literatura de
equidad algorítmica.

**C.4** *A quien quiera usarlo:* el modelo ordena bien (AUC 0.93) y con el umbral de mínimo
costo ahorra un 14 % frente a la logística (ejercicio 02), pero sus decisiones difieren por
sexo de forma medible, y quitar la columna no lo arregla. Antes de usarlo para asignar un
producto habría que decidir explícitamente qué criterio de equidad se exige (¿misma tasa
de ofertas por grupo? ¿mismo recall?), medirlo en cada versión del modelo como se mide la
AP, y documentarlo. Además, son datos del censo de EE. UU. de **1994**: cualquier uso actual
requeriría datos actuales.

*Lo que no se puede concluir:* que el sexo **cause** una diferencia de ingresos, ni de
cuánto. SHAP explica el modelo, no el mundo: dice que, en estos datos, saber el sexo (o la
relación familiar) cambia la predicción, porque en 1994 hombres y mujeres con el mismo
perfil declaraban ingresos distintos. Las causas de eso —discriminación, ocupaciones,
horas, historia laboral no registrada— no están en el modelo. Confundir "el modelo usa X"
con "X causa Y" es el error de la sección 5 de `06-interpretabilidad.md`; en este dataset
tiene consecuencias.

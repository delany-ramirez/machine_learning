# Solución · Ejercicio 01 · Clasificación, métricas y umbral sobre Adult Census

> **Material del docente.** Todos los números provienen de ejecutar el código sobre
> `adult-census.csv` (48 842 filas) con `random_state=42`, partición estratificada 80/20 y
> `StratifiedKFold(5, shuffle=True, random_state=42)`.

## Parte A — Encuadre y diagnóstico

**A.1** Prevalencia de `ingreso_alto`: **0.239**. Faltantes: `tipo_empleo` 5.7 %, `ocupacion`
5.8 % (casi las mismas filas: quien no reporta empleo no reporta ocupación) y `pais_origen`
1.8 %. Cardinalidades: `tipo_empleo` 8, `educacion` 16, `estado_civil` 7, `ocupacion` 14,
`relacion` 6, `raza` 5, `sexo` 2, `pais_origen` 41.

**A.2** Cada valor de `educacion` corresponde a **exactamente un** valor de `anos_educacion`:
son la misma variable, una como texto y otra como entero ordinal. Se conserva
`anos_educacion` (una sola columna numérica, con orden) y se elimina `educacion` (16
columnas *one-hot* sin orden). Conservar ambas no rompe nada, pero duplica la información y
reparte la importancia entre las dos (ejercicio 03).

**A.3** 52 filas idénticas (0.1 %). A diferencia de Wine Quality —11 mediciones de laboratorio
con decimales—, aquí las 14 columnas toman valores gruesos (edad entera, categorías, horas
redondas), y dos personas distintas con el mismo perfil censal son perfectamente plausibles:
es el caso del Titanic. Además, son tan pocas que no pueden alterar ninguna métrica. Se
conservan. Se acepta eliminarlas si el estudiante lo justifica; lo que no se acepta es
hacerlo por reflejo.

**A.4** El 89.7 % de las filas es `United-States`; las otras 40 categorías se reparten el
10 % restante, muchas con menos de 50 personas. Un *one-hot* completo produce 40 columnas casi
vacías, que aportan ruido y pueden aparecer en prueba con categorías que no estaban en
entrenamiento. `min_frequency=50` agrupa las categorías raras en una sola columna
`infrequent`, y `handle_unknown="ignore"` evita el error con categorías nuevas.

## Parte B — Regresión logística en `Pipeline`

**B.1** Quedan **74 columnas** tras la codificación (6 numéricas + las categorías con al
menos 50 filas + una columna de infrecuentes por variable).

**B.2**

| Métrica | Logística (CV) |
|---|---|
| Accuracy | 0.852 |
| Precisión | 0.734 |
| Recall | 0.599 |
| F1 | 0.660 |
| AUC-ROC | 0.906 |
| AP | 0.766 |

Referencia trivial ("nadie gana más de 50 K"): accuracy **0.761**. La logística la supera
por 9 puntos — aquí, a diferencia de Wine Quality, la accuracy sí distingue algo, porque el
desbalance es menor y la señal es mucho más fuerte (AUC 0.91 frente a 0.83).

**B.3** Matriz de confusión en 0.5 (filas: real; columnas: predicho):

| | pred. 0 | pred. 1 |
|---|---|---|
| **real 0** | 27 696 | 2 028 |
| **real 1** | 3 747 | 5 602 |

Domina el **falso negativo**: se escapan 3 747 de los 9 349 positivos (recall 0.60), casi el
doble que los falsos positivos. Con umbral 0.5 el modelo es conservador.

## Parte C — Curvas y umbral

**C.1** La mayor precisión con recall $\geq 0.8$ es **0.602**. La curva PR es mucho mejor que
la de Wine Quality (AP 0.77 sobre una prevalencia de 0.24): aquí el modelo sí sirve para el
problema.

**C.2** El F1 se maximiza en el umbral **0.31**, con F1 = **0.690** (precisión 0.62, recall
0.78), frente a 0.660 en 0.5.

**C.3** Con costos 1 : 5, el umbral de mínimo costo es **0.15**, con costo 12 284. En 0.5 el
costo es 20 763: **un 69 % más caro**. Con un falso negativo cinco veces más caro que un
falso positivo, conviene ofrecer el producto a casi cualquiera con una probabilidad
razonable; el umbral por defecto deja pasar demasiados clientes valiosos.

## Parte D — Pesos de clase

**D.1**

| Modelo | AUC-ROC | AP | Recall en 0.5 | F1 en 0.5 | Mejor F1 (umbral libre) |
|---|---|---|---|---|---|
| Logística | 0.906 | 0.765 | 0.599 | 0.660 | 0.690 |
| Logística + `class_weight="balanced"` | 0.906 | 0.764 | 0.847 | 0.680 | 0.690 |

**D.2** El recall en 0.5 pasa de 0.60 a 0.85 y el F1 en 0.5 sube dos puntos — pero AUC-ROC,
AP y el mejor F1 alcanzable son **idénticos** hasta la tercera cifra. Los pesos no cambiaron
el orden en que el modelo clasifica a las personas; solo desplazaron las probabilidades, y
eso ya lo hace el umbral de C.3 sin tocar el modelo. Misma conclusión que
`02-clasificacion-aplicado.ipynb`, sección 7, con 10 veces más datos: en un modelo lineal,
balancear es mover el umbral con otro nombre.

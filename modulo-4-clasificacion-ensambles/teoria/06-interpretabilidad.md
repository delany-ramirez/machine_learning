# 06 · Interpretabilidad: importancia por permutación, valores de Shapley y SHAP

**Módulo 4 · Sesión 11** — Boosting e interpretabilidad

## Objetivos

- Distinguir las tres preguntas que se esconden bajo "interpretar un modelo": qué variables
  importan globalmente, cómo depende la predicción de cada una, y por qué el modelo predijo
  lo que predijo para **este** caso.
- Conocer las tres herramientas del módulo —importancia por impureza, por permutación y
  SHAP— y, sobre todo, **dónde se equivoca cada una**, medido.
- Entender los valores de Shapley lo suficiente para leer un gráfico SHAP sin sobreinterpretarlo.
- Saber qué **no** es una explicación: correlación con la predicción no es causalidad sobre
  el mundo.

## 1. Tres preguntas distintas

Un ensamble de 300 árboles no se lee. Pero "interpretar" no es una sola cosa:

| Pregunta | Alcance | Herramientas |
|---|---|---|
| ¿Qué variables usa el modelo, y cuánto? | Global | MDI, permutación, SHAP promedio |
| ¿Cómo cambia la predicción al cambiar una variable? | Global, por variable | Dependencia parcial (PDP), curvas ICE, dependencia SHAP |
| ¿Por qué esta predicción? | Local | SHAP por observación (cascada), LIME |

Un modelo lineal responde las tres con sus coeficientes (una razón de momios por variable,
`01-regresion-logistica.md`). Para árboles y ensambles hacen falta herramientas
*post hoc*, y ninguna es gratis.

## 2. Importancia por impureza (MDI)

La que traen los bosques de fábrica (`feature_importances_`; en LightGBM,
`importance_type="gain"`): para cada variable, la suma de la reducción de impureza (o de
pérdida) en todas las particiones donde se usó, ponderada por el tamaño del nodo, promediada
sobre los árboles. Es gratis —se acumula al entrenar— y por eso es la primera gráfica que
todo el mundo hace.

**Dónde se equivoca**, medido en `07-interpretabilidad-aplicado.ipynb`: se añaden al Wine
Quality dos columnas de ruido puro, una continua (gaussiana) y una binaria, y se ajusta un
Random Forest. La MDI pone al **ruido continuo por encima de cuatro variables reales**
(`free_sulfur_dioxide`, `ph`, `citric_acid`, `fixed_acidity`) y le da 6 veces más
importancia que al ruido binario, que es exactamente igual de inútil. La razón: con 4256
valores distintos siempre hay algún umbral que reduce la impureza por azar, y con árboles
sin podar esos umbrales se usan. La MDI **premia la cardinalidad** y **mide sobre
entrenamiento**: cuánto usó el modelo cada variable para ajustar, no cuánto le sirve para
generalizar. Es la explicación de lo que el módulo 2 vio en el Titanic (`age` por encima del
sexo).

Sirve para una primera mirada. No sirve para descartar variables ni para explicarle nada a
nadie.

## 3. Importancia por permutación

Breiman (2001) para Random Forest; hoy, para cualquier modelo (`sklearn.inspection.permutation_importance`).
Sobre un conjunto de **validación** (no de entrenamiento, no de prueba): se mide la métrica,
se **baraja** una columna —rompiendo su relación con $y$ y dejando intactas las demás—, se
vuelve a medir, y la importancia es la caída. Se repite varias veces para promediar el azar
del barajado.

Ventajas sobre la MDI: es independiente del modelo, mide sobre datos no vistos y en la
métrica que importa (aquí, AP), y **no premia la cardinalidad**: las dos columnas de ruido
obtienen una importancia indistinguible de cero (ligeramente negativa, que es la firma del
ruido).

**Dónde se equivoca.** Barajar una columna crea filas **imposibles** (la densidad de un vino
dulce con el alcohol de uno seco), y si la variable tiene una compañera muy correlacionada,
el modelo sigue leyendo en la compañera lo que la permutación rompió. El notebook 07 lo mide
en dos escenarios:

- Con las correlaciones reales del dataset (`density`–`alcohol` −0.67, `density`–`residual_sugar`
  0.52), permutar las tres **juntas** vale 0.217 frente a 0.208 de la suma de las tres por
  separado: un 4 % de información compartida que no se atribuye a ninguna. El problema
  existe, pero es pequeño.
- Con una **copia casi exacta** de `alcohol` añadida al modelo, la importancia por
  permutación de `alcohol` se desploma de 0.104 a 0.017 (la copia se lleva 0.059), y las dos
  juntas recuperan 0.137. La variable más importante del problema parece prescindible.

La permutación no inventa importancia, como la MDI, pero la **reparte mal** entre variables
casi redundantes. Cuando se sabe que hay grupos correlacionados, se permutan por grupo. Y en
general: importancia cero no significa "irrelevante para el problema", significa "redundante
para este modelo" — `tipo` (tinto/blanco) vale cero en todas las medidas porque las
variables de azufre y la acidez volátil ya lo dicen.

## 4. Valores de Shapley y SHAP

### La idea

Shapley (1953), teoría de juegos cooperativos: ¿cómo repartir la ganancia de una coalición
entre sus miembros de forma justa? La respuesta única que cumple cuatro axiomas razonables
(eficiencia, simetría, jugador nulo, aditividad) es el promedio de la contribución marginal
de cada jugador sobre **todos los órdenes** posibles en que podrían haberse unido:

$$
\phi_j = \sum_{S \subseteq \{1..p\} \setminus \{j\}} \frac{|S|!\,(p - |S| - 1)!}{p!}
\left[ f(S \cup \{j\}) - f(S) \right]
$$

Lundberg y Lee (2017) lo aplican a modelos: los "jugadores" son las variables, la "ganancia"
es la predicción de un caso concreto menos la predicción base (la esperada sin conocer
ninguna variable), y $f(S)$ es la predicción usando solo las variables de $S$. El valor
SHAP $\phi_j$ de la variable $j$ para la observación $i$ es cuánto movió esa variable la
predicción de ese caso. Por el axioma de **eficiencia**:

$$
f(x_i) = \phi_0 + \sum_{j=1}^p \phi_{ij}
$$

Las contribuciones **suman exactamente** la predicción. Ninguna de las otras dos
importancias tiene esa propiedad, y es lo que permite pasar de "qué importa" a "cuánto aportó
aquí". `07-interpretabilidad-aplicado.ipynb` lo verifica: la diferencia entre
$\phi_0 + \sum_j \phi_{ij}$ y el log-momio del modelo es de $10^{-14}$.

### Cómo se calcula

La fórmula exacta es exponencial en $p$. Para árboles, **TreeExplainer** (Lundberg et al.,
2020) la calcula de forma exacta en tiempo polinómico, aprovechando la estructura del árbol;
para boosting es muy rápido (851 vinos × 615 árboles en menos de un segundo). Para modelos
arbitrarios, **KernelExplainer** la aproxima por muestreo, y es lento. En la práctica, SHAP
es la herramienta de los ensambles de árboles y de las redes (DeepExplainer); para modelos
lineales, los coeficientes ya son valores de Shapley.

En clasificación, los $\phi$ están en la escala de **log-momios** (la salida cruda del
modelo antes de la sigmoide), no de probabilidades. Un $\phi = +1.7$ multiplica los momios
por 5.5, sea cual sea el punto de partida; en probabilidad, ese mismo $\phi$ mueve más o
menos según dónde se esté en la sigmoide (`01-regresion-logistica.md`, sección 2).

### Cuatro gráficos

| Gráfico | Qué muestra | Pregunta |
|---|---|---|
| Barras (media de $\lvert\phi_j\rvert$) | Importancia global | ¿Qué variables? |
| Enjambre (*beeswarm*) | Un punto por observación y variable: $\phi$ en el eje $x$, valor de la variable en el color | ¿Qué variables, y en qué **dirección**? |
| Dependencia (*scatter*) | $\phi_j$ contra $x_j$, coloreado por la variable con la que más interactúa | ¿Cómo depende, y de qué otra variable? |
| Cascada (*waterfall*) | Los $\phi_{ij}$ de una observación, de la base a la predicción | ¿Por qué **este** caso? |

Lo que el notebook 07 lee en ellos sobre Wine Quality: `alcohol` domina, con un cruce por
cero cerca de 10.7 % y una contribución casi lineal en log-momios entre 9.5 y 13 %; para el
mismo alcohol, los vinos más densos reciben menos — una interacción `alcohol × density` que
un modelo lineal necesitaría como término explícito. Y en el falso negativo más claro —un
vino bueno para los catadores con 9.3 % de alcohol—, `alcohol` resta 1.7 log-momios y
`chlorides` otro 1.0: la explicación local no arregla el error, pero dice qué tendría que ser
distinto para que la predicción cambiara.

### Dependencia parcial (PDP) e ICE

El **gráfico de dependencia parcial** fija $x_j$ en cada valor de una malla para *todas* las
observaciones, predice, y promedia. Es más simple que SHAP y también responde "cómo depende",
pero (a) promedia sobre combinaciones imposibles, igual que la permutación, y (b) el
promedio puede no describir a nadie: en el notebook 07, la curva promedio de `alcohol` sube
de 0.03 a 0.3, mientras que las **curvas individuales** (ICE, una por vino) muestran que para
la mayoría de los vinos subir el alcohol no mueve la probabilidad y para una minoría la
dispara hasta casi 1. Cuando las ICE se abren en abanico hay interacciones, y la dependencia
SHAP es la forma de verlas con color.

## 5. Lo que una explicación no es

Todas las herramientas de este documento explican **el modelo**, no el mundo. Que
`alcohol` sea la variable más importante significa que el modelo la usa para separar los
vinos que los catadores puntuaron alto; no significa que añadir alcohol a un vino lo mejore.
Tres razones para no dar ese salto:

1. **Correlación, no intervención.** El alcohol correlaciona con la madurez de la uva, la
   región, el precio y la técnica de vinificación. El modelo no distingue cuál de ellas
   mueve la puntuación.
2. **Redundancia.** Una importancia de cero (`tipo`) no significa irrelevancia; significa
   que otras variables ya llevan la información. Quitar una variable importante y
   reentrenar puede dar un modelo casi igual de bueno que usa otras.
3. **Fugas.** Una variable derivada del objetivo (`alive` en el Titanic, módulo 2) sería la
   variable "más importante" de cualquier modelo. La interpretabilidad **detecta** fugas,
   precisamente porque una variable con importancia sospechosamente alta merece la pregunta
   "¿esto se conoce en el momento de predecir?".

Ese tercer uso —auditar el modelo antes de desplegarlo— es el más valioso en la práctica, y
es la razón por la que la entrega E4 del proyecto integrador exige una sección de
interpretación.

## Resumen

| Herramienta | Mide | Dónde se equivoca (medido) | Cuándo usarla |
|---|---|---|---|
| MDI | Uso de cada variable al entrenar | Premia la cardinalidad: ruido continuo por encima de 4 variables reales | Primera mirada; nunca para descartar |
| Permutación | Caída de la métrica de validación al barajar | Reparte mal entre variables casi redundantes (copia de `alcohol`: 0.104 → 0.017) | Importancia global honesta; por grupos si hay correlación |
| SHAP | Contribución de cada variable a cada predicción; suma exacta | Escala de log-momios; costoso fuera de los árboles | Global con dirección, dependencia con interacción, explicación local |
| PDP / ICE | Predicción promedio (o individual) al mover una variable | Combinaciones imposibles; el promedio puede no describir a nadie | Complemento rápido; las ICE delatan interacciones |

**Notebook:** `07-interpretabilidad-aplicado.ipynb`.

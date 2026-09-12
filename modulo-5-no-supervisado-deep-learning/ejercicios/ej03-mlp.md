# Ejercicio 03 · Retropropagación con dos capas, y cuándo la red no gana

**Módulo 5 · Sesión 13** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Extender la retropropagación del notebook 05 a **dos capas ocultas** y
> verificarla; y medir, con la comparación pareada, qué hace un MLP sobre dos datasets
> que ya conoces —uno donde la verdad es lineal, otro tabular grande— frente a los
> modelos de los módulos 3 y 4. El resultado no está decidido de antemano: hay que
> medirlo.

## Contexto

Reutiliza `adelante`, `atras`, `gradiente_numerico` y `entrenar` de
`05-mlp-intuicion.ipynb`, y `entrenar_mlp` / `MLPClasificador` de
`06-mlp-pytorch-aplicado.ipynb`. Datos: `make_moons` (parte A),
`../datos/rendimiento-estudiantes.csv` (parte B) y `../datos/adult-census.csv` (parte C;
`python datos/descargar-adult-census.py` si no lo tienes).

Semilla 42; `torch.manual_seed(42)` antes de construir cada red. Entrega un notebook
`ej03-<tu-apellido>.ipynb`.

## Parte A — Dos capas ocultas a mano (25 min)

**A.1** Escribe las ecuaciones de la pasada hacia adelante para un MLP con dos capas
ocultas de tamaños $h_1$ y $h_2$, activación $\tanh$ en ambas y salida sigmoide:
$\mathbf{Z}_1, \mathbf{H}_1, \mathbf{Z}_2, \mathbf{H}_2, \mathbf{z}_3, \hat{\mathbf{p}}$.

**A.2** Deriva las ecuaciones de la retropropagación. Parte de
$\boldsymbol{\delta}_3 = \hat{\mathbf{p}} - \mathbf{y}$ y escribe
$\boldsymbol{\Delta}_2$ y $\boldsymbol{\Delta}_1$ en función de la capa siguiente. La única
línea nueva respecto al notebook 05 es la que pasa de $\boldsymbol{\Delta}_2$ a
$\boldsymbol{\Delta}_1$: ¿qué matriz multiplica y por qué transpuesta?

**A.3** Implementa `adelante2` y `atras2` en NumPy. Sobre 300 puntos de `make_moons`
(ruido 0.2), con $h_1 = 6$, $h_2 = 4$ y pesos iniciales `rng.normal(0, 0.5, ...)`, verifica
el gradiente de **todos** los parámetros contra diferencias finitas ($\epsilon = 10^{-5}$).
Reporta el error relativo máximo. Si es mayor que $10^{-6}$, hay un error en A.2 o A.3.

**A.4** *(sin código)* Con $L$ capas ocultas de anchura $h$, ¿cuántas multiplicaciones
matriz-por-matriz hace la pasada hacia atrás, y cómo se compara con la pasada hacia
adelante? ¿Qué hay que guardar de la pasada hacia adelante para poder hacer la de atrás?

## Parte B — Cuando la verdad es lineal (20 min)

`rendimiento-estudiantes.csv` se generó con un proceso **lineal** más ruido gaussiano
(módulo 1). Predice `nota_final` a partir de los seis predictores de siempre (`edad`,
`estrato`, `trabaja`, `promedio_anterior`, `horas_estudio_semana`, `asistencia_pct`).

**B.1** Con `RepeatedKFold(n_splits=5, n_repeats=2, random_state=42)`, RMSE de: regresión
lineal (S6), `ExtraTreesRegressor(300)`, y un MLP de regresión en PyTorch (32-16, ReLU,
salida lineal, `MSELoss`, Adam, early stopping sobre un 15 % interno del entrenamiento,
objetivo estandarizado). Reporta media ± ee para los tres.

**B.2** Comparación pareada: MLP − lineal y Extra-Trees − lineal, con error estándar y
cociente. ¿Alguno de los dos modelos flexibles gana al lineal? ¿Por qué no deberían
poder, y por qué pierden en vez de empatar?

**B.3** La desviación típica de `nota_final` es 0.59. ¿Qué fracción de esa varianza
explica el modelo lineal, y cuánto de lo que queda es ruido irreducible? (Pista: el
módulo 1 generó los datos con ruido conocido; si no lo recuerdas, razona con el RMSE.)

## Parte C — Adult Census: ¿más red ayuda? (30 min)

Misma partición 80/20 estratificada y CV de 5 pliegues del ejercicio 01 del módulo 4.
Categóricas en *one-hot* para la red y la logística; nativas para LightGBM.

**C.1** Dos MLP con early stopping sobre un 15 % interno: (a) una capa de 64 con dropout
0.1; (b) 256-128 con dropout 0.3. AP media ± ee y segundos por pliegue, junto a LightGBM
por defecto y la regresión logística.

**C.2** Comparación pareada de cada MLP contra LightGBM. ¿La red grande mejora a la
pequeña? ¿Alguna se acerca a LightGBM?

**C.3** Repite el MLP (b) haciendo el early stopping **sobre el pliegue de validación
de la CV** (el mismo sobre el que se calcula la AP), como hacía la sección 3 del notebook
06 antes de corregirlo. Reporta la diferencia pareada con la versión correcta. ¿Cuánto
infla la fuga la AP? ¿Es relevante frente a la distancia con LightGBM?

**C.4** Anota las épocas en las que paró cada pliegue del MLP (b). ¿Por qué para tan
pronto con 39 000 filas? ¿Qué diría eso sobre entrenar 100 épocas fijas sin validación?

## Entrega

Notebook, y una recomendación de tres líneas para el proyecto integrador: ¿en qué
condiciones probarías una red neuronal sobre tu caso, y qué comparación exigirías
antes de adoptarla?

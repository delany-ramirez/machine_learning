# Ejercicio 02 · Pipeline, características y fuga de datos

**Módulo 2 · Sesión 5** · Tiempo estimado: **90 min** · Con código

> **Objetivo.** Convertir las decisiones del ejercicio 01 en un `Pipeline` que se pueda
> desplegar, crear características nuevas y **medir** si aportan, y comprobar de primera mano
> cuánto infla cada tipo de fuga de datos.

## Punto de partida

Seguimos con `../datos/matriculas-sucio.csv` y con el objetivo `admitido`.

Empieza aplicando la **limpieza estructural** del ejercicio 01 — la que no aprende nada de los
datos y por tanto puede hacerse antes de partir:

```python
datos["promedio_pregrado"] = pd.to_numeric(
    datos["promedio_pregrado"].str.replace(",", ".", regex=False))
datos["puntaje_examen"] = pd.to_numeric(datos["puntaje_examen"], errors="coerce")
datos["fecha_solicitud"] = pd.to_datetime(datos["fecha_solicitud"], format="%d/%m/%Y")
datos["ingresos_hogar"] = datos["ingresos_hogar"].replace(-999, np.nan)
datos["estado_civil"] = (datos["estado_civil"].str.strip().str.lower()
                         .str.replace("ó", "o", regex=False))
datos.loc[(datos["edad"] > 100) | (datos["edad"] < 0), "edad"] = np.nan
datos = datos.drop_duplicates(subset="id_solicitud", keep="first")
```

Entrega un notebook `ej02-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — El pipeline (30 min)

**A.1** Separa `X` e `y`. Justifica en una línea por qué eliminas `admitido_texto` y
`id_solicitud` de las predictoras.

**A.2** Aparta el conjunto de prueba (20 %, estratificado). Hazlo **antes** de cualquier otra
cosa.

**A.3** Escribe una función `caracteristicas(df)` que cree, **fila a fila**:

- `fue_entrevistado`: si `nota_entrevista` no es nulo.
- `falta_ingresos`: si `ingresos_hogar` es nulo.
- `log_ingresos`: logaritmo de los ingresos.
- `mes_solicitud`: extraído de la fecha.

y elimine `fecha_solicitud` y `nota_entrevista`.

Explica por qué esta función **puede** aplicarse antes de partir sin causar fuga.

**A.4** Construye un `ColumnTransformer` con tratamientos separados:

- Numéricas: imputar con la mediana + estandarizar.
- Categóricas: imputar con la moda + one-hot con `handle_unknown="ignore"` y `drop="first"`.

**A.5** Móntalo todo en un `Pipeline` con una regresión logística y evalúalo con validación
cruzada de 5 pliegues sobre el conjunto de entrenamiento. Compara contra la **referencia
trivial** (predecir siempre la clase mayoritaria).

## Parte B — La fuga evidente (10 min)

**B.1** Añade `admitido_texto` (codificada como 0/1) a las variables predictoras y vuelve a
evaluar con validación cruzada.

**B.2** ¿Qué accuracy obtienes? ¿Qué habrías concluido si no supieras qué es esa columna?

**B.3** Escribe una función `detectar_sospechosas(X, y, umbral=0.95)` que devuelva las columnas
cuya correlación absoluta con el objetivo supere el umbral. Aplícala. Explica por qué esta
comprobación debe ser rutinaria y cuál es su límite.

## Parte C — ¿Cuánto importa el orden? (20 min)

Ahora mide, no supongas.

**C.1** Repite la evaluación de A.5, pero **imputando y escalando fuera del pipeline**: aplica
`SimpleImputer` y `StandardScaler` sobre todo `X` antes de la validación cruzada.

**C.2** Compara el resultado con el de A.5. ¿Cuánto se infla la métrica?

**C.3** Ahora la selección de características. Compara:

- `SelectKBest(f_classif, k=5)` aplicado sobre **todo** `X` antes de la validación cruzada.
- El mismo selector **dentro** del `Pipeline`.

**C.4** Con los tres resultados (C.2 y C.3), ordena los tipos de fuga por gravedad **según tus
propias mediciones**. ¿Coincide con lo que viste en el notebook 03? Si el efecto de la
selección te sale más pequeño que allí, explica por qué (pista: ¿cuántas variables candidatas
hay en cada caso?).

## Parte D — ¿Aportan las variables nuevas? (15 min)

**D.1** Evalúa con validación cruzada dos pipelines: uno con las variables originales y otro
con las cuatro que creaste en A.3.

**D.2** ¿La diferencia supera a la desviación entre pliegues? ¿Puedes afirmar que las
variables nuevas ayudan?

**D.3** Propón **una** variable adicional que creas que sí puede aportar, con una justificación
del dominio. Impleméntala y mídela. Reporta el resultado **aunque sea negativo**.

## Parte E — Evaluación final y artefacto (15 min)

**E.1** Entrena el pipeline elegido con todo el entrenamiento y evalúalo **una sola vez** en el
conjunto de prueba. Compara con la referencia trivial.

**E.2** Examina los coeficientes de la regresión logística (usa
`get_feature_names_out()` del preprocesador). ¿Las variables más influyentes coinciden con lo
que sugería el EDA del ejercicio 01?

**E.3** Guarda el pipeline con `joblib`. Recárgalo y predice sobre **un solicitante nuevo**
que pases en crudo, con `NaN` incluido en alguna columna. Verifica que funciona.

**E.4** Prueba a predecir con un solicitante cuyo `programa` sea `"Arquitectura"` (una
categoría que no existe en los datos). ¿Qué pasa? ¿Qué habría pasado sin
`handle_unknown="ignore"`?

## Entrega

Notebook ejecutado, con las respuestas en Markdown. Se valoran especialmente **C.4** (el
razonamiento sobre las magnitudes) y **D.2** (reconocer cuándo no se puede afirmar una mejora).

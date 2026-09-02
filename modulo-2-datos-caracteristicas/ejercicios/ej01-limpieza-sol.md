# Solución · Ejercicio 01 · Diagnóstico y limpieza

> **Material del docente.** Todos los números provienen de ejecutar el código sobre
> `matriculas-sucio.csv` generado con `SEMILLA = 7`. Si el estudiante regeneró el archivo con
> `generar-matriculas-sucio.py`, deben coincidir exactamente.

## Resumen de los defectos plantados

| # | Problema | Columna | Dónde se evalúa |
|---|---|---|---|
| 1 | Fuga de datos | `admitido_texto` | A.3 |
| 2 | Faltante disfrazado (`-999`) | `ingresos_hogar` | B.2 |
| 3 | Faltantes como texto (`N/D`, `-`, vacío) | `puntaje_examen` | B.2 |
| 4 | Faltante MAR | `experiencia_anios` | B.3 |
| 5 | Faltante MNAR | `nota_entrevista` | B.4 |
| 6 | Duplicados reales y aparentes | — | C |
| 7 | Outliers por error de registro | `edad` | D.1 |
| 8 | Outliers legítimos + asimetría | `ingresos_hogar` | D.2, D.3 |
| 9 | Inconsistencia de formato | `estado_civil` | D.4 |
| 10 | Número con coma decimal, como texto | `promedio_pregrado` | A.1 |
| 11 | Fecha como texto | `fecha_solicitud` | D.5 |

## Parte A — Perfilado

**A.1** 620 filas × 13 columnas. Tipos incorrectos:

| Columna | Tipo leído | Debería ser | Por qué |
|---|---|---|---|
| `promedio_pregrado` | `object` | `float` | Usa **coma decimal** (`"3,85"`) |
| `puntaje_examen` | `object` | `float` | Contiene `"N/D"` y `"-"` |
| `fecha_solicitud` | `object` | `datetime` | Formato `dd/mm/yyyy` |

Conversión correcta:

```python
datos["promedio_pregrado"] = pd.to_numeric(
    datos["promedio_pregrado"].str.replace(",", ".", regex=False)
)
datos["puntaje_examen"] = pd.to_numeric(datos["puntaje_examen"], errors="coerce")
datos["fecha_solicitud"] = pd.to_datetime(datos["fecha_solicitud"], format="%d/%m/%Y")
```

> Sin `errors="coerce"`, la conversión de `puntaje_examen` **falla**. Ese error es la pista de
> que hay faltantes disfrazados.

**A.2** Lo evaluable es que aparezca la fila **"disponible al decidir"**. `nota_entrevista`
merece discusión: existe solo para quienes fueron entrevistados y es posterior a la solicitud,
así que su uso depende de en qué punto del proceso se quiera predecir.

**A.3** `admitido_texto` es **fuga de datos**: es `admitido` escrito en texto.

```python
pd.crosstab(datos["admitido"], datos["admitido_texto"])
```

|  | Admitido | No admitido |
|---|---|---|
| **0** | 0 | 174 |
| **1** | 446 | 0 |

Correspondencia perfecta. Un modelo con esa columna alcanzaría el 100 % de acierto y sería
inútil.

## Parte B — Faltantes

**B.1** Declarados: `experiencia_anios` 85 (13.7 %), `nota_entrevista` 412 (66.5 %).

**B.2 — Los disfrazados.**

| Columna | Disfraz | Cantidad |
|---|---|---|
| `ingresos_hogar` | `-999` | **57** |
| `puntaje_examen` | vacío | 15 |
| `puntaje_examen` | `"-"` | 11 |
| `puntaje_examen` | `"N/D"` | 4 |

En total 30 faltantes en `puntaje_examen` y 57 en `ingresos_hogar` que `isna()` no veía.

```python
datos["ingresos_hogar"] = datos["ingresos_hogar"].replace(-999, np.nan)
```

> **El caso de `-999` es el más peligroso** del ejercicio: es numérico, no genera ningún error
> y arrastra la media de ingresos hacia abajo. Se detecta solo mirando el mínimo. Conviene
> insistir en clase: `describe()` antes de cualquier cosa.

**B.3 — `experiencia_anios` es MAR.**

| modalidad | tasa de faltantes |
|---|---|
| Presencial | 0.057 |
| Virtual | **0.305** |

Falta cinco veces más en modalidad virtual. No es MCAR: depende de una variable observada.
**Imputar por la mediana de cada modalidad**, no por la mediana global. Añadir indicador de
ausencia es recomendable.

**B.4 — `nota_entrevista` es MNAR.**

- Falta el **66.5 %**.
- Tasa de admisión: **67.3 %** entre quienes tienen nota (208 casos) frente al **74.3 %** entre
  quienes no la tienen (412 casos).

El valor falta porque **a esa persona no se la entrevistó**: la ausencia depende del propio
proceso, no de otra variable observada. Es MNAR.

Decisión: **no imputar**. Imputar el 66 % de una columna es inventarse los datos. Lo correcto
es crear la binaria `fue_entrevistado` y, si se quiere conservar la nota, tratarla como una
variable disponible solo para un subconjunto.

> **Detalle que merece discusión.** Los entrevistados se admiten **menos**, lo cual es
> contraintuitivo. La hipótesis razonable es que se entrevista precisamente a los casos
> dudosos: los expedientes claramente buenos se admiten sin entrevista. Eso convierte a
> `fue_entrevistado` en un indicador de "caso dudoso" — informativo, pero también una posible
> fuga por retroalimentación, porque refleja una decisión previa del propio proceso que se
> quiere modelar. Se acepta cualquier respuesta que note la tensión.

**B.5 — Tabla de decisiones**

| Columna | % faltante | Mecanismo | Decisión |
|---|---|---|---|
| `experiencia_anios` | 13.7 % | MAR (modalidad) | Mediana por modalidad + indicador |
| `nota_entrevista` | 66.5 % | MNAR | No imputar; crear `fue_entrevistado` |
| `ingresos_hogar` | 9.2 % (tras destapar `-999`) | Probablemente MNAR (no declarar ingresos) | Mediana + indicador |
| `puntaje_examen` | 4.8 % | MCAR aparente | Mediana |
| `promedio_pregrado` | 0 % | — | Solo conversión de tipo |

## Parte C — Duplicados

| Medida | Valor |
|---|---|
| Filas completamente duplicadas | **12** |
| `id_solicitud` repetidos | **12** |
| Filas idénticas ignorando `id_solicitud` | **20** |

**C.4 — La interpretación**, que es lo que se evalúa:

- Las **12** filas con `id_solicitud` repetido son **duplicados reales**: la misma solicitud
  cargada dos veces. Se eliminan.
- Los **20 − 12 = 8** casos restantes tienen **id distinto** y todo lo demás igual: son
  solicitudes **diferentes** que coinciden en todos sus valores. Se **conservan**.

```python
datos = datos.drop_duplicates(subset="id_solicitud", keep="first")   # 620 -> 608
```

> **El error a cazar** es usar `drop_duplicates()` sin `subset`, o peor,
> `drop_duplicates(subset=[todo menos id])`, que borraría 20 filas y perdería 8 solicitudes
> legítimas. La existencia de `id_solicitud` es lo que permite responder; sin ella el problema
> sería indecidible, como en el Titanic.

## Parte D — Extremos e inconsistencias

**D.1 — `edad`.** Hay **6 filas** con valores imposibles: `210` y `-5`.

Son claramente errores de registro. Opciones válidas: convertirlos a `NaN` e imputar, o
eliminar las filas (son 6 de 620, ~1 %). Lo que no vale es dejarlos: contaminan cualquier
media y cualquier escalado.

**D.2 — `ingresos_hogar`.** Sobre los 563 valores válidos: mediana ≈ 2.23 M, máximo ≈ 71.6 M.

La regla del IQR marca varias decenas de outliers en la cola alta. Los más extremos
(45–90 M) son **legítimos**: los ingresos tienen una distribución muy asimétrica y esos valores
corresponden a hogares de altos ingresos, no a errores. **No se eliminan.**

Contrasta con `edad = 210`, que es imposible. La distinción entre "extremo" e "imposible" es el
punto del apartado.

**D.3 — Transformación.** Logaritmo. La asimetría cae de un valor alto (>5) a cerca de 0.5–1.
Se conserva toda la información y se limita la influencia de la cola.

```python
datos["log_ingresos"] = np.log1p(datos["ingresos_hogar"])
```

**D.4 — `estado_civil`.** Aparecen **10 categorías** donde debería haber 3:

`Soltero`, `Casado`, `Union libre`, `Soltero ` (con espacio), `casado`, `soltero`, ` SOLTERO`,
`CASADO `, `Unión libre` (con tilde), `union libre`.

```python
datos["estado_civil"] = (
    datos["estado_civil"].str.strip().str.lower()
    .str.replace("ó", "o", regex=False)
)
```

Resultado: `soltero` 347, `casado` 179, `union libre` 94.

> Nótese que hay tres fuentes de inconsistencia a la vez: mayúsculas, espacios y tildes. Una
> sola de las tres operaciones no basta.

**D.5 — `fecha_solicitud`.** Variables derivadas razonables: mes, semana del año, día de la
semana, días transcurridos desde la apertura de la convocatoria, o si la solicitud llegó en la
última semana del plazo (posible indicador de improvisación).

## Parte E — EDA

**E.1** Tasa de admisión por programa y modalidad, con conteos. Lo evaluable es que **aparezca
el conteo**: sin él, una tasa no es interpretable.

**E.2** Los admitidos tienen promedio y puntaje visiblemente más altos. Es coherente con el
proceso generador: la probabilidad de admisión depende de `promedio_pregrado`,
`puntaje_examen` y `experiencia_anios`.

**E.3** Las correlaciones más altas con `admitido` corresponden a `promedio_pregrado` y
`puntaje_examen`, seguidas de `experiencia_anios`. `edad`, `ingresos_hogar` y las derivadas de
la fecha deben salir cercanas a cero — **y eso también es un hallazgo**: significa que el
ingreso del hogar no influye en la admisión, algo que conviene poder afirmar con datos.

> Si un estudiante calcula la correlación **sin** haber limpiado `edad` (con los 210) o
> `ingresos_hogar` (con los `-999`), obtendrá valores distorsionados. Es una buena forma de
> comprobar quién hizo la limpieza antes del análisis.

**E.4** Se acepta cualquier presentación correcta: discretizar `promedio_pregrado` en tramos y
cruzar con `modalidad`, o comparar la pendiente por modalidad. En este dataset la interacción
**no es fuerte** —el proceso generador es aditivo— y detectar su ausencia es tan válido como
detectar su presencia, siempre que se justifique con la evidencia.

## Rúbrica sugerida

| Criterio | Puntos |
|---|---|
| A: tipos incorrectos identificados y convertidos; diccionario con disponibilidad temporal | 0.7 |
| A.3: detecta la fuga y la demuestra con tabla cruzada | 0.5 |
| B.2: encuentra **los dos** faltantes disfrazados (`-999` y texto) | 0.8 |
| B.3–B.4: identifica correctamente MAR y MNAR con evidencia numérica | 0.8 |
| C.4: distingue duplicados reales de aparentes y usa `subset="id_solicitud"` | 0.8 |
| D.1–D.2: separa "imposible" de "extremo legítimo" | 0.6 |
| D.4: normaliza las tres fuentes de inconsistencia | 0.3 |
| E: análisis con conteos; interpreta las correlaciones bajas | 0.5 |
| **Total** | **5.0** |

> Las preguntas que mejor discriminan son **B.2** (los faltantes disfrazados) y **C.4** (los
> duplicados). Quien aplica recetas automáticas falla las dos.

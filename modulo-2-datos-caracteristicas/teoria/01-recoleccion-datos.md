# 01 · Recolección de datos

**Módulo 2 · Sesión 4**

> **Objetivos.** Distinguir datos estructurados de no estructurados; conocer las fuentes
> habituales y cómo se accede a cada una; entender qué es un diccionario de datos y por qué
> es obligatorio; y aplicar los criterios legales y éticos que condicionan el uso de datos.

## 1. El dato no aparece: hay que ir a buscarlo

En un curso, el dataset viene dado. En un proyecto real, conseguirlo suele ser la fase más
larga, y las decisiones que se toman aquí condicionan todo lo demás. Un modelo no puede
compensar datos que no contienen la información necesaria.

Antes de recolectar nada, hay dos preguntas de la sesión 2 que ya deberían estar respondidas:
qué se quiere predecir, y **qué información estará disponible en el momento de predecir**.
La segunda determina qué datos tiene sentido recoger.

## 2. Datos estructurados y no estructurados

### Estructurados

Organizados en un formato predefinido: filas y columnas, con un tipo definido por columna.
Bases de datos relacionales, hojas de cálculo, CSV.

- Cada **fila** es una unidad de observación.
- Cada **columna** es una variable con un tipo y un significado.
- Se consultan con SQL y se procesan directamente con pandas.

Es el caso del 90 % de los problemas de este curso, y también de la mayoría de los problemas
reales en la industria.

### No estructurados

Sin formato predefinido: texto libre, imágenes, audio, video, correos, publicaciones en redes.
Constituyen la mayor parte de los datos que se generan en el mundo.

Requieren un paso previo de **representación**: convertirlos en vectores numéricos antes de
poder modelarlos. Ahí es donde el deep learning tiene su ventaja decisiva (sesión 13).

### Semiestructurados

JSON y XML: tienen estructura, pero no tabular. Es lo que devuelve la mayoría de las APIs.
Normalmente hay que "aplanarlos" a una tabla (`pd.json_normalize`).

## 3. Fuentes y cómo se accede

| Fuente | Herramienta | Cuidado principal |
|---|---|---|
| Archivos (CSV, Excel, Parquet) | `pd.read_csv`, `read_excel`, `read_parquet` | Codificación, separadores, tipos mal inferidos |
| Bases de datos | SQL + `pd.read_sql` | Filtrar en el servidor, no traer la tabla entera |
| APIs | `requests` + JSON | Límites de tasa, paginación, autenticación |
| Web scraping | `requests` + BeautifulSoup | Legalidad, fragilidad, todo llega como texto |
| Datos abiertos | Portales oficiales | Verificar vigencia y metodología |

### Archivos: los problemas de siempre

Leer un CSV parece trivial y no lo es:

- **Codificación.** En Latinoamérica es frecuente encontrar archivos en `latin-1` o `cp1252`
  en vez de `utf-8`. Un error de codificación se manifiesta como tildes rotas.
- **Separador decimal.** En español la coma suele ser el separador decimal y el punto el de
  miles: `1.234,56`. Si pandas lo lee con la convención anglosajona, la columna entera queda
  como texto.
- **Tipos mal inferidos.** Un código de programa como `"01"` se convierte en el número `1` y
  pierde el cero. Se evita con `dtype={"codigo": str}`.
- **Valores faltantes disfrazados.** `"N/D"`, `"-"`, `"NULL"`, `"999"` o una celda vacía con
  un espacio. Se declaran con `na_values=[...]`.

### Bases de datos

La regla es **filtrar y agregar en el servidor**, no traer todo a memoria. Una consulta que
devuelve lo necesario es más rápida y consume menos recursos que `SELECT *` seguido de un
filtro en pandas.

Cuidado con las credenciales: nunca se escriben en el código ni se suben a Git (sesión 2). Se
leen de variables de entorno o de un archivo de configuración excluido en `.gitignore`.

### APIs

La forma preferible de obtener datos de un servicio externo: interfaz estable, documentada y
autorizada. Aspectos a considerar: autenticación (tokens), **límites de tasa** (cuántas
peticiones por minuto), **paginación** (los resultados vienen por bloques) y el formato de la
respuesta.

## 4. Web scraping

Extraer datos directamente del HTML de una página. Es el último recurso, no el primero: es
frágil (la página cambia y el código se rompe), lento y a menudo está restringido.

**Antes de raspar:**

1. ¿Existe una **API oficial**? Casi siempre sí.
2. ¿Están los datos en un **portal de datos abiertos**?
3. ¿Qué dice `robots.txt` del sitio?
4. ¿Qué dicen los términos de servicio?

**Al raspar:**

- Identificarse con un `User-Agent` descriptivo.
- Esperar entre peticiones. Un bucle sin pausas es indistinguible de un ataque.
- Guardar el HTML crudo en local, para no repetir peticiones al ajustar el código.
- Nunca extraer datos personales sin base legal.

**Después de raspar:** todo llega como texto. La conversión de tipos es parte obligatoria del
proceso, no un detalle posterior.

## 5. El diccionario de datos

Un dataset sin documentación es una fuente de errores. Para cada columna hay que registrar:

| Campo | Ejemplo |
|---|---|
| Nombre | `asistencia_pct` |
| Significado | Porcentaje de sesiones asistidas en el semestre |
| Tipo | Numérica continua |
| Unidad / rango | Porcentaje, 0–100 |
| Cómo se mide | Registro automático de la plataforma |
| **Cuándo está disponible** | Al cierre de cada semana |
| Valores faltantes | Codificados como celda vacía |

La fila **"cuándo está disponible"** es la que previene la fuga de datos, y es la que casi
nunca se documenta.

> **Un caso real del curso.** El dataset del Titanic incluye una columna `alive` con los
> valores `yes`/`no`. Leyendo el diccionario se descubre en treinta segundos que es la
> variable objetivo escrita en texto. Sin diccionario, se descubre cuando el modelo alcanza el
> 100 % de acierto — o peor, no se descubre.

## 6. Consideraciones legales y éticas

### Protección de datos personales

En Colombia rige la **Ley 1581 de 2012** (habeas data) y en Europa el **RGPD**. Ambas
comparten principios que afectan directamente a un proyecto de ML:

- **Finalidad.** Los datos recogidos para un fin no pueden usarse para otro distinto sin
  nueva autorización.
- **Minimización.** Recoger solo lo necesario. Más columnas no es mejor si no las necesitas.
- **Autorización.** El titular debe haber consentido el tratamiento.
- **Seguridad.** Protegerlos frente a accesos no autorizados.

En la práctica: **anonimizar** (eliminar identificadores directos) o **seudonimizar**
(sustituirlos por códigos) tan pronto como sea posible. Y tener presente que la anonimización
no es infalible: cruzando varias variables se puede reidentificar a una persona.

### Representatividad y sesgo

Una pregunta que hay que hacerse durante la recolección, no después:

> ¿A quién representan estos datos, y a quién dejan fuera?

Si el histórico solo contiene estudiantes de jornada diurna, el modelo no sabrá nada de los
nocturnos. Si registra decisiones tomadas con un criterio sesgado, el modelo aprenderá ese
sesgo y lo aplicará con eficiencia. El problema no se corrige con más datos del mismo tipo:
se corrige revisando cómo se generaron.

### Procedencia

Documentar de dónde salió cada dato, con qué licencia y en qué fecha. Es parte de la
reproducibilidad (sesión 2) y lo que permite responder a una auditoría.

## Para recordar

- Conseguir los datos suele ser la fase más larga del proyecto.
- Estructurado, semiestructurado y no estructurado piden herramientas distintas.
- Leer un CSV bien exige atender a codificación, separadores, tipos y faltantes disfrazados.
- Prefiere siempre una API oficial al scraping.
- El diccionario de datos es obligatorio, y su fila más importante es **cuándo está
  disponible cada variable**.
- La ley 1581 y el RGPD condicionan qué datos puedes usar y cómo.

## Notebooks relacionados

- [`../notebooks/02-webscraping-aplicado.ipynb`](../notebooks/02-webscraping-aplicado.ipynb) 🔵
  — extracción de tablas con BeautifulSoup y limpieza de datos raspados.

## Documento siguiente

- [`02-limpieza-y-calidad.md`](02-limpieza-y-calidad.md) — faltantes, duplicados y outliers.

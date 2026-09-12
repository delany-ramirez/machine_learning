# 03 · Versionado de código y datos: Git y DVC

**Módulo 1 · Sesión 2**

> **Objetivos.** Manejar el flujo básico de Git aplicado a un proyecto de datos; decidir qué
> se versiona y qué no; entender por qué Git no sirve para datasets grandes y cómo DVC
> resuelve el problema; y dejar montado el repositorio del proyecto integrador.

## 1. El problema

Sin control de versiones, un proyecto de ML termina así:

```
analisis.ipynb
analisis_v2.ipynb
analisis_v2_bueno.ipynb
analisis_FINAL.ipynb
analisis_FINAL_corregido.ipynb
datos_limpios_ESTE_SI.csv
```

Y con preguntas sin respuesta: ¿qué código produjo el modelo que está en producción? ¿con qué
versión de los datos? ¿qué cambió entre el experimento que dio 0.82 y el que dio 0.79?

El control de versiones responde esas preguntas. En ML hay que responderlas **dos veces**:
una para el código y otra para los datos.

## 2. Git: lo mínimo indispensable

Git es un sistema de control de versiones distribuido. Guarda **instantáneas** del proyecto
(*commits*), cada una con su autor, fecha y mensaje.

### Conceptos

| Concepto | Qué es |
|---|---|
| **Repositorio** | La carpeta del proyecto con todo su historial |
| **Commit** | Una instantánea del proyecto en un momento dado |
| **Área de preparación** (*staging*) | Antesala: lo que entrará en el próximo commit |
| **Rama** (*branch*) | Una línea de desarrollo paralela |
| **Remoto** | Copia del repositorio en un servidor (GitHub, GitLab) |

### El flujo diario

```bash
git init
```

```bash
git status
```

```bash
git add src/entrenar.py
```

```bash
git commit -m "Agrega linea base con random forest"
```

```bash
git log --oneline
```

El ciclo real es siempre el mismo: modificar archivos → `git add` lo que forma un cambio
coherente → `git commit` con un mensaje que explique **por qué**, no qué.

| Mensaje pobre | Mensaje útil |
|---|---|
| `cambios` | `Corrige fuga de datos: escala dentro del pipeline` |
| `update` | `Agrega VIF para diagnosticar multicolinealidad` |
| `arreglo` | `Fija semilla en la particion train/test` |

### Volver atrás

Ver cómo estaba el proyecto en un commit anterior:

```bash
git checkout <hash-del-commit>
```

Y regresar a la última versión:

```bash
git checkout main
```

Esta es la capacidad que hace auditable un proyecto: poder reconstruir el estado exacto que
produjo un resultado.

## 3. Qué versionar y qué no

En un proyecto de ML la respuesta no es "todo".

| Se versiona en Git | No se versiona |
|---|---|
| Código: `.py`, `.ipynb` | Datasets grandes |
| `pyproject.toml`, `uv.lock`, `requirements.txt` | Modelos entrenados (`.joblib`, `.pkl`) |
| Configuración, documentación | Resultados regenerables |
| Datasets pequeños (< 1 MB) | Entornos virtuales (`.venv/`) |
| Scripts que descargan o generan datos | Credenciales, tokens, contraseñas |

Lo que se excluye se declara en `.gitignore`:

```
.venv/
__pycache__/
datos/crudos/*.csv
modelos/*.joblib
mlruns/
.env
```

Tres razones para excluir:

1. **Tamaño.** Git guarda el historial completo. Un CSV de 500 MB modificado diez veces
   convierte el repositorio en algo inmanejable.
2. **Formato binario.** Git no sabe hacer diff de un `.joblib`: guarda una copia entera cada
   vez.
3. **Seguridad.** Una credencial en el historial de Git sigue ahí aunque borres el archivo
   después.

### Notebooks y Git

Un `.ipynb` es un JSON que incluye las salidas: tablas, gráficas codificadas en base64,
números de ejecución. Si haces commit con las salidas puestas, cada ejecución genera un diff
gigantesco e ilegible aunque no hayas cambiado una línea de código.

**Limpia las salidas antes de hacer commit** (`Kernel → Restart & Clear Output`). Es una
convención de este repositorio y una buena práctica general.

## 4. DVC: control de versiones para datos

Git no puede con un dataset de 2 GB, pero el dataset también necesita versionarse: sin saber
con qué datos se entrenó un modelo, el resultado no es reproducible.

**DVC** (Data Version Control) resuelve esto con una idea simple y elegante:

> El archivo grande se guarda en un almacenamiento aparte. En Git queda solo un archivo de
> texto diminuto —un puntero con el **hash** del archivo— que sí se puede versionar.

Es exactamente la idea del hash SHA-256 del notebook 02, automatizada e integrada con Git.

### Flujo básico

```bash
dvc init
```

```bash
dvc add datos/crudos/dataset.csv
```

Esto crea `datos/crudos/dataset.csv.dvc`, un archivo de texto de unas pocas líneas que
contiene el hash, el tamaño y la ruta. Además añade el CSV al `.gitignore`. Lo que se versiona
en Git es el puntero:

```bash
git add datos/crudos/dataset.csv.dvc datos/crudos/.gitignore
```

```bash
git commit -m "Agrega dataset v1"
```

Y los datos se envían al almacenamiento configurado:

```bash
dvc remote add -d almacen /ruta/compartida
```

```bash
dvc push
```

### Recuperar el estado completo

Quien clone el repositorio obtiene el código de Git y los datos de DVC:

```bash
git clone <repo>
```

```bash
dvc pull
```

Y para volver a un experimento antiguo con **sus** datos:

```bash
git checkout <hash-del-commit>
```

```bash
dvc checkout
```

Ese par de comandos reconstruye código y datos exactamente como estaban. Es la pieza que
faltaba para que un experimento de ML sea reproducible de verdad.

### Qué más hace DVC

DVC también permite definir *pipelines* — etapas encadenadas (preparar → entrenar → evaluar)
que solo se re-ejecutan cuando cambian sus entradas. No lo usaremos en el curso, pero conviene
saber que existe si el proyecto crece.

## 5. Estructura recomendada para el proyecto integrador

```
proyecto/
├── README.md              # qué hace, cómo se ejecuta, resultados principales
├── requirements.txt       # dependencias con versión fijada
├── .gitignore
├── .dvc/                  # configuración de DVC
├── datos/
│   ├── crudos/            # solo lectura, versionado con DVC
│   └── procesados/        # regenerable
├── notebooks/             # exploración
├── src/                   # código estable y reutilizable
├── modelos/               # artefactos entrenados
└── resultados/            # métricas y figuras
```

## 6. Errores frecuentes

| Error | Consecuencia | Prevención |
|---|---|---|
| Commit de credenciales | Quedan en el historial para siempre | `.gitignore` desde el primer commit |
| Commit de notebooks con salidas | Diffs ilegibles, repositorio pesado | Limpiar salidas antes del commit |
| Un solo commit gigante al final | Se pierde la trazabilidad | Commits pequeños y frecuentes |
| Modificar los datos crudos | Imposible rehacer el trabajo | Datos crudos de solo lectura |
| Mensajes de commit vacíos de contenido | El historial no sirve para nada | Explicar el porqué del cambio |

## Para recordar

- Git versiona el **código**; DVC versiona los **datos**. Hacen falta los dos.
- Se versiona lo pequeño y textual; se excluye lo grande, binario y secreto.
- Limpia las salidas de los notebooks antes de hacer commit.
- `git checkout` + `dvc checkout` reconstruyen un experimento completo.
- Los datos crudos no se modifican nunca.

## Notebooks relacionados

- [`../notebooks/02-proyecto-reproducible-aplicado.ipynb`](../notebooks/02-proyecto-reproducible-aplicado.ipynb)
  — hashes, artefactos y la ficha de un experimento.

## Documento siguiente

- [`04-algebra-lineal.md`](04-algebra-lineal.md) — fundamentos matemáticos.

# Guía de entorno

Cómo dejar tu máquina lista para ejecutar todo el material del curso. Elige **una** de las dos
opciones; no necesitas ambas.

> Esta es la **versión corta**, para quien ya maneja `uv` y Git. El tutorial paso a paso
> (instalar Git y uv en cada sistema operativo, VS Code, Colab como plan B, FAQ y tabla
> extensa de problemas) está en
> [`../modulo-0-instalacion/README.md`](../modulo-0-instalacion/README.md).

## Opción A — uv (recomendada)

Requiere [uv](https://docs.astral.sh/uv/getting-started/installation/). No hace falta tener
Python instalado: uv descarga la versión fijada en `.python-version` (3.11).

```bash
uv sync
uv run python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
uv run jupyter lab
```

`uv sync` crea `.venv/` en la raíz del repositorio con las versiones exactas de `uv.lock`.
`uv run <comando>` ejecuta cualquier cosa dentro del entorno sin activarlo; si prefieres
activarlo, `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate` (macOS/Linux).

Para actualizar el entorno cuando cambien `pyproject.toml` o `uv.lock` (después de un
`git pull`), el mismo comando:

```bash
uv sync
```

Para añadir un paquete: `uv add <paquete>` (actualiza `pyproject.toml` y `uv.lock`).

## Opción B — venv + pip

Requiere Python 3.11 instalado en el sistema. No fija versiones exactas: usa `requirements.txt`,
que replica la lista de `pyproject.toml` con versiones mínimas.

```bash
python -m venv .venv
```

Activar el entorno:

```bash
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar y registrar el kernel:

```bash
pip install -r requirements.txt
python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
jupyter lab
```

En Linux, `pip install torch` descarga la variante con CUDA (varios GB). Para la versión CPU
que usa el curso: `pip install torch --index-url https://download.pytorch.org/whl/cpu` antes
de instalar `requirements.txt`.

## Verificar la instalación

Desde la raíz del repositorio:

```bash
uv run modulo-0-instalacion/verificar-entorno.py
```

(con la opción B, `python modulo-0-instalacion/verificar-entorno.py` con el entorno activo).
Revisa Python, que el intérprete sea el `.venv` del repositorio, cada paquete de
`pyproject.toml`, el kernel de Jupyter, Git y uv, e indica cómo corregir lo que falte. La
comprobación rápida equivalente en una línea:

```bash
uv run python -c "import numpy, pandas, sklearn, matplotlib, statsmodels, xgboost, lightgbm, shap, optuna, torch; print('Entorno OK')"
```

Debe imprimir `Entorno OK` sin errores.

## Notas por herramienta

### PyTorch (módulo 5)

El curso solo necesita **CPU**: los ejemplos son pequeños y están pensados para correr en un
portátil. `pyproject.toml` toma `torch` del índice oficial de PyTorch para CPU
(`download.pytorch.org/whl/cpu`), así que en Linux no se descargan las librerías CUDA. En
macOS solo hay ruedas para Apple Silicon (arm64) a partir de PyTorch 2.3; en un Mac Intel
usa Colab para la sesión 13.

Si tienes GPU NVIDIA y quieres usarla, hazlo en un entorno aparte siguiendo la
[guía de uv para PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/); no
modifiques el `pyproject.toml` del curso. No es necesario para ninguna actividad evaluable.

### LightGBM (módulo 4)

En macOS la rueda de pip necesita la librería OpenMP: `brew install libomp`. Sin ella,
`import lightgbm` mata el kernel.

### MLflow (módulo 6)

MLflow guarda los experimentos en la carpeta `mlruns/`, que está excluida en `.gitignore`.
Para abrir la interfaz:

```bash
uv run mlflow ui
```

Queda disponible en <http://localhost:5000>.

### DVC (módulo 1, sesión 2)

DVC se usa para versionar datos junto al código. Se inicializa dentro de un repositorio git
ya existente:

```bash
uv run dvc init
```

La sesión 2 explica el flujo completo. No inicialices DVC en este repositorio del curso: se
practica en el repositorio del **proyecto integrador** de cada estudiante.

### Docker (módulo 6)

Solo se necesita en la sesión 14, para empaquetar la API. Instala
[Docker Desktop](https://www.docker.com/products/docker-desktop/). Si no puedes instalarlo,
la sesión incluye una alternativa que ejecuta la API directamente con `uvicorn`.

## Datasets

Los datasets pequeños ya están en la carpeta `datos/` de cada módulo. Los grandes se
descargan con el script correspondiente, por ejemplo:

```bash
uv run modulo-4-clasificacion-ensambles/datos/descargar-adult-census.py
```

Los scripts son idempotentes: si el archivo ya existe, no lo vuelven a bajar. Los datos
descargados están excluidos de git, así que cada quien los genera en su máquina.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| El notebook no encuentra los paquetes | Jupyter está usando otro kernel | Selecciona el kernel `Python (ml-curso)` en la esquina superior derecha; si apunta a otro Python, vuelve a ejecutar el `ipykernel install` de arriba con `uv run` |
| `ModuleNotFoundError` en la terminal | El comando corrió con el Python del sistema | Antepón `uv run`, o activa `.venv` |
| `FileNotFoundError` al leer un CSV | Se abrió Jupyter desde una carpeta distinta | Abre `uv run jupyter lab` desde la raíz del repositorio; las rutas son relativas a la carpeta del notebook |
| `uv sync` se corta a mitad de la descarga | Red inestable | Vuelve a ejecutarlo: retoma desde la caché |
| Gráficas que no aparecen | Backend de matplotlib | Añade `%matplotlib inline` en la primera celda |
| Error de codificación al leer CSV con tildes | Encoding del sistema | Usa `pd.read_csv(ruta, encoding="utf-8")` |

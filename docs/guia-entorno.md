# Guía de entorno

Cómo dejar tu máquina lista para ejecutar todo el material del curso. Elige **una** de las dos
opciones; no necesitas ambas.

> Esta es la **versión corta**, para quien ya maneja conda y Git. El tutorial paso a paso
> (instalar Git y Miniconda en cada sistema operativo, VS Code, Colab como plan B, FAQ y
> tabla extensa de problemas) está en
> [`../modulo-0-instalacion/README.md`](../modulo-0-instalacion/README.md).

## Opción A — conda (recomendada)

Requiere [Miniconda](https://docs.conda.io/en/latest/miniconda.html) o Anaconda.

```bash
conda env create -f environment.yml
conda activate ml-curso
python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
jupyter lab
```

La creación del entorno tarda varios minutos la primera vez. Si el solver de conda se demora
demasiado, instala `mamba` y usa `mamba env create -f environment.yml`.

Para actualizar el entorno cuando cambie `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

## Opción B — venv + pip

Requiere Python 3.11 instalado en el sistema.

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

## Verificar la instalación

Con el entorno activo y desde la raíz del repositorio:

```bash
python modulo-0-instalacion/verificar-entorno.py
```

Revisa Python, cada paquete de `environment.yml`, el kernel de Jupyter y Git, e indica cómo
corregir lo que falte. La comprobación rápida equivalente en una línea:

```bash
python -c "import numpy, pandas, sklearn, matplotlib, statsmodels, xgboost, lightgbm, shap, optuna, torch; print('Entorno OK')"
```

Debe imprimir `Entorno OK` sin errores. Si falla en `torch`, revisa la sección de PyTorch.

## Notas por herramienta

### PyTorch (módulo 5)

El curso solo necesita **CPU**: los ejemplos son pequeños y están pensados para correr en un
portátil. `environment.yml` instala `pytorch-cpu` desde conda-forge (no la rueda de pip),
porque la rueda de pip se instala pero **falla al importar en Windows dentro de un entorno
conda** (`OSError: ... shm.dll`). Si ves ese error, con el entorno activo:

```bash
pip uninstall -y torch
```

```bash
conda install -c conda-forge pytorch-cpu
```

En la opción B (venv + pip) la rueda de pip funciona con normalidad.

Si tienes GPU NVIDIA y quieres usarla, instala la variante CUDA siguiendo el selector oficial
en <https://pytorch.org/get-started/locally/>. No es necesario para ninguna actividad
evaluable.

### MLflow (módulo 6)

MLflow guarda los experimentos en la carpeta `mlruns/`, que está excluida en `.gitignore`.
Para abrir la interfaz:

```bash
mlflow ui
```

Queda disponible en <http://localhost:5000>.

### DVC (módulo 1, sesión 2)

DVC se usa para versionar datos junto al código. Se inicializa dentro de un repositorio git
ya existente:

```bash
dvc init
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
python modulo-4-clasificacion-ensambles/datos/descargar-adult-census.py
```

Los scripts son idempotentes: si el archivo ya existe, no lo vuelven a bajar. Los datos
descargados están excluidos de git, así que cada quien los genera en su máquina.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| El notebook no encuentra los paquetes | Jupyter está usando otro kernel | Selecciona el kernel `Python (ml-curso)` en la esquina superior derecha |
| `FileNotFoundError` al leer un CSV | Se abrió Jupyter desde una carpeta distinta | Abre `jupyter lab` desde la raíz del repositorio; las rutas son relativas a la carpeta del notebook |
| `conda` tarda horas resolviendo | Solver clásico | Usa `mamba`, o `conda config --set solver libmamba` |
| Gráficas que no aparecen | Backend de matplotlib | Añade `%matplotlib inline` en la primera celda |
| Error de codificación al leer CSV con tildes | Encoding del sistema | Usa `pd.read_csv(ruta, encoding="utf-8")` |

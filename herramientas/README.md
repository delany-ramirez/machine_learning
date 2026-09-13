# Herramientas de construcción

Utilidades para producir el material del curso. No son contenido para los estudiantes.

## `percent2ipynb.py`

Convierte un `.py` en formato *percent* a un notebook `.ipynb`, sin dependencias externas.

Los notebooks del curso se escriben primero como `.py` en formato percent porque así se
pueden **ejecutar como script** para verificar que corren sin errores, y el diff en git es
legible. Después se convierten al `.ipynb` que se versiona.

Formato de entrada:

```python
# %% [markdown]
# # Título
# Texto en markdown, con "# " al inicio de cada línea.

# %%
codigo_python()
```

Convertir a notebook:

```bash
python herramientas/percent2ipynb.py entrada.py salida.ipynb
```

Extraer solo el código, para ejecutarlo y verificar que no falla:

```bash
python herramientas/percent2ipynb.py entrada.py --solo-codigo
```

El kernel que declara es `ml-curso`, el del entorno de `pyproject.toml` (`.venv` creado con `uv sync`).

Al convertir, inserta automáticamente la **celda de arranque para Google Colab** (ver abajo)
justo después del título, deduciendo la carpeta del módulo de la ruta de salida. En
`--solo-codigo` esa celda se omite, porque sus `!` y `%` solo son válidos en IPython.

## `celda_colab.py`

Inserta (o reemplaza) en cada notebook la primera celda de código, etiquetada
`colab-arranque`, que en Colab clona el repositorio y se ubica en la carpeta del notebook
para que `../datos` exista; en local no hace nada. Sin dependencias externas.

```bash
python herramientas/celda_colab.py                       # los 29 modulo-*/notebooks/*.ipynb
python herramientas/celda_colab.py ruta/al/notebook.ipynb  # solo esos
```

- Es **idempotente**: si el notebook ya tiene la celda, la reemplaza; no toca salidas, metadatos
  ni el kernel.
- Añade `%pip install -q ...` solo con los paquetes que el notebook importa y Colab no trae
  (`PAQUETES_NO_EN_COLAB`: `optuna`, `shap`, `umap-learn`, `mlflow`). Si un notebook nuevo usa
  otro paquete ausente en Colab, añadirlo a ese diccionario.
- Si el notebook lee un CSV que no se versiona (`DATOS_DESCARGABLES`, hoy solo
  `adult-census.csv`), la celda ejecuta el script `descargar-*.py` cuando el archivo no existe.

`percent2ipynb.py` importa este módulo, así que la celda es la misma por los dos caminos.

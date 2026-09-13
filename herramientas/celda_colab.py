"""Inserta en cada notebook la celda de arranque para Google Colab, sin dependencias.

El portal del curso abre cada .ipynb en Colab cargando solo ese archivo desde GitHub,
asi que las rutas relativas (../datos/...) no existen. La celda de arranque clona el
repositorio y se ubica en la carpeta del notebook; en local no hace nada porque el
modulo `google.colab` no esta importado.

Reglas:
- Va justo despues de la celda markdown de titulo (si la hay), antes de la primera
  celda de codigo, con metadata {"tags": ["colab-arranque"]}.
- Es idempotente: si ya existe una celda con esa etiqueta, la reemplaza.
- Instala con `%pip` solo los paquetes que el notebook importa y Colab no trae
  (PAQUETES_NO_EN_COLAB), deducidos de los imports del propio notebook.
- Si el notebook lee un CSV que no se versiona (DATOS_DESCARGABLES), ejecuta el script
  de descarga solo si el archivo no existe.
- No toca nada mas del notebook: ni salidas, ni metadatos, ni el kernel.

Uso:
    python herramientas/celda_colab.py                 # todos los modulo-*/notebooks/*.ipynb
    python herramientas/celda_colab.py ruta.ipynb ...  # solo esos
"""
import json
import re
import sys
from pathlib import Path

REPO_URL = "https://github.com/delany-ramirez/machine_learning"
DESTINO_COLAB = "/content/machine_learning"
ETIQUETA = "colab-arranque"
MARCA = "# Arranque para Google Colab"

# modulo importado -> paquete pip. Solo lo que Colab no trae de serie.
PAQUETES_NO_EN_COLAB = {
    "optuna": "optuna",
    "shap": "shap",
    "umap": "umap-learn",
    "mlflow": "mlflow",
}

# CSV excluido de git (ver .gitignore) -> script que lo genera, relativo a notebooks/.
DATOS_DESCARGABLES = {
    "../datos/adult-census.csv": "../datos/descargar-adult-census.py",
}

RAIZ = Path(__file__).resolve().parent.parent


def modulos_importados(codigo):
    return {m.split(".")[0] for m in re.findall(r"^\s*(?:from|import)\s+([\w.]+)", codigo, re.M)}


def es_celda_arranque(fuente):
    """True si el texto de una celda es la celda de arranque (empieza con MARCA)."""
    return fuente.lstrip().startswith(MARCA)


def celda_arranque(carpeta, codigo=""):
    """Texto de la celda para un notebook en `carpeta` (relativa a la raiz del repo,
    p. ej. 'modulo-3-regresion-evaluacion/notebooks'). `codigo` es el codigo del resto
    del notebook, del que se deducen los paquetes y datos extra."""
    lineas = [
        f"{MARCA} (en local no hace nada): trae el repositorio para que",
        "# ../datos y ../src existan. Ejecútala antes que cualquier otra celda.",
        "import sys",
        'if "google.colab" in sys.modules:',
        f"    !git clone -q --depth 1 {REPO_URL} {DESTINO_COLAB}",
        f"    %cd {DESTINO_COLAB}/{carpeta}",
    ]
    faltan = sorted(p for m, p in PAQUETES_NO_EN_COLAB.items() if m in modulos_importados(codigo))
    if faltan:
        lineas.append(f"    %pip install -q {' '.join(faltan)}")
    for csv, script in DATOS_DESCARGABLES.items():
        if csv in codigo:
            lineas += [
                "    from pathlib import Path",
                f'    if not Path("{csv}").exists():  # no está en el repositorio, se descarga',
                f"        !python {script}",
            ]
    return "\n".join(lineas)


def a_fuente(cuerpo):
    lineas = cuerpo.split("\n")
    return [ln + "\n" for ln in lineas[:-1]] + [lineas[-1]]


def construir_celda(carpeta, codigo=""):
    return {
        "cell_type": "code",
        "metadata": {"tags": [ETIQUETA]},
        "source": a_fuente(celda_arranque(carpeta, codigo)),
        "execution_count": None,
        "outputs": [],
    }


def es_arranque(celda):
    return ETIQUETA in celda.get("metadata", {}).get("tags", []) or (
        celda["cell_type"] == "code" and es_celda_arranque("".join(celda["source"]))
    )


def insertar(nb, carpeta):
    """Devuelve las celdas con la de arranque puesta (o reemplazada) en su sitio."""
    celdas = [c for c in nb["cells"] if not es_arranque(c)]
    codigo = "\n".join("".join(c["source"]) for c in celdas if c["cell_type"] == "code")
    nueva = construir_celda(carpeta, codigo)
    pos = 0
    if celdas and celdas[0]["cell_type"] == "markdown" and "".join(celdas[0]["source"]).lstrip().startswith("#"):
        pos = 1
    nb["cells"] = celdas[:pos] + [nueva] + celdas[pos:]
    return nb


def carpeta_de(ruta):
    """'modulo-N-.../notebooks' a partir de la ruta de un .ipynb (relativa o absoluta)."""
    ruta = Path(ruta).resolve()
    try:
        return ruta.parent.relative_to(RAIZ).as_posix()
    except ValueError:
        return ruta.parent.as_posix()


def procesar(ruta):
    raw = Path(ruta).read_bytes()
    nueva_linea = "\r\n" if b"\r\n" in raw else "\n"
    nb = json.loads(raw.decode("utf-8"))
    insertar(nb, carpeta_de(ruta))
    texto = json.dumps(nb, ensure_ascii=False, indent=1) + "\n"
    Path(ruta).write_bytes(texto.replace("\n", nueva_linea).encode("utf-8"))


if __name__ == "__main__":
    rutas = sys.argv[1:] or sorted(RAIZ.glob("modulo-*/notebooks/*.ipynb"))
    for ruta in rutas:
        procesar(ruta)
        print(f"{Path(ruta).name}: celda '{ETIQUETA}' -> %cd {DESTINO_COLAB}/{carpeta_de(ruta)}")

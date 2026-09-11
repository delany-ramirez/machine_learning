"""Verifica que el entorno del curso quedó bien instalado.

Uso, con el entorno `ml-curso` activo y desde la raíz del repositorio:

    python modulo-0-instalacion/verificar-entorno.py

Revisa la versión de Python, que cada paquete de environment.yml esté instalado con una
versión suficiente, que el kernel de Jupyter esté registrado y que Git funcione. No modifica
nada. Si algo falla, copia la salida completa y envíasela al docente.
"""

import os
import platform
import shutil
import subprocess
import sys
from importlib import metadata

# (nombre para importar, nombre del paquete en pip/conda, versión mínima, módulo del curso)
PAQUETES = [
    ("numpy", "numpy", "1.26", "todo el curso"),
    ("pandas", "pandas", "2.2", "todo el curso"),
    ("scipy", "scipy", "1.13", "todo el curso"),
    ("sklearn", "scikit-learn", "1.5", "todo el curso"),
    ("statsmodels", "statsmodels", "0.14", "módulo 3"),
    ("matplotlib", "matplotlib", "3.8", "todo el curso"),
    ("seaborn", "seaborn", "0.13", "todo el curso"),
    ("jupyterlab", "jupyterlab", "4.2", "todo el curso"),
    ("ipykernel", "ipykernel", "6.29", "todo el curso"),
    ("ipywidgets", "ipywidgets", "8.1", "todo el curso"),
    ("requests", "requests", "2.32", "módulo 2"),
    ("bs4", "beautifulsoup4", "4.12", "módulo 2"),
    ("lxml", "lxml", "5.2", "módulo 2"),
    ("xgboost", "xgboost", "2.1", "módulo 4"),
    ("lightgbm", "lightgbm", "4.5", "módulo 4"),
    ("imblearn", "imbalanced-learn", "0.12", "módulo 4"),
    ("shap", "shap", "0.46", "módulo 4"),
    ("optuna", "optuna", "3.6", "módulo 3"),
    ("umap", "umap-learn", "0.5", "módulo 5"),
    ("torch", "torch", "2.4", "módulo 5"),
    ("mlflow", "mlflow", "2.16", "módulo 6"),
    ("fastapi", "fastapi", "0.115", "módulo 6"),
    ("uvicorn", "uvicorn", "0.30", "módulo 6"),
    ("dvc", "dvc", "3.55", "módulo 1"),
    ("ucimlrepo", "ucimlrepo", "0.0.7", "datasets"),
]

# Paquetes que environment.yml instala con pip (no existen con ese nombre en conda-forge).
SOLO_PIP = {"ucimlrepo"}
# Paquetes cuyo nombre en conda-forge no coincide con el de pip.
NOMBRE_CONDA = {"torch": "pytorch-cpu"}

PYTHON_MINIMO = (3, 11)
PYTHON_MAXIMO_EXCLUSIVO = (3, 12)
NOMBRE_ENTORNO = "ml-curso"

ok, advertencias, fallos = [], [], []


def _version_tupla(texto):
    partes = []
    for trozo in texto.split("."):
        digitos = ""
        for c in trozo:
            if c.isdigit():
                digitos += c
            else:
                break
        if not digitos:
            break
        partes.append(int(digitos))
    return tuple(partes)


def reporta(estado, mensaje, ayuda=None):
    icono = {"OK": "[OK]  ", "WARN": "[!!]  ", "FAIL": "[XX]  "}[estado]
    print(f"{icono}{mensaje}")
    if ayuda:
        print(f"       -> {ayuda}")
    {"OK": ok, "WARN": advertencias, "FAIL": fallos}[estado].append(mensaje)


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


# --- 1. Sistema y Python -------------------------------------------------------------------
seccion("1. Sistema y Python")
print(f"       Sistema: {platform.system()} {platform.release()} ({platform.machine()})")
print(f"       Ejecutable: {sys.executable}")

version_py = sys.version_info[:3]
texto_py = ".".join(map(str, version_py))
if PYTHON_MINIMO <= version_py[:2] < PYTHON_MAXIMO_EXCLUSIVO:
    reporta("OK", f"Python {texto_py}")
elif version_py[:2] >= PYTHON_MAXIMO_EXCLUSIVO:
    reporta(
        "WARN",
        f"Python {texto_py}: el curso se verificó con 3.11",
        "Si usaste environment.yml deberías tener 3.11. Comprueba que activaste `ml-curso`.",
    )
else:
    reporta(
        "FAIL",
        f"Python {texto_py} es demasiado antiguo (se requiere 3.11)",
        "Crea el entorno con `conda env create -f environment.yml` y actívalo.",
    )

entorno = os.environ.get("CONDA_DEFAULT_ENV")
if entorno == NOMBRE_ENTORNO:
    reporta("OK", f"Entorno conda activo: {entorno}")
elif entorno:
    reporta(
        "WARN",
        f"Entorno conda activo: {entorno} (se esperaba {NOMBRE_ENTORNO})",
        f"Ejecuta `conda activate {NOMBRE_ENTORNO}` y vuelve a correr este script.",
    )
elif sys.prefix != sys.base_prefix:
    reporta("OK", f"Entorno virtual (venv) activo: {sys.prefix}")
else:
    reporta(
        "WARN",
        "No hay ningún entorno virtual activo",
        f"Ejecuta `conda activate {NOMBRE_ENTORNO}` (o activa tu venv) y vuelve a correr.",
    )

ruta = os.getcwd()
if any(ch in ruta for ch in " áéíóúñÁÉÍÓÚÑ"):
    reporta(
        "WARN",
        f"La ruta actual tiene espacios o tildes: {ruta}",
        "Algunas librerías fallan con ellas. Considera mover el repositorio a una ruta simple.",
    )
else:
    reporta("OK", f"Ruta sin espacios ni tildes: {ruta}")

if os.path.exists("environment.yml"):
    reporta("OK", "Ejecutado desde la raíz del repositorio (environment.yml encontrado)")
else:
    reporta(
        "WARN",
        "No se encontró environment.yml en la carpeta actual",
        "Ejecuta el script desde la raíz del repositorio (`cd machine_learning`).",
    )

# --- 2. Paquetes ----------------------------------------------------------------------------
seccion("2. Paquetes del curso")
for modulo, paquete, minimo, uso in PAQUETES:
    try:
        instalada = metadata.version(paquete)
    except metadata.PackageNotFoundError:
        if paquete in SOLO_PIP:
            ayuda = f"Con el entorno activo: `pip install {paquete}`."
        else:
            ayuda = (f"Con el entorno activo: `conda install -c conda-forge "
                     f"{NOMBRE_CONDA.get(paquete, paquete)}`.")
        reporta("FAIL", f"{paquete:<18} no está instalado  ({uso})", ayuda)
        continue

    if _version_tupla(instalada) < _version_tupla(minimo):
        reporta(
            "WARN",
            f"{paquete:<18} {instalada:<10} (se recomienda >= {minimo}; {uso})",
            "Actualiza con `conda env update -f environment.yml --prune`.",
        )
        continue

    # Importar de verdad: detecta paquetes instalados pero rotos (p. ej. lightgbm sin OpenMP).
    try:
        __import__(modulo)
    except Exception as exc:  # noqa: BLE001 - queremos capturar cualquier error de import
        ayuda = f"`import {modulo}` falló: {type(exc).__name__}: {exc}"
        if paquete == "lightgbm" and platform.system() == "Darwin":
            ayuda += " | En macOS: `conda install -c conda-forge llvm-openmp`."
        reporta("FAIL", f"{paquete:<18} {instalada:<10} instalado pero no importa", ayuda)
        continue

    reporta("OK", f"{paquete:<18} {instalada:<10} ({uso})")

# --- 3. Kernel de Jupyter -------------------------------------------------------------------
seccion("3. Kernel de Jupyter")
try:
    from jupyter_client.kernelspec import KernelSpecManager

    kernels = KernelSpecManager().find_kernel_specs()
    if NOMBRE_ENTORNO in kernels:
        reporta("OK", f"Kernel `{NOMBRE_ENTORNO}` registrado en {kernels[NOMBRE_ENTORNO]}")
    else:
        reporta(
            "WARN",
            f"El kernel `{NOMBRE_ENTORNO}` no está registrado (hay: {', '.join(sorted(kernels)) or 'ninguno'})",
            f'Ejecuta: python -m ipykernel install --user --name {NOMBRE_ENTORNO} '
            f'--display-name "Python ({NOMBRE_ENTORNO})"',
        )
except Exception as exc:  # noqa: BLE001
    reporta("WARN", f"No se pudo consultar los kernels ({type(exc).__name__})",
            "Instala ipykernel y jupyterlab con `conda env update -f environment.yml`.")

# --- 4. Git ---------------------------------------------------------------------------------
seccion("4. Git")
if shutil.which("git") is None:
    reporta("FAIL", "Git no está instalado o no está en el PATH",
            "Instálalo desde https://git-scm.com y reinicia la terminal.")
else:
    salida = subprocess.run(["git", "--version"], capture_output=True, text=True)
    reporta("OK", salida.stdout.strip())
    for clave in ("user.name", "user.email"):
        valor = subprocess.run(["git", "config", "--global", clave],
                               capture_output=True, text=True).stdout.strip()
        if valor:
            reporta("OK", f"git config {clave} = {valor}")
        else:
            reporta("WARN", f"git config {clave} no está configurado",
                    f'Ejecuta: git config --global {clave} "<valor>"')

# --- 5. Prueba funcional mínima -------------------------------------------------------------
seccion("5. Prueba funcional: entrenar un modelo pequeño")
try:
    import numpy as np
    from sklearn.linear_model import LinearRegression

    rng = np.random.default_rng(42)
    X = rng.normal(size=(100, 2))
    y = 3 * X[:, 0] - 2 * X[:, 1] + rng.normal(scale=0.1, size=100)
    coef = LinearRegression().fit(X, y).coef_
    if np.allclose(coef, [3, -2], atol=0.1):
        reporta("OK", f"Regresión lineal recupera los coeficientes: {np.round(coef, 2)}")
    else:
        reporta("WARN", f"Coeficientes inesperados: {coef}")
except Exception as exc:  # noqa: BLE001
    reporta("FAIL", f"No se pudo entrenar un modelo: {type(exc).__name__}: {exc}")

# --- Resumen --------------------------------------------------------------------------------
print()
print("=" * 60)
print(f" RESUMEN: {len(ok)} OK · {len(advertencias)} advertencias · {len(fallos)} fallos")
if fallos:
    print(" Hay fallos. Revisa las líneas [XX] y la sección 14 del tutorial.")
elif advertencias:
    print(" Entorno utilizable, pero revisa las líneas [!!].")
else:
    print(" Entorno listo para el curso.")
print("=" * 60)

sys.exit(1 if fallos else 0)

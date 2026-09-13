"""Convierte un .py en formato 'percent' a .ipynb (nbformat 4), sin dependencias.

Formato de entrada:
    # %% [markdown]
    # Texto markdown con un '# ' de prefijo en cada linea
    # %%
    codigo_python()

Al convertir inserta la celda de arranque para Google Colab (ver celda_colab.py),
deduciendo la carpeta del notebook de la ruta de salida. En --solo-codigo esa celda se
omite: sus '!' y '%' solo son validos en IPython.

Uso:
    python percent2ipynb.py entrada.py salida.ipynb
    python percent2ipynb.py entrada.py --solo-codigo   # imprime el codigo para ejecutarlo
"""
import json
import sys

import celda_colab


def parsear(texto):
    celdas = []
    tipo = None
    buffer = []

    def cerrar():
        if tipo is None:
            return
        cuerpo = "\n".join(buffer).strip("\n")
        if not cuerpo.strip():
            return
        if tipo == "markdown":
            lineas = []
            for ln in cuerpo.split("\n"):
                if ln.startswith("# "):
                    lineas.append(ln[2:])
                elif ln.strip() == "#":
                    lineas.append("")
                else:
                    lineas.append(ln)
            cuerpo = "\n".join(lineas)
        celdas.append((tipo, cuerpo))

    for linea in texto.split("\n"):
        if linea.startswith("# %%"):
            cerrar()
            tipo = "markdown" if "[markdown]" in linea else "code"
            buffer = []
        else:
            buffer.append(linea)
    cerrar()
    return celdas


def a_fuente(cuerpo):
    """Lista de lineas con '\\n' al final, salvo la ultima (convencion nbformat)."""
    lineas = cuerpo.split("\n")
    return [ln + "\n" for ln in lineas[:-1]] + [lineas[-1]]


def construir(celdas, carpeta):
    """Notebook nbformat 4 con la celda de arranque para Colab para `carpeta`
    (p. ej. 'modulo-3-regresion-evaluacion/notebooks')."""
    salida = []
    for tipo, cuerpo in celdas:
        celda = {"cell_type": tipo, "metadata": {}, "source": a_fuente(cuerpo)}
        if tipo == "code":
            celda["execution_count"] = None
            celda["outputs"] = []
        salida.append(celda)
    nb = {
        "cells": salida,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (ml-curso)",
                "language": "python",
                "name": "ml-curso",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return celda_colab.insertar(nb, carpeta)


if __name__ == "__main__":
    entrada = sys.argv[1]
    with open(entrada, encoding="utf-8") as fh:
        celdas = parsear(fh.read())

    if "--solo-codigo" in sys.argv:
        # Sin la celda de arranque para Colab: sus '!' y '%' no son Python.
        print("\n\n".join(c for t, c in celdas if t == "code" and not celda_colab.es_celda_arranque(c)))
    else:
        salida = sys.argv[2]
        nb = construir(celdas, celda_colab.carpeta_de(salida))
        with open(salida, "w", encoding="utf-8") as fh:
            json.dump(nb, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        md = sum(1 for c in nb["cells"] if c["cell_type"] == "markdown")
        code = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
        print(f"{salida}: {len(nb['cells'])} celdas ({md} markdown / {code} codigo, con la de arranque para Colab)")

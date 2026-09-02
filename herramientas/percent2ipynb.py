"""Convierte un .py en formato 'percent' a .ipynb (nbformat 4), sin dependencias.

Formato de entrada:
    # %% [markdown]
    # Texto markdown con un '# ' de prefijo en cada linea
    # %%
    codigo_python()

Uso:
    python percent2ipynb.py entrada.py salida.ipynb
    python percent2ipynb.py entrada.py --solo-codigo   # imprime el codigo para ejecutarlo
"""
import json
import sys


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


def construir(celdas):
    salida = []
    for tipo, cuerpo in celdas:
        celda = {"cell_type": tipo, "metadata": {}, "source": a_fuente(cuerpo)}
        if tipo == "code":
            celda["execution_count"] = None
            celda["outputs"] = []
        salida.append(celda)
    return {
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


if __name__ == "__main__":
    entrada = sys.argv[1]
    with open(entrada, encoding="utf-8") as fh:
        celdas = parsear(fh.read())

    if "--solo-codigo" in sys.argv:
        print("\n\n".join(c for t, c in celdas if t == "code"))
    else:
        salida = sys.argv[2]
        with open(salida, "w", encoding="utf-8") as fh:
            json.dump(construir(celdas), fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        md = sum(1 for t, _ in celdas if t == "markdown")
        code = sum(1 for t, _ in celdas if t == "code")
        print(f"{salida}: {len(celdas)} celdas ({md} markdown / {code} codigo)")

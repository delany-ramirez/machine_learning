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

El kernel que declara es `ml-curso`, el del entorno de `environment.yml`.

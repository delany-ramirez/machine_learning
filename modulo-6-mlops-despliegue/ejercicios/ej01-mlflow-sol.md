# Solución · Ejercicio 01 · Trazabilidad de los modelos de Adult Census

> **Material del docente.** Números con `random_state=42` en partición y CV. Las AP se
> reproducen a la tercera cifra; los tamaños, a la centésima de MB; las latencias y
> tiempos dependen de la máquina (aquí, CPU de escritorio, 4 hilos).

## Parte A — Cuatro corridas

**A.1**

| Corrida | AP (CV) | AUC (CV) | Tamaño | Latencia por fila | Ajuste (5 pliegues) |
|---|---|---|---|---|---|
| logistica | 0.766 ± 0.002 | 0.906 | 0.00 MB | 0.005 ms | 0.7 s |
| random_forest_300_hoja5 | 0.797 ± 0.002 | 0.918 | **11.6 MB** | 0.041 ms | 5.6 s |
| hist_gradient_boosting | 0.827 ± 0.002 | 0.928 | 0.15 MB | 0.006 ms | 2.9 s |
| lightgbm_nativo | **0.828 ± 0.002** | 0.928 | 0.15 MB | **0.002 ms** | 0.4 s |

Hash del CSV: `c6a2e9f9…` (los 12 primeros caracteres del SHA-256 de `adult-census.csv`
tal como lo produce el script de descarga).

**A.2** En `modelo/`: `MLmodel` (el manifiesto: *flavors*, firma, ejemplo, versión de
MLflow), `model.skops` (scikit-learn) o `model.lgb` (LightGBM; el archivo del modelo en
sí), `requirements.txt` y `python_env.yaml`/`conda.yaml` (las dependencias exactas para
cargarlo), `input_example.json` y `serving_input_example.json` (un ejemplo con el que
probar el modelo cargado y la forma de la petición a `mlflow models serve`). Error
típico: no registrar la firma, con lo que el modelo cargado acepta cualquier columna en
cualquier orden sin avisar.

## Parte B — Comparar y elegir

**B.1** La gráfica AP-tamaño tiene tres puntos en la esquina "bien y ligero"
(logística, HGB, LightGBM, todos < 0.2 MB) y uno lejos (Random Forest, 11.6 MB, y **peor**
AP que los dos boosting). La de AP-latencia, lo mismo: LightGBM es a la vez el mejor y el
más rápido.

**B.2** Aquí **coinciden**: LightGBM es el mejor en AP y el más ligero y rápido. 500
peticiones por segundo a 0.002 ms por fila es una carga trivial para el modelo (el cuello
de botella será HTTP, como en `api/README.md`); 0.15 MB cabe en cualquier contenedor. El
Random Forest, que en el módulo 4 era el "modelo fuerte" por defecto, queda descartado por
los tres criterios a la vez.

**B.3** Versión 1 = LightGBM, alias `campeon` **y** `produccion` (tag: "mejor AP, menor
tamaño y menor latencia"); versión 2 = HGB como respaldo sin dependencia de LightGBM
(tag: "equivalente en AP, solo scikit-learn"). En Wine Quality no coincidían porque el
mejor en AP era un bosque de 12 MB y 20× más lento; en Adult, el boosting gana en todo.
La lección no es "boosting siempre" sino que la decisión de producción **se toma con las
tres métricas**, y a veces no hay conflicto.

## Parte C — Reproducir y romper

**C.1** AP registrada 0.827924; reproducida con los mismos hiperparámetros, semilla y
datos: 0.827924. Idénticas.

**C.2** Al cambiar la edad del primer registro (+1 año): el hash pasa de `c6a2e9f9…` a otro
valor, y **la AP no cambia en absoluto** (0.827924): un año en una fila de 39 000 cae en el
mismo *bin* del histograma de LightGBM. Sin el hash, el cambio en los datos habría pasado
completamente desapercibido — y en un caso real el cambio no es un año en una fila sino
una recarga del CSV con filas de menos, una columna recodificada o una fuga. **La métrica
no es un detector de cambios en los datos; el hash sí.** Es la razón de registrarlo aunque
parezca burocracia.

**C.3** LightGBM desde `models:/adult-ingreso-alto@produccion` sobre el conjunto de prueba:
AP 0.835, AUC 0.931. Algo por encima de la CV (0.828): dentro de lo esperable (la CV
entrena con el 80 % del entrenamiento; el modelo final con el 100 %), y la diferencia es
del orden de tres errores estándar de la CV, no una señal de nada.

## Tabla final (lo que se espera)

| Corrida | AP ± ee | Tamaño | Latencia | Alias | Razón |
|---|---|---|---|---|---|
| lightgbm_nativo | 0.828 ± 0.002 | 0.15 MB | 0.002 ms | campeon, produccion | mejor en las cuatro métricas |
| hist_gradient_boosting | 0.827 ± 0.002 | 0.15 MB | 0.006 ms | — (versión 2) | respaldo sin LightGBM |
| random_forest_300_hoja5 | 0.797 ± 0.002 | 11.6 MB | 0.041 ms | — | peor AP, 80× el tamaño |
| logistica | 0.766 ± 0.002 | 0.00 MB | 0.005 ms | — | línea base |

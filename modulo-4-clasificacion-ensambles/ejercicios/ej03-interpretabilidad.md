# Ejercicio 03 · Interpretar el modelo de Adult Census: importancias, SHAP y sesgos

**Módulo 4 · Sesión 11** · Tiempo estimado: **75 min** · Con código

> **Objetivo.** Explicar el LightGBM del ejercicio 02 con las tres herramientas de
> `06-interpretabilidad.md`, ver cómo discrepan sobre datos reales —con una variable de alta
> cardinalidad y otra redundante que lo provocan sin que nadie plante ruido—, y cerrar con la
> pregunta que un modelo sobre ingresos y datos personales obliga a hacer: ¿qué hace el
> modelo con `sexo`, y qué pasa si se quita?

## Contexto

Misma partición del ejercicio 01, categóricas nativas (`dtype="category"`) como en C.1 del
ejercicio 02, y el modelo `LGBMClassifier(n_estimators=335, learning_rate=0.03)` de C.2.
Para la permutación y SHAP se necesita un conjunto no visto que no sea el de prueba: usa el
primer pliegue de la CV como validación (ajusta sobre los otros cuatro), igual que
`07-interpretabilidad-aplicado.ipynb`.

```python
import shap
from sklearn.inspection import permutation_importance
```

Entrega un notebook `ej03-<tu-apellido>.ipynb` que corra de principio a fin.

## Parte A — Tres importancias, dos ganancias (20 min)

**A.1** Para el modelo ajustado sobre cuatro pliegues, calcula y tabula, normalizadas para
que sumen 1 donde aplique:

- la importancia por **ganancia** (`booster_.feature_importance("gain")`),
- la importancia por **número de particiones** (`"split"`),
- la importancia por **permutación** sobre el pliegue de validación (AP, `n_repeats=5`),
- la media de $|\phi_j|$ de **SHAP** (`shap.TreeExplainer`) sobre el mismo pliegue.

**A.2** `fnlwgt` es el peso muestral del censo: un número con decenas de miles de valores
distintos y sin relación causal con el ingreso. ¿En qué posición queda en cada una de las
cuatro medidas? Explica la discrepancia con la sección 2 de `06-interpretabilidad.md`.

**A.3** `relacion` es la primera variable por ganancia y una de las últimas por
permutación. Comprueba la relación entre `relacion` y `sexo` (¿qué fracción de `Husband` es
`Male`, y de `Wife` es `Female`?) y entre `relacion` y `estado_civil`, y explica la
discrepancia.

**A.4** `ganancia_capital` es, por permutación, la variable más importante con mucha
diferencia, y solo la cuarta por SHAP. ¿Qué fracción de las personas tiene
`ganancia_capital > 0`? Usa la contribución SHAP media de esa variable para quienes la tienen
en cero, mayor que cero y mayor o igual a 5 000, y explica por qué las dos medidas pueden
decir cosas distintas sin que ninguna esté mal.

## Parte B — Lectura global y local con SHAP (20 min)

**B.1** Dibuja el gráfico de enjambre (*beeswarm*). Describe, para las cuatro variables
principales, en qué dirección empujan los valores altos.

**B.2** Dibuja la dependencia SHAP de `edad`, coloreada por `horas_semana`
(`shap.plots.scatter(explicacion[:, "edad"], color=explicacion[:, "horas_semana"])`; la
selección automática de la variable de color falla con columnas categóricas). Resume la
contribución media de `edad` por tramos de edad. ¿El efecto es monótono?

**B.3** Localiza, en el pliegue de validación, al positivo con menor probabilidad predicha
(el falso negativo más claro). Muestra su cascada (*waterfall*) y explica, con sus cuatro
contribuciones más negativas, por qué el modelo no tenía forma de acertar.

## Parte C — `sexo`: qué hace el modelo y qué pasa si se quita (35 min)

**C.1** Reporta la contribución SHAP media de `sexo` para hombres y para mujeres. Con el
umbral de mínimo costo del ejercicio 02 (0.15), calcula sobre el pliegue de validación, por
sexo: prevalencia real, fracción de personas predichas como positivas, recall y precisión.

**C.2** Reentrena el mismo modelo **sin** la columna `sexo` y repite C.1. ¿Cuánto cambia la
AP? ¿Cuánto cambian las tasas de positivos predichos y el recall por sexo?

**C.3** A partir de A.3 y C.2, explica por qué quitar la variable sensible no quitó la
información sensible. ¿Qué haría falta para que el modelo *no pudiera* usar el sexo?
(No se pide implementarlo: se pide identificar el problema con precisión.)

**C.4** Dos párrafos: qué le dirías a quien quiera usar este modelo para decidir a quién
ofrecer un producto financiero, y qué **no** se puede concluir de estos gráficos sobre las
causas de la brecha de ingresos (sección 5 de `06-interpretabilidad.md`).

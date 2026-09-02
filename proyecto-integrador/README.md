# Proyecto integrador

> Estado: **contenido pendiente** (Fase 7 de [`../PLAN.md`](../PLAN.md)).

Un caso único que acompaña todo el curso: cada módulo aporta una entrega parcial, y en la
sesión 14 se sustenta el resultado completo, desplegado como API y trazable en MLflow.

## Archivos planeados

| Archivo | Contenido | Estado |
|---|---|---|
| `enunciado.md` | Contexto del caso, objetivo, datos y entregables | ⬜ |
| `entregas.md` | Detalle de las 6 entregas parciales y su cronograma | ⬜ |
| `rubrica.md` | Criterios de evaluación por entrega | ⬜ |
| `datos/generar-datos.py` | Generador del dataset con semilla fija | ⬜ |
| `datos/*.csv` | Dataset del proyecto | ⬜ |

## Entregas por módulo

| Entrega | Módulo | Sesiones | Contenido |
|---|---|---|---|
| **E1** | 1 | S1–S3 | Definición del problema, variable objetivo, métricas de éxito; repositorio con Git y DVC |
| **E2** | 2 | S4–S5 | EDA, decisiones de limpieza y `Pipeline` de preprocesamiento |
| **E3** | 3 | S6–S8 | Modelo de línea base con validación cruzada honesta |
| **E4** | 4 | S9–S11 | Ensambles ajustados, comparados con la línea base, con interpretabilidad |
| **E5** | 5 | S12–S13 | Exploración no supervisada del caso, o variante con MLP |
| **E6** | 6 | S14 | Modelo en MLflow, API FastAPI, informe final y sustentación |

## Decisión pendiente

El **tema del caso** aún no está fijado. La propuesta es *predicción de deserción
estudiantil*, con un dataset sintético pero realista generado con semilla fija, que incluya a
propósito valores faltantes, variables categóricas, desbalance de clases y una **fuga de datos
plantada** para que los estudiantes la detecten en el módulo 2.

Alternativa: reutilizar el enunciado del trabajo final de la edición anterior del curso. Si se
opta por esa vía, basta con copiarlo a esta carpeta para adaptarlo.

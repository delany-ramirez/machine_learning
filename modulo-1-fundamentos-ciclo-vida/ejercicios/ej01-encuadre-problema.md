# Ejercicio 01 · Encuadrar problemas de Machine Learning

**Módulo 1 · Sesiones 1–2** · Tiempo estimado: **45 min** · Sin código

> **Objetivo.** Practicar la etapa que decide el destino de un proyecto: traducir una
> necesidad real en un problema de ML bien planteado, con variable objetivo, tipo de tarea,
> métricas y referencia; y detectar fugas de datos antes de que ocurran.

## Parte A — Clasificar el tipo de aprendizaje (10 min)

Para cada situación, indica el **tipo de aprendizaje** (supervisado, no supervisado o por
refuerzo) y, si es supervisado, si es **regresión** o **clasificación**. Justifica en una
línea.

1. Estimar cuántos estudiantes se matricularán el próximo semestre.
2. Agrupar a los estudiantes de la maestría en perfiles similares, sin saber de antemano
   cuántos perfiles hay ni cuáles.
3. Decidir si un correo entrante es fraudulento.
4. Predecir la nota que sacará un estudiante en el examen final.
5. Identificar transacciones inusuales en el sistema financiero de la universidad, sin
   ejemplos previos de fraude etiquetados.
6. Un sistema que ajusta automáticamente la dificultad de los ejercicios según cómo responde
   cada estudiante, buscando maximizar el aprendizaje a largo plazo.
7. Clasificar los artículos científicos de un repositorio en las tres líneas de investigación
   del programa.

## Parte B — Encuadrar un problema completo (20 min)

> **Situación.** La Vicerrectoría Académica quiere reducir la deserción en los programas de
> posgrado. Actualmente, un coordinador revisa manualmente los casos y cita a los estudiantes
> que "le parecen en riesgo". El año pasado desertó el 18 % de los estudiantes. Hay
> presupuesto para atender con tutoría personalizada a unos 60 estudiantes por semestre, de
> un total de 400 matriculados.

Completa la ficha de definición del problema:

| Elemento | Tu respuesta |
|---|---|
| Decisión que apoya el modelo | |
| Variable objetivo (precisa y observable) | |
| Tipo de tarea | |
| Momento en que se predice | |
| Referencia contra la cual comparar | |
| Métrica técnica y por qué esa | |
| Métrica de negocio | |
| Restricción operativa principal | |

Añade además:

- **B.1** ¿Los costos de los dos tipos de error son simétricos? Explica cuál es peor y por qué.
- **B.2** ¿Qué consecuencia tiene sobre el modelo el hecho de que solo haya 60 cupos?

## Parte C — Detectar fugas de datos (10 min)

Para el problema de la Parte B, el equipo propone estas variables predictoras. Marca cuáles
producen **fuga de datos** y explica por qué.

| # | Variable candidata | ¿Fuga? | Por qué |
|---|---|---|---|
| 1 | Promedio acumulado al momento de ingresar al programa | | |
| 2 | Número de créditos matriculados el semestre siguiente | | |
| 3 | Asistencia a clases durante las primeras cuatro semanas | | |
| 4 | Si solicitó retiro formal ante la secretaría académica | | |
| 5 | Estrato socioeconómico declarado en la matrícula | | |
| 6 | Promedio del semestre en curso, calculado al cierre del semestre | | |
| 7 | Número de veces que ingresó a la plataforma virtual en el primer mes | | |
| 8 | Si el coordinador ya lo citó a tutoría | | |

## Parte D — Argumentar en contra (5 min)

**D.1** Da dos razones concretas por las que este proyecto podría **no** deber hacerse con
Machine Learning.

**D.2** El modelo se entrena con datos históricos de deserción de los últimos cinco años.
Menciona un riesgo ético o de sesgo concreto que esto introduce, y una forma de detectarlo.

---

> **Entrega.** Un documento de máximo dos páginas con las cuatro partes. Se evalúa la
> justificación, no la coincidencia literal con la solución.

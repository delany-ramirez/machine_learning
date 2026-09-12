# 05 · Entrenar una red, y cuándo no hace falta

**Módulo 5 · Sesión 13** — Deep learning (puente)

## Objetivos

- Conocer las piezas de un entrenamiento en PyTorch y las decisiones que hay que tomar:
  mini-lotes, optimizador, tasa de aprendizaje, épocas, *early stopping*.
- Entender las tres formas de regularizar una red —*early stopping*, *weight decay*,
  *dropout*— y qué mide cada una.
- Tener un criterio **medido** para decidir cuándo un problema tabular no necesita deep
  learning, y saber en qué tipos de datos las redes sí ganan y por qué.

## 1. El bucle de entrenamiento

Entrenar una red es el descenso del gradiente por mini-lotes de la S6, con la
retropropagación calculando el gradiente. En PyTorch, las piezas
(`06-mlp-pytorch-aplicado.ipynb`, sección 2):

| Pieza | En PyTorch | Decisión |
|---|---|---|
| Datos | tensores `float32`, estandarizados | Estandarizar es obligatorio, como en cualquier modelo con gradiente |
| Modelo | `nn.Sequential(nn.Linear, nn.ReLU, nn.Dropout, …)` | Anchura y profundidad; para tabular, 1–3 capas de 32–256 |
| Pérdida | `BCEWithLogitsLoss` (binaria), `CrossEntropyLoss` (multiclase), `MSELoss` | La última capa devuelve *logits*; la sigmoide/softmax va en la pérdida por estabilidad numérica |
| Optimizador | `torch.optim.Adam`, `SGD` | Adam con $\eta = 10^{-3}$ es el punto de partida |
| Bucle | por época: barajar; por lote: `zero_grad()` → adelante → pérdida → `backward()` → `step()` | Tamaño del lote (32–256), número de épocas |
| Validación | al final de cada época, en modo `eval()` | Guardar el mejor estado; parar con paciencia |

### Mini-lotes y épocas

Una **época** es una pasada por todos los datos; un **lote** (*batch*) es el subconjunto
con el que se calcula cada gradiente. Lotes pequeños dan gradientes ruidosos pero muchos
pasos por época (S6: mini-batch llega en una época a donde batch tarda veinte); lotes
grandes aprovechan mejor el hardware. 32–256 es el rango habitual; el ruido del lote
pequeño actúa además como regularizador suave.

### Optimizadores

- **SGD**: $\theta \leftarrow \theta - \eta\nabla\mathcal{L}$.
- **Momento**: $v \leftarrow \beta v + \nabla\mathcal{L}$, $\theta \leftarrow \theta - \eta v$,
  con $\beta \approx 0.9$: una media móvil del gradiente que acelera en direcciones
  consistentes y amortigua las oscilaciones en las que cambia de signo.
- **Adam** (Kingma y Ba, 2015): momento y, además, una tasa **por parámetro** normalizada
  por la media móvil del gradiente al cuadrado. Cada peso avanza a un ritmo adaptado a la
  escala de su gradiente, lo que lo hace robusto a la elección de $\eta$.

Sobre Wine Quality con la misma tasa, SGD se estanca en pérdida 0.35, el momento llega en
5 épocas a donde SGD tarda 100, y Adam va por delante todo el camino
(`06-mlp-pytorch-aplicado.ipynb`, sección 3). Pero la mejor AP de validación es la misma
para los tres: el optimizador cambia la **velocidad**, no el destino. Adam es el valor por
defecto porque ahorra buscar la tasa; SGD con momento y una tasa bien afinada sigue
siendo competitivo (y a veces generaliza mejor) en visión.

### La tasa de aprendizaje

Es el hiperparámetro que más importa. Demasiado alta: la pérdida oscila o diverge
(módulo 3, notebook 01, sin estandarizar). Demasiado baja: no llega. Se explora en
escala logarítmica ($10^{-4}$ a $10^{-2}$ para Adam) y suele combinarse con un
**programa** (*schedule*) que la reduce a lo largo del entrenamiento.

## 2. Regularizar una red

Una red tiene, casi siempre, más parámetros que datos, y el poder de ajustar cualquier
cosa incluye el ruido (`04-redes-neuronales.md`, §5). Tres controles, que se combinan:

- ***Early stopping***: evaluar en validación al final de cada época, guardar el mejor
  estado y parar cuando lleve `paciencia` épocas sin mejorar. Es regularización porque
  limita cuánto se alejan los pesos de la inicialización. Sobre Wine Quality, la pérdida
  de validación toca fondo en las primeras decenas de épocas mientras la de entrenamiento
  sigue bajando durante 300. Es el mismo mecanismo del early stopping de LightGBM (S11).
- ***Weight decay***: la penalización $\ell_2$ de la S7 sobre todos los pesos,
  $\mathcal{L} + \lambda\sum\theta^2$, aplicada por el optimizador en cada paso
  (`weight_decay` en PyTorch). Valores típicos, $10^{-5}$ a $10^{-3}$.
- ***Dropout*** (Srivastava et al., 2014): en cada paso de entrenamiento, poner a cero
  al azar una fracción $p$ (0.1–0.5) de las activaciones de cada capa. Ninguna neurona
  puede depender de que otra concreta esté presente; el efecto es parecido a promediar
  muchas sub-redes, como un ensamble. En evaluación (`model.eval()`) se usan todas las
  neuronas con las activaciones escaladas.

Medido sobre Wine Quality en CV de 5 pliegues (`06-mlp-pytorch-aplicado.ipynb`, sección
3): con early stopping en todos los casos, añadir weight decay, dropout, ambos, o cambiar
el tamaño de la red (32 a 256-128) mueve la AP entre 0.55 y 0.57, con error estándar
0.013 — nada detectable. El early stopping hace casi todo el trabajo en un dataset
pequeño. Lo que sí cambia es el tiempo (5–10 s por configuración en CV, frente a una
fracción de segundo para la logística).

### Una fuga que conviene conocer

Si el early stopping elige la época mirando el **mismo** pliegue sobre el que se reporta
la métrica, esa métrica es optimista: se eligió la época con la mejor AP *de ese pliegue*.
En Wine Quality el sesgo es de casi dos centésimas (AP 0.565 frente a 0.548 cuando la
validación del early stopping sale de un 15 % apartado del entrenamiento). Es la fuga de
selección del módulo 3 (S8, CV anidada), otra vez. La regla: el conjunto de validación
que decide cuándo parar es parte del entrenamiento, no de la evaluación.

## 3. Cuándo no usar deep learning: la comparación

La pregunta central de la sesión, respondida con la comparación pareada del módulo 3
sobre los mismos pliegues que los notebooks del módulo 4 (`06-mlp-pytorch-aplicado.ipynb`,
secciones 4 y 5):

| Dataset | Modelo | AP (CV) | Tiempo por pliegue |
|---|---|---|---|
| Wine Quality (4256 filas, 12 variables) | Regresión logística | 0.525 ± 0.006 | 0.01 s |
| | LightGBM por defecto | 0.555 ± 0.009 | 0.04 s |
| | **Extra-Trees** | **0.594 ± 0.009** | 0.2 s |
| | MLP 64-32, dropout, weight decay, early stopping | 0.548 ± 0.007 | 1.4 s |
| Adult Census (39 073 filas, 14 variables, 8 categóricas) | Regresión logística | 0.766 ± 0.002 | 0.2 s |
| | **LightGBM** (categóricas nativas) | **0.828 ± 0.002** | 0.2 s |
| | MLP 128-64 | 0.781 ± 0.002 | 2.1 s |

Comparaciones pareadas: en Wine, MLP − Extra-Trees $= -0.046 \pm 0.004$ (cociente 10);
MLP − logística $= +0.023 \pm 0.005$; MLP − LightGBM, indistinguible de cero. En Adult,
MLP − LightGBM $= -0.047 \pm 0.001$. Con diez veces más datos la red mejora, pero el
boosting también, y la distancia se mantiene.

No es una peculiaridad de estos dos datasets. Los *benchmarks* sistemáticos sobre datos
tabulares (Grinsztajn, Oyallon y Varoquaux, 2022; Shwartz-Ziv y Armon, 2022) encuentran
que los árboles con boosting ganan a las redes en la mayoría de los conjuntos de tamaño
pequeño y mediano ($n < 10^5$), y que las redes solo se acercan con arquitecturas
específicas para tabular y mucho ajuste. Las razones que dan:

- Los árboles son **invariantes a transformaciones monótonas** de cada variable y manejan
  escalas heterogéneas, umbrales, categóricas y valores faltantes de fábrica; la red
  tiene que aprender todo eso desde pesos aleatorios.
- Las funciones que aprenden las redes son **suaves** por construcción, y las relaciones
  en datos tabulares suelen ser irregulares (escalones, interacciones abruptas).
- Los datos tabulares tienen **variables no informativas**, y las redes son más sensibles
  a ellas que los árboles.

La regla práctica para el proyecto integrador: en datos tabulares, la línea base es
la regresión logística y el modelo fuerte es un ensamble de árboles (S10–S11). Un MLP se
prueba si sobra tiempo, con la comparación pareada, y se adopta solo si gana de forma
detectable **y** relevante — lo que en estos dos datasets no ocurrió.

## 4. Dónde las redes sí ganan, y por qué

Las redes dominan en imágenes, audio, texto y series largas. La razón no es que "tengan
más parámetros" sino que su **arquitectura codifica la estructura del dato** — el sesgo
inductivo adecuado:

- **Convoluciones** (imágenes): el mismo filtro pequeño se aplica en todas las posiciones.
  Comparte pesos, respeta la localidad y detecta el mismo patrón esté donde esté. Sobre
  los dígitos de 8 × 8 (`06-mlp-pytorch-aplicado.ipynb`, sección 6), una CNN mínima es la
  mejor (97.9 % frente a 97.0 % de la logística y 96.4 % del MLP) y, sobre todo, la que
  menos se desploma cuando los dígitos se corren un píxel (0.62 frente a 0.42–0.51): la
  logística y el MLP tienen cada peso atado a una posición fija. Con imágenes reales y
  aumento de datos, esa diferencia se vuelve enorme.
- **Recurrencia y atención** (secuencias, texto): compartir pesos a lo largo del tiempo
  y aprender qué partes de la entrada mirar.
- ***Transfer learning***: partir de una red entrenada sobre millones de imágenes (o de
  textos) y ajustar solo la última capa, o toda la red con una tasa pequeña, sobre unos
  cientos de ejemplos propios. Es la forma en que el deep learning se usa en la práctica
  fuera de las grandes empresas, y el tema del curso especializado.

Y el criterio, en una frase: **gana el modelo cuyo sesgo inductivo encaja con la
estructura de los datos**. Árboles para tablas, convoluciones para imágenes, atención
para texto. Cuando la estructura no está clara, se mide — con la comparación pareada,
sobre los mismos pliegues, con error estándar y con el tiempo al lado.

## Referencias

- Kingma, D. y Ba, J. (2015). Adam: a method for stochastic optimization. *ICLR*.
- Srivastava, N. et al. (2014). Dropout: a simple way to prevent neural networks from
  overfitting. *JMLR*.
- Grinsztajn, L., Oyallon, E. y Varoquaux, G. (2022). Why do tree-based models still
  outperform deep learning on typical tabular data? *NeurIPS Datasets and Benchmarks*.
- Shwartz-Ziv, R. y Armon, A. (2022). Tabular data: deep learning is not all you need.
  *Information Fusion*.
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*, caps. 7, 8 y 9.
- Documentación de PyTorch: <https://pytorch.org/tutorials/beginner/basics/intro.html>.

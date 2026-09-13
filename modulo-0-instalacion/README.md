# Módulo 0 — Instalación del software (antes de la S1)

> **Objetivo.** Que llegues a la primera sesión con todo instalado y probado, de modo que el
> tiempo de clase se dedique al contenido y no a arreglar computadores. Sigue este tutorial
> **completo y en orden**; al final ejecutas un script que te dice si todo quedó bien.
>
> **Tiempo estimado:** 30–60 minutos, según la velocidad de tu conexión (se descargan
> ~1.5 GB de paquetes). Hazlo con calma y con buena conexión, no la noche anterior.

Si ya tienes experiencia con Python, `uv` y Git, la versión corta está en
[`../docs/guia-entorno.md`](../docs/guia-entorno.md). Este documento es la versión larga,
pensada para quien parte de cero o quiere entender qué está instalando y por qué.

## Contenido

1. [Qué vas a instalar y por qué](#1-qué-vas-a-instalar-y-por-qué)
2. [Requisitos de tu computador](#2-requisitos-de-tu-computador)
3. [La terminal: tu herramienta de trabajo](#3-la-terminal-tu-herramienta-de-trabajo)
4. [Paso 1 — Git](#4-paso-1--git)
5. [Paso 2 — uv (Python)](#5-paso-2--uv-python)
6. [Paso 3 — Descargar el repositorio del curso](#6-paso-3--descargar-el-repositorio-del-curso)
7. [Paso 4 — Crear el entorno del curso](#7-paso-4--crear-el-entorno-del-curso)
8. [Paso 5 — Verificar la instalación](#8-paso-5--verificar-la-instalación)
9. [Paso 6 — Editor: VS Code o JupyterLab](#9-paso-6--editor-vs-code-o-jupyterlab)
10. [Plan B — Google Colab](#10-plan-b--google-colab)
11. [Herramientas que se instalan más adelante](#11-herramientas-que-se-instalan-más-adelante)
12. [Mantenimiento durante el curso](#12-mantenimiento-durante-el-curso)
13. [Preguntas frecuentes (FAQ)](#13-preguntas-frecuentes-faq)
14. [Problemas frecuentes y su solución](#14-problemas-frecuentes-y-su-solución)
15. [Glosario mínimo](#15-glosario-mínimo)
16. [Lista de verificación final](#16-lista-de-verificación-final)

---

## 1. Qué vas a instalar y por qué

| Herramienta | Para qué sirve en el curso | Cuándo se usa |
|---|---|---|
| **Git** | Descargar el repositorio del curso y recibir sus actualizaciones. Versionar el código de tu proyecto integrador | Desde la S1; a fondo en la S2 |
| **uv** | Descarga Python 3.11 y crea el *entorno virtual* del curso (`.venv`) con todas las librerías, a partir de `pyproject.toml` y `uv.lock` | Todo el curso |
| **Entorno `.venv`** | NumPy, pandas, scikit-learn, matplotlib, XGBoost, LightGBM, PyTorch, MLflow, etc. — todo con versiones compatibles entre sí | Todo el curso |
| **JupyterLab** (viene en el entorno) | Ejecutar los notebooks del curso | Todo el curso |
| **VS Code** (opcional pero recomendado) | Editor con soporte para notebooks, terminal integrada y Git | Todo el curso |
| **Cuenta en GitHub** | Alojar el repositorio de tu proyecto integrador | Desde la S2 |
| **Docker Desktop** | Empaquetar la API del proyecto | Solo en la S14; ver §11 |

### ¿Por qué un entorno virtual y no "instalar Python y ya"?

Las librerías de ML dependen unas de otras con versiones muy concretas. Si instalas todo en el
Python "global" de tu máquina, tarde o temprano dos proyectos piden versiones incompatibles y
se rompe alguno. Un **entorno virtual** es una carpeta aislada con su propio Python y sus
propias librerías. El archivo [`../pyproject.toml`](../pyproject.toml) declara qué librerías
necesita el curso y [`../uv.lock`](../uv.lock) fija la versión **exacta** de cada una (y de
las que estas arrastran), así que todos los estudiantes y el docente trabajamos con el mismo
entorno y "en mi máquina sí funciona" deja de ser un problema.

Esto es, además, el primer contenido del curso: un proyecto de ML **reproducible** empieza por
un entorno reproducible (S1 y S2).

### ¿Por qué uv?

[uv](https://docs.astral.sh/uv/) es un gestor de Python y de paquetes moderno, muy rápido y
que resuelve en un solo programa lo que antes requería varios (instalar Python, crear el
entorno, instalar librerías, fijar versiones). No necesita permisos de administrador, no toca
ningún Python que ya tengas instalado y el mismo comando (`uv sync`) sirve para crear el
entorno, actualizarlo o repararlo.

## 2. Requisitos de tu computador

| Recurso | Mínimo | Recomendado |
|---|---|---|
| Sistema operativo | Windows 10/11, macOS 12+, Ubuntu 20.04+ (o similar) | Cualquiera de ellos actualizado |
| RAM | 8 GB | 16 GB |
| Disco libre | 10 GB | 20 GB |
| Procesador | Cualquiera de 64 bits de los últimos ~8 años | — |
| GPU | **No se necesita** | — |
| Conexión | Necesaria para instalar y para descargar algunos datasets | — |

**No necesitas GPU.** El curso está diseñado para correr en un portátil corriente: los
datasets son pequeños y el único módulo con redes neuronales (S13) usa ejemplos que entrenan
en segundos en CPU.

Si tu máquina está por debajo del mínimo, o no puedes instalar software (equipo corporativo
bloqueado), ve directo al [Plan B con Google Colab](#10-plan-b--google-colab).

## 3. La terminal: tu herramienta de trabajo

Casi todo lo que sigue se hace escribiendo comandos en una **terminal**. No es más difícil que
copiar y pegar, pero hay que abrir la terminal correcta:

| Sistema | Terminal que debes usar | Cómo abrirla |
|---|---|---|
| **Windows** | **PowerShell** (o *Terminal de Windows*, que la abre por dentro). No uses el viejo *Símbolo del sistema* (CMD) | Menú Inicio → escribe `PowerShell` |
| **macOS** | **Terminal** | Cmd + Espacio → escribe `Terminal` |
| **Linux** | Terminal del sistema | Ctrl + Alt + T |

Convenciones de este documento:

- Cada bloque de código es **un comando**: cópialo, pégalo en la terminal y pulsa Enter.
  Espera a que termine (vuelve a aparecer el *prompt*) antes de ejecutar el siguiente.
- Cuando un comando cambia según el sistema operativo, se indica explícitamente.
- Lo que va entre `<...>` lo reemplazas tú (por ejemplo, `<tu-nombre>`).
- Si un comando falla, **lee el mensaje de error completo** antes de buscar en §14; casi
  siempre dice exactamente qué pasó.

Dos comandos que usarás todo el tiempo:

```bash
cd <ruta-de-una-carpeta>
```

cambia a esa carpeta ("*change directory*"), y

```bash
dir
```

(en Windows) o `ls` (macOS/Linux) lista lo que hay en la carpeta actual.

## 4. Paso 1 — Git

### Windows

1. Descarga el instalador desde <https://git-scm.com/download/win> (versión de 64 bits).
2. Ejecútalo. Puedes dejar **todas las opciones por defecto**; solo asegúrate de que
   "Git from the command line and also from 3rd-party software" esté seleccionado en la
   pantalla *Adjusting your PATH environment*.
3. Cierra y vuelve a abrir la terminal.

### macOS

Abre Terminal y ejecuta:

```bash
git --version
```

Si no está instalado, macOS ofrece instalar las *Command Line Tools*; acepta y espera. Como
alternativa, si usas [Homebrew](https://brew.sh): `brew install git`.

### Linux (Debian/Ubuntu)

```bash
sudo apt update && sudo apt install -y git
```

(En Fedora: `sudo dnf install git`.)

### Configuración inicial (todos los sistemas)

Git firma cada cambio con tu nombre y correo. Configúralos una sola vez:

```bash
git config --global user.name "<Nombre Apellido>"
```

```bash
git config --global user.email "<tu-correo@utp.edu.co>"
```

Y evita un problema clásico de saltos de línea entre Windows y el resto del mundo:

```bash
git config --global core.autocrlf true
```

(en macOS/Linux usa `input` en vez de `true`).

Comprueba:

```bash
git --version
```

Debe responder algo como `git version 2.4x.x`.

### Cuenta en GitHub

Crea una cuenta gratuita en <https://github.com> con tu correo institucional (te da acceso al
[GitHub Student Developer Pack](https://education.github.com/pack)). La necesitarás en la S2
para el repositorio de tu proyecto integrador; no hace falta nada más por ahora.

## 5. Paso 2 — uv (Python)

No instales Python por separado: **uv se encarga de descargar la versión exacta que usa el
curso (3.11)** cuando cree el entorno, sin tocar ningún otro Python que tengas en la máquina.

> Si ya tienes Anaconda o Miniconda instalados, no los desinstales ni los necesitas: uv es
> independiente. Solo evita instalar paquetes con `conda` o `pip` dentro del entorno del
> curso; siempre con `uv` (ver FAQ).

### Windows

En PowerShell, ejecuta el instalador oficial (no requiere permisos de administrador):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Al terminar dice algo como `everything's installed!` e indica que reinicies la terminal.
**Cierra PowerShell y ábrela de nuevo.**

Alternativa si ya usas el gestor de paquetes de Windows: `winget install --id=astral-sh.uv -e`.

### macOS y Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Cierra la terminal y ábrela de nuevo. En macOS, si usas Homebrew, `brew install uv` es
equivalente.

### Verificación (todos los sistemas)

```bash
uv --version
```

Debe responder `uv 0.x.x`. Si dice que no reconoce el comando, ve a §14 ("`uv` no se
reconoce").

## 6. Paso 3 — Descargar el repositorio del curso

Elige **dónde** va a vivir el curso en tu disco. Recomendación: una carpeta sin espacios ni
tildes y **fuera de OneDrive, Google Drive o iCloud** (los sincronizadores rompen los
entornos virtuales y ralentizan Git). Por ejemplo `C:\proyectos` en Windows o `~/proyectos`
en macOS/Linux.

Créala y entra en ella:

```bash
mkdir proyectos
```

```bash
cd proyectos
```

Clona el repositorio (descarga una copia con todo su historial):

```bash
git clone https://github.com/delany-ramirez/machine_learning.git
```

Entra en la carpeta que se acaba de crear:

```bash
cd machine_learning
```

A partir de aquí, **todos los comandos del tutorial se ejecutan desde esta carpeta** (la raíz
del repositorio). Si cierras la terminal, al volver a abrirla tendrás que hacer `cd` hasta
aquí de nuevo.

> **¿Descargar el ZIP en vez de clonar?** Funciona, pero pierdes lo importante: con `git pull`
> recibes las actualizaciones del material durante el curso sin volver a descargar todo.
> Clona.

## 7. Paso 4 — Crear el entorno del curso

Desde la raíz del repositorio (donde están `pyproject.toml` y `uv.lock`), un solo comando:

```bash
uv sync
```

uv descarga Python 3.11 (si no lo tiene ya), crea la carpeta `.venv` dentro del repositorio
e instala en ella los ~250 paquetes del curso con las versiones exactas de `uv.lock`
(~1.5 GB). Tarda entre **2 y 15 minutos** según tu conexión; es normal que se demore en los
paquetes grandes (PyTorch, MLflow). No cierres la terminal. Al final imprime
`Installed 2xx packages`.

### Cómo se usa el entorno: `uv run`

No hace falta "activar" nada. Anteponer `uv run` a cualquier comando lo ejecuta **dentro**
del entorno del curso, desde cualquier terminal:

```bash
uv run python --version
```

Debe responder `Python 3.11.x`. Esa es la regla general del curso: **`uv run` + lo que
quieras ejecutar** (`uv run jupyter lab`, `uv run python script.py`, …).

Si prefieres el estilo clásico de activar el entorno y luego escribir los comandos sin
prefijo, también funciona:

```powershell
.venv\Scripts\activate
```

en Windows, o `source .venv/bin/activate` en macOS/Linux. El *prompt* muestra `(ml-curso)` al
inicio; `deactivate` lo desactiva. Ambas formas son equivalentes; en este tutorial usamos
`uv run` porque no tiene nada que olvidar.

Por último, registra el entorno como *kernel* para que Jupyter y VS Code lo ofrezcan por su
nombre:

```bash
uv run python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
```

### Alternativa sin uv: `venv` + `pip`

Si por alguna razón no puedes usar uv, la ruta equivalente con las herramientas que trae
Python está en [`../docs/guia-entorno.md`](../docs/guia-entorno.md#opción-b--venv--pip).
Requiere tener Python 3.11 instalado y no fija las versiones exactas, por eso uv es la
opción recomendada.

## 8. Paso 5 — Verificar la instalación

Desde la raíz del repositorio:

```bash
uv run modulo-0-instalacion/verificar-entorno.py
```

El script revisa la versión de Python, que el entorno sea el `.venv` del repositorio, que
todas las librerías del curso estén instaladas con una versión adecuada, que el *kernel*
esté registrado y que Git y uv funcionen. Termina con un resumen como este:

```
============================================================
 RESUMEN: 37 OK · 0 advertencias · 0 fallos
 Entorno listo para el curso.
============================================================
```

Si algo falla, el propio mensaje indica qué hacer. Si no logras resolverlo con §14, envía al
docente **la salida completa del script** (copia todo el texto, no una foto de la pantalla).

Ahora la prueba de fuego: abre JupyterLab.

```bash
uv run jupyter lab
```

Se abre el navegador con la interfaz de JupyterLab mostrando las carpetas del repositorio.
Navega a `modulo-1-fundamentos-ciclo-vida/notebooks/` y abre
`01-primer-modelo-aplicado.ipynb`. Arriba a la derecha debe decir **Python (ml-curso)**; si
dice otra cosa, haz clic ahí y selecciónalo. Ejecuta las dos primeras celdas con
Shift + Enter. Si no hay errores, **ya está**.

Para cerrar JupyterLab: en la terminal donde lo lanzaste pulsa Ctrl + C (dos veces si
pregunta). No basta con cerrar la pestaña del navegador.

## 9. Paso 6 — Editor: VS Code o JupyterLab

Puedes trabajar todo el curso solo con JupyterLab. Pero recomendamos **Visual Studio Code**
porque integra en una sola ventana los notebooks, un editor para scripts `.py`, la terminal y
Git, y porque es lo que vas a usar en el proyecto integrador cuando el código deje de caber en
un notebook.

1. Descárgalo desde <https://code.visualstudio.com> e instálalo (en Windows, marca la opción
   *Add "Open with Code" action* durante la instalación; es cómoda).
2. Ábrelo y, en la barra lateral izquierda, entra en **Extensiones** (icono de cuadrados, o
   Ctrl/Cmd + Shift + X). Instala:
   - **Python** (de Microsoft) — trae también *Pylance*.
   - **Jupyter** (de Microsoft).
   - Opcional: **Spanish Language Pack** si prefieres la interfaz en español, y **GitLens**
     para ver el historial de Git dentro del editor.
3. *File → Open Folder* y elige la carpeta `machine_learning` que clonaste. Ábrela
   **siempre desde la raíz**, no desde una subcarpeta: VS Code detecta solo el `.venv` que
   está ahí, y las rutas de los notebooks lo asumen.
4. Abre cualquier `.ipynb`. Arriba a la derecha aparece **Select Kernel**: elige
   *Python Environments* → **ml-curso** (o **`.venv`**; es el mismo). Se recuerda para los
   siguientes notebooks.
5. Para la terminal integrada: *Terminal → New Terminal*. VS Code activa el `.venv` solo al
   abrirla (verás `(ml-curso)` en el *prompt*), así que ahí puedes escribir `python …` sin
   `uv run`. Si no lo hace, `uv run` funciona igual.

### Atajos que ahorran mucho tiempo en los notebooks

| Atajo | Acción |
|---|---|
| Shift + Enter | Ejecutar la celda y pasar a la siguiente |
| Ctrl + Enter | Ejecutar la celda y quedarse en ella |
| Esc, luego `A` / `B` | Insertar celda arriba / abajo |
| Esc, luego `M` / `Y` | Convertir celda a Markdown / a código |
| Esc, luego `D D` | Borrar la celda |
| Tab | Autocompletar |
| Shift + Tab (JupyterLab) | Ver la documentación de la función bajo el cursor |
| *Kernel → Restart Kernel and Run All* | Ejecutar todo desde cero (hazlo antes de entregar) |

## 10. Plan B — Google Colab

[Google Colab](https://colab.research.google.com) es un Jupyter en la nube, gratuito, que solo
requiere una cuenta de Google. Úsalo si:

- tu computador no cumple los requisitos o no puedes instalar software;
- estás de viaje o en un equipo prestado;
- la instalación local falla y no quieres perder la sesión mientras la resuelves.

**No es el plan A** porque las sesiones se desconectan tras un tiempo de inactividad, los
archivos se pierden si no los guardas en Drive, y en el módulo 6 (API, Docker, MLflow) se
queda corto. Pero para los módulos 1 a 5 funciona bien.

### Cómo abrir un notebook del curso en Colab

1. Ve a <https://colab.research.google.com> → pestaña **GitHub** → pega
   `https://github.com/delany-ramirez/machine_learning` → Enter → elige el notebook (o usa el
   botón *Abrir en Colab* del portal del curso).
2. **Al abrir un notebook en Colab, ejecuta la primera celda de código antes que nada**: carga
   los datos del curso. Los notebooks leen datos con rutas relativas (`../datos/archivo.csv`),
   que en Colab no existen; esa primera celda (etiquetada `colab-arranque`) clona el
   repositorio, se ubica en la carpeta correcta e instala lo que Colab no trae. En tu
   computador esa celda no hace nada, así que puedes ejecutarla siempre.
3. Para conservar tus cambios: *Archivo → Guardar una copia en Drive*. Si la sesión se
   reinicia, vuelve a ejecutar la primera celda.

## 11. Herramientas que se instalan más adelante

No las instales ahora; se avisará en la sesión correspondiente.

| Herramienta | Sesión | Notas |
|---|---|---|
| **DVC** | S2 | Ya viene en el entorno del curso. Se inicializa en el repositorio de tu **proyecto integrador**, no en el del curso |
| **MLflow** | S14 (y se menciona en S2) | Ya viene en el entorno. La interfaz se abre con `uv run mlflow ui` |
| **Docker Desktop** | S14 | Descarga: <https://www.docker.com/products/docker-desktop/>. En Windows requiere WSL 2; el instalador lo configura. Si no puedes instalarlo, la sesión incluye una alternativa que ejecuta la API con `uvicorn` sin contenedor |
| **PyTorch con GPU** | Nunca es necesario | El entorno instala PyTorch solo CPU. Si tienes GPU NVIDIA y quieres usarla por curiosidad, hazlo en un entorno aparte siguiendo <https://docs.astral.sh/uv/guides/integration/pytorch/>; no cambies el `pyproject.toml` del curso |

## 12. Mantenimiento durante el curso

### Recibir actualizaciones del material

El repositorio se actualiza antes de cada sesión. Para traer los cambios, desde la raíz del
repositorio:

```bash
git pull
```

Si Git se queja de que tienes cambios locales en un notebook que también cambió en el
repositorio, la salida más simple es guardar tu copia con otro nombre y descartar la
original:

```bash
git checkout -- <ruta/del/notebook.ipynb>
```

y luego `git pull` de nuevo. Consejo: **no edites los notebooks del curso directamente**;
duplícalos con sufijo (`01-primer-modelo-aplicado-mio.ipynb`) y trabaja en la copia. Ver la
FAQ.

### Actualizar el entorno cuando cambie `pyproject.toml` o `uv.lock`

Se avisará en clase cuando ocurra, pero no hace daño ejecutarlo después de cada `git pull`:

```bash
uv sync
```

Instala lo que falte, quita lo que sobre y no toca lo que ya está bien; si no hay cambios
termina en un segundo.

### Empezar de cero

Si el entorno se corrompe (paquetes que se pisan, errores extraños al importar), lo más rápido
es borrarlo y recrearlo. Como los paquetes ya están en la caché de uv, tarda menos que la
primera vez, y nunca afecta a tus archivos:

```bash
uv sync --reinstall
```

Si eso no basta, borra la carpeta `.venv` de la raíz del repositorio y ejecuta `uv sync` de
nuevo.

## 13. Preguntas frecuentes (FAQ)

**¿Puedo usar Python 3.12 o 3.13 que ya tengo instalado?**
No para este curso, y tampoco hace falta decidirlo: `.python-version` fija **3.11** porque es
la versión con la que se verificó todo el material, y uv la descarga dentro del entorno sin
tocar tu otro Python.

**Ya tengo Anaconda / Miniconda. ¿Se estorban?**
No. uv no usa conda para nada. Si tu terminal muestra `(base)` al abrirse, ignóralo: `uv run`
ejecuta siempre el Python del `.venv` del curso. Lo único que debes evitar es instalar
paquetes con `conda install` o `pip install` "a pelo" dentro del entorno del curso.

**¿Tengo que activar el entorno cada vez?**
No si usas `uv run` delante de cada comando (recomendado). Si prefieres activar, es en cada
terminal nueva: `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate`
(macOS/Linux). En VS Code, la terminal integrada lo activa sola y, una vez elegido el kernel,
se recuerda. En JupyterLab, elige el kernel *Python (ml-curso)* en cada notebook nuevo.

**¿Puedo instalar paquetes adicionales?**
Sí, pero con `uv add <paquete>`, que además lo anota en `pyproject.toml` y `uv.lock`. Ten en
cuenta que esos dos archivos son del repositorio del curso: `git pull` te avisará de un
conflicto si el docente también los cambió. Por eso es mejor no instalar nada que no
necesites; y para el proyecto integrador tendrás tu propio `pyproject.toml`.

**¿Puedo trabajar en Windows con WSL?**
Sí, y es una buena opción si ya lo usas: sigue las instrucciones de Linux dentro de WSL. No lo
instales solo por el curso; Windows nativo funciona perfectamente.

**¿Sirve un Mac con chip Apple Silicon (M1/M2/M3/M4)?**
Sí. uv descarga automáticamente el Python y los paquetes nativos para arm64. Un Mac con
procesador Intel también sirve, con una salvedad: las versiones recientes de PyTorch ya no
publican paquetes para Mac Intel, así que en la S13 (redes neuronales) usa el Plan B (Colab).

**¿Sirve una tableta o Chromebook?**
No para instalar localmente. Usa el Plan B (Colab).

**¿Necesito internet durante las sesiones?**
Para instalar y para descargar los datasets que no están en el repositorio (los scripts
`descargar-*.py`, se ejecutan una sola vez). El resto funciona sin conexión.

**¿Cómo evito perder mi trabajo cuando el repositorio se actualiza?**
No edites los notebooks originales. Para cada uno que quieras modificar, haz una copia con
sufijo `-mio` en la misma carpeta (así las rutas a `../datos/` siguen funcionando). Como esas
copias no existen en el repositorio remoto, `git pull` nunca las tocará; solo aparecerán como
"sin seguimiento" (*untracked*) en `git status`, y eso es correcto.

**¿Cómo entrego un notebook?**
Se explica en cada ejercicio, pero la regla general es: *Kernel → Restart Kernel and Run All*
antes de guardar, de modo que el notebook entregado se ejecute limpio de arriba abajo. Un
notebook que solo funciona "si ejecutas primero la celda 14" no se considera terminado.

**Mi antivirus / el proxy de la empresa bloquea las descargas.**
Prueba desde otra red (los datos del móvil suelen bastar para la instalación inicial). Si es
un equipo corporativo con políticas, usa el Plan B.

**¿Qué hago si nada de esto funciona?**
Escríbele al docente **antes** de la primera sesión con: sistema operativo, qué paso falló y
el texto completo del error (copiado, no en foto). Parte de la S1 se reserva para resolver
instalaciones, pero llegar con el problema identificado ahorra mucho tiempo.

## 14. Problemas frecuentes y su solución

| Síntoma | Causa probable | Solución |
|---|---|---|
| `'uv' no se reconoce como un comando…` (Windows) | La terminal se abrió antes de instalar uv, o el instalador no pudo añadirlo al PATH | Cierra **todas** las ventanas de PowerShell y abre una nueva. Si persiste, ejecuta de nuevo el instalador del Paso 2 y lee su mensaje final |
| `uv: command not found` (macOS/Linux) | La terminal no recargó el PATH | Cierra y abre la terminal. Si persiste: `source ~/.local/bin/env` y, para dejarlo fijo, vuelve a ejecutar el instalador |
| PowerShell: `…no se puede cargar porque la ejecución de scripts está deshabilitada` | Política de ejecución de PowerShell (afecta a `.venv\Scripts\activate`, no a `uv run`) | Usa `uv run`, o ejecuta una vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y confirma con `S` |
| `error: No pyproject.toml found in current directory or any parent directory` | No estás en la raíz del repositorio | `cd` hasta la carpeta `machine_learning` (comprueba con `dir` / `ls` que ves `pyproject.toml`) |
| `uv sync` falla con `Failed to download` / `error sending request` / *timeout* | Red que bloquea o corta la descarga | Vuelve a ejecutar `uv sync` (retoma donde quedó); cambia de red; si hay proxy, define la variable de entorno `HTTPS_PROXY` |
| `uv sync` falla con `No solution found` o dice que no hay *wheel* para tu plataforma | Plataforma sin paquetes precompilados (p. ej. Mac Intel con PyTorch) o Python de 32 bits | Envía la salida completa al docente; mientras tanto, Plan B |
| `ModuleNotFoundError: No module named 'sklearn'` en la terminal | El comando corrió con otro Python (el del sistema o el de conda) | Antepón `uv run` al comando, o activa el `.venv` |
| `ModuleNotFoundError` **dentro de un notebook** aunque en la terminal funciona | El notebook usa otro kernel | Arriba a la derecha selecciona **Python (ml-curso)**. Si no aparece, ejecuta el comando de `ipykernel install` del Paso 4 |
| El kernel "muere" al importar `lightgbm` en macOS | Falta la librería OpenMP | `brew install libomp` |
| `FileNotFoundError: ../datos/…csv` | Jupyter se abrió desde otra carpeta o el notebook se movió | Abre JupyterLab / VS Code desde la raíz del repositorio y no muevas los notebooks fuera de su carpeta |
| `jupyter lab` no abre el navegador | Terminal remota, WSL o navegador por defecto no configurado | Copia en el navegador la URL `http://localhost:8888/lab?token=…` que aparece en la terminal |
| `Port 8888 is already in use` | Otro JupyterLab sigue abierto | Ciérralo con Ctrl + C en su terminal, o usa `uv run jupyter lab --port 8889` |
| Las gráficas no aparecen | Backend de matplotlib | Añade `%matplotlib inline` en la primera celda de código |
| `UnicodeDecodeError` al leer un CSV con tildes | Codificación del sistema (Windows) | `pd.read_csv(ruta, encoding="utf-8")` |
| Errores raros con rutas que tienen tildes, eñes o espacios | Algunas librerías no las manejan bien | Clona el repositorio en una ruta sin esos caracteres (`C:\proyectos`) y vuelve a ejecutar `uv sync` ahí |
| El entorno se rompe o se vuelve lentísimo sin razón | Carpeta sincronizada por OneDrive / Drive / iCloud | Mueve el repositorio fuera de la carpeta sincronizada y ejecuta `uv sync` de nuevo |
| Windows: `error: could not create '…': Filename too long` | Límite de longitud de rutas | Ejecuta como administrador: `git config --system core.longpaths true` |
| El notebook funciona a trozos pero *Run All* falla | Celdas ejecutadas en desorden; variables que ya no existen | *Kernel → Restart Kernel and Run All* y corrige de arriba hacia abajo |
| `git pull` dice `Your local changes would be overwritten` | Editaste un notebook del curso | Guarda tu copia con otro nombre, `git checkout -- <archivo>` y repite `git pull` |
| `git pull` dice que hay conflicto en `uv.lock` o `pyproject.toml` | Instalaste paquetes con `uv add` y el docente también cambió esos archivos | `git checkout -- uv.lock pyproject.toml`, `git pull` y luego `uv sync` (vuelve a añadir lo tuyo después si lo necesitas) |
| `uv sync` falla por falta de espacio en disco | El entorno más la caché de uv ocupan ~4 GB | Libera espacio y vuelve a ejecutar `uv sync`. `uv cache clean` borra la caché si necesitas recuperar espacio después |

## 15. Glosario mínimo

| Término | Qué es |
|---|---|
| **Terminal** (consola, shell) | Ventana donde escribes comandos de texto en vez de hacer clic |
| **Prompt** | El texto al inicio de la línea de la terminal que indica que está lista para recibir un comando. Si el entorno está activado, lo muestra entre paréntesis: `(ml-curso)` |
| **Ruta** (*path*) | Dirección de un archivo o carpeta. *Absoluta* si empieza desde la raíz del disco (`C:\proyectos\…`); *relativa* si parte de la carpeta actual (`../datos/archivo.csv`, donde `..` es "la carpeta de arriba") |
| **Paquete / librería** | Código de terceros que se instala y se importa (`import pandas`) |
| **Entorno virtual** | Carpeta aislada con su propio Python y sus propios paquetes; en este curso, `.venv` en la raíz del repositorio |
| **uv** | Gestor de Python, de entornos y de paquetes. `pip` es el gestor de paquetes clásico de Python; uv lo reemplaza y es mucho más rápido |
| **`pyproject.toml`** | Archivo que declara qué necesita el proyecto (versión de Python y librerías). Es el estándar actual de Python |
| **`uv.lock`** | Archivo generado por uv con la versión exacta de cada paquete instalado; garantiza que todos tengamos el mismo entorno |
| **Notebook** (`.ipynb`) | Documento con celdas de texto y de código que se ejecutan en orden; el formato de todos los ejemplos del curso |
| **Kernel** | El proceso de Python que ejecuta las celdas de un notebook. Cada entorno virtual puede registrarse como un kernel distinto |
| **JupyterLab** | Aplicación web (corre en tu máquina) para editar y ejecutar notebooks |
| **Repositorio** | Carpeta de un proyecto con su historial de versiones gestionado por Git |
| **Clonar** / **pull** | Descargar un repositorio por primera vez / traer sus cambios más recientes |
| **Commit** | Una instantánea guardada del proyecto en Git, con autor, fecha y mensaje |

## 16. Lista de verificación final

Marca cada punto antes de la S1:

- [ ] `git --version` responde en la terminal.
- [ ] Git tiene configurados mi nombre y mi correo.
- [ ] Tengo cuenta en GitHub.
- [ ] `uv --version` responde en la terminal.
- [ ] Cloné el repositorio en una carpeta sin espacios ni tildes, fuera de OneDrive/Drive.
- [ ] `uv sync` terminó sin errores y `uv run python --version` responde `Python 3.11.x`.
- [ ] `uv run modulo-0-instalacion/verificar-entorno.py` termina con "Entorno listo para el
      curso".
- [ ] Abrí `01-primer-modelo-aplicado.ipynb` con el kernel *Python (ml-curso)* y las primeras
      celdas se ejecutan sin error.
- [ ] (Recomendado) VS Code instalado con las extensiones Python y Jupyter, y sabe encontrar
      el kernel `ml-curso`.
- [ ] Sé cómo traer actualizaciones del repositorio (`git pull` y luego `uv sync`).

Cuando todo esté marcado, estás listo para la **Sesión 1**:
[`../modulo-1-fundamentos-ciclo-vida/`](../modulo-1-fundamentos-ciclo-vida/).

---

> Versión corta de estas instrucciones: [`../docs/guia-entorno.md`](../docs/guia-entorno.md).
> Programa completo del curso: [`../docs/programa.md`](../docs/programa.md).

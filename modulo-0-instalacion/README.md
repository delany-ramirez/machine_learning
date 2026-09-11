# Módulo 0 — Instalación del software (antes de la S1)

> **Objetivo.** Que llegues a la primera sesión con todo instalado y probado, de modo que el
> tiempo de clase se dedique al contenido y no a arreglar computadores. Sigue este tutorial
> **completo y en orden**; al final ejecutas un script que te dice si todo quedó bien.
>
> **Tiempo estimado:** 45–90 minutos, según la velocidad de tu conexión (se descargan
> ~1.5 GB de paquetes). Hazlo con calma y con buena conexión, no la noche anterior.

Si ya tienes experiencia con Python y conda, la versión corta está en
[`../docs/guia-entorno.md`](../docs/guia-entorno.md). Este documento es la versión larga,
pensada para quien parte de cero o quiere entender qué está instalando y por qué.

## Contenido

1. [Qué vas a instalar y por qué](#1-qué-vas-a-instalar-y-por-qué)
2. [Requisitos de tu computador](#2-requisitos-de-tu-computador)
3. [La terminal: tu herramienta de trabajo](#3-la-terminal-tu-herramienta-de-trabajo)
4. [Paso 1 — Git](#4-paso-1--git)
5. [Paso 2 — Miniconda (Python)](#5-paso-2--miniconda-python)
6. [Paso 3 — Descargar el repositorio del curso](#6-paso-3--descargar-el-repositorio-del-curso)
7. [Paso 4 — Crear el entorno `ml-curso`](#7-paso-4--crear-el-entorno-ml-curso)
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
| **Miniconda** | Instala Python 3.11 y gestiona el *entorno virtual* `ml-curso` con todas las librerías | Todo el curso |
| **Entorno `ml-curso`** | NumPy, pandas, scikit-learn, matplotlib, XGBoost, LightGBM, PyTorch, MLflow, etc. — todo con versiones compatibles entre sí | Todo el curso |
| **JupyterLab** (viene en el entorno) | Ejecutar los notebooks del curso | Todo el curso |
| **VS Code** (opcional pero recomendado) | Editor con soporte para notebooks, terminal integrada y Git | Todo el curso |
| **Cuenta en GitHub** | Alojar el repositorio de tu proyecto integrador | Desde la S2 |
| **Docker Desktop** | Empaquetar la API del proyecto | Solo en la S14; ver §11 |

### ¿Por qué un entorno virtual y no "instalar Python y ya"?

Las librerías de ML dependen unas de otras con versiones muy concretas. Si instalas todo en el
Python "global" de tu máquina, tarde o temprano dos proyectos piden versiones incompatibles y
se rompe alguno. Un **entorno virtual** es una carpeta aislada con su propio Python y sus
propias librerías. El archivo [`../environment.yml`](../environment.yml) describe exactamente
qué debe haber dentro, así que todos los estudiantes y el docente trabajamos con el mismo
entorno y "en mi máquina sí funciona" deja de ser un problema.

Esto es, además, el primer contenido del curso: un proyecto de ML **reproducible** empieza por
un entorno reproducible (S1 y S2).

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
| **Windows** | **Anaconda Prompt** (aparece en el menú Inicio después de instalar Miniconda). Antes de instalar Miniconda, usa **PowerShell** | Menú Inicio → escribe `Anaconda Prompt` |
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

## 5. Paso 2 — Miniconda (Python)

Instalamos **Miniconda**, no Anaconda. Anaconda trae cientos de paquetes que no vamos a usar y
ocupa varios GB; Miniconda solo trae Python y `conda`, y nosotros instalamos justo lo que
necesitamos.

> Si ya tienes Anaconda instalado y funcionando, no lo desinstales: sirve igual. Salta a la
> verificación al final de esta sección.

### Windows

1. Descarga el instalador de 64 bits desde
   <https://www.anaconda.com/download/success> (sección *Miniconda Installers*).
2. Ejecútalo con estas opciones:
   - *Install for:* **Just Me**.
   - *Destination folder:* deja la que propone (`C:\Users\<tu-usuario>\miniconda3`).
     **Importante:** la ruta no debe tener tildes, eñes ni espacios. Si tu nombre de usuario de
     Windows los tiene, instala en `C:\miniconda3`.
   - Marca **"Register Miniconda3 as my default Python"** y deja **desmarcada** la de
     *Add to PATH* (no hace falta; usaremos Anaconda Prompt).
3. Al terminar, abre **Anaconda Prompt** desde el menú Inicio. Verás `(base)` al inicio de la
   línea: es el entorno por defecto de conda.

### macOS

Descarga el instalador `.pkg` para tu procesador (Apple Silicon M1/M2/M3/M4, o Intel) desde
<https://www.anaconda.com/download/success> y ejecútalo con las opciones por defecto. Luego
cierra Terminal, ábrela de nuevo y deberías ver `(base)` en el *prompt*.

¿No sabes qué procesador tienes? → menú Apple → *Acerca de este Mac* → *Chip*.

### Linux

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
```

```bash
bash ~/miniconda.sh -b -p ~/miniconda3
```

```bash
~/miniconda3/bin/conda init bash
```

(si usas `zsh`, reemplaza `bash` por `zsh`). Cierra la terminal y ábrela de nuevo.

### Verificación (todos los sistemas)

```bash
conda --version
```

Debe responder `conda 2x.x.x`. Si dice que no reconoce el comando, ve a §14 ("`conda` no se
reconoce").

Dos ajustes recomendados, una sola vez. El primero activa el *solver* rápido (evita que crear
el entorno tarde una hora):

```bash
conda config --set solver libmamba
```

El segundo evita que conda active `base` cada vez que abres la terminal (opcional; a muchos
les resulta molesto):

```bash
conda config --set auto_activate_base false
```

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

## 7. Paso 4 — Crear el entorno `ml-curso`

Desde la raíz del repositorio (donde está `environment.yml`):

```bash
conda env create -f environment.yml
```

Esto descarga e instala unos 250 paquetes (~1.5 GB). Tarda entre **5 y 20 minutos** según
tu conexión. Es normal que parezca detenido durante un rato en "Solving environment" o al
descargar los paquetes grandes (PyTorch, MLflow). No cierres la terminal.

Cuando termine, actívalo:

```bash
conda activate ml-curso
```

El *prompt* debe cambiar de `(base)` a `(ml-curso)`. **Cada vez que abras una terminal para
trabajar en el curso tendrás que ejecutar este comando**; es la causa número uno de "no me
encuentra el paquete".

Por último, registra el entorno como *kernel* para que Jupyter y VS Code lo ofrezcan por su
nombre:

```bash
python -m ipykernel install --user --name ml-curso --display-name "Python (ml-curso)"
```

### Alternativa sin conda: `venv` + `pip`

Si por alguna razón no puedes usar conda (por ejemplo, ya tienes Python 3.11 instalado y
prefieres no añadir otro gestor), la ruta equivalente está en
[`../docs/guia-entorno.md`](../docs/guia-entorno.md#opción-b--venv--pip). Es más frágil en
Windows (LightGBM y XGBoost a veces requieren compiladores), por eso conda es la opción
recomendada.

## 8. Paso 5 — Verificar la instalación

Con el entorno activo (`(ml-curso)` visible en el *prompt*) y desde la raíz del repositorio:

```bash
python modulo-0-instalacion/verificar-entorno.py
```

El script revisa la versión de Python, que todas las librerías del curso estén instaladas con
una versión adecuada, que el *kernel* esté registrado y que Git funcione. Termina con un
resumen como este:

```
============================================================
 RESUMEN: 34 OK · 0 advertencias · 0 fallos
 Entorno listo para el curso.
============================================================
```

Si algo falla, el propio mensaje indica qué hacer. Si no logras resolverlo con §14, envía al
docente **la salida completa del script** (copia todo el texto, no una foto de la pantalla).

Ahora la prueba de fuego: abre JupyterLab.

```bash
jupyter lab
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
   **siempre desde la raíz**, no desde una subcarpeta: las rutas de los notebooks lo asumen.
4. Abre cualquier `.ipynb`. Arriba a la derecha aparece **Select Kernel**: elige
   *Python Environments* → **ml-curso**. Se recuerda para los siguientes notebooks.
5. Para la terminal integrada: *Terminal → New Terminal*. En Windows, si la terminal que abre
   es PowerShell y `conda` no responde, cambia el perfil por defecto a *Command Prompt* (menú
   desplegable junto al `+` de la terminal → *Select Default Profile*).

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
   `https://github.com/delany-ramirez/machine_learning` → Enter → elige el notebook.
2. Los notebooks leen datos con rutas relativas (`../datos/archivo.csv`), que en Colab no
   existen. Añade **una celda al inicio** que clone el repositorio y se ubique en la carpeta
   correcta:

```python
!git clone -q https://github.com/delany-ramirez/machine_learning.git
%cd machine_learning/modulo-1-fundamentos-ciclo-vida/notebooks
```

(cambia la carpeta del módulo según el notebook que estés usando).

3. Colab trae NumPy, pandas, scikit-learn, matplotlib, XGBoost, LightGBM y PyTorch. Lo que no
   trae se instala en una celda:

```python
!pip install -q statsmodels shap optuna umap-learn imbalanced-learn ucimlrepo mlflow
```

4. Para conservar tus cambios: *Archivo → Guardar una copia en Drive*.

## 11. Herramientas que se instalan más adelante

No las instales ahora; se avisará en la sesión correspondiente.

| Herramienta | Sesión | Notas |
|---|---|---|
| **DVC** | S2 | Ya viene en el entorno `ml-curso`. Se inicializa en el repositorio de tu **proyecto integrador**, no en el del curso |
| **MLflow** | S14 (y se menciona en S2) | Ya viene en el entorno. La interfaz se abre con `mlflow ui` |
| **Docker Desktop** | S14 | Descarga: <https://www.docker.com/products/docker-desktop/>. En Windows requiere WSL 2; el instalador lo configura. Si no puedes instalarlo, la sesión incluye una alternativa que ejecuta la API con `uvicorn` sin contenedor |
| **PyTorch con GPU** | Nunca es necesario | Si tienes GPU NVIDIA y quieres usarla por curiosidad, sigue el selector de <https://pytorch.org/get-started/locally/> dentro del entorno activo |

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

### Actualizar el entorno cuando cambie `environment.yml`

Se avisará en clase cuando ocurra. Con el entorno activo:

```bash
conda env update -f environment.yml --prune
```

### Empezar de cero

Si el entorno se corrompe (paquetes que se pisan, errores extraños al importar), lo más rápido
es borrarlo y recrearlo. Tarda lo mismo que la primera vez y nunca afecta a tus archivos:

```bash
conda deactivate
```

```bash
conda env remove -n ml-curso
```

```bash
conda env create -f environment.yml
```

## 13. Preguntas frecuentes (FAQ)

**¿Puedo usar Python 3.12 o 3.13 que ya tengo instalado?**
No para este curso. El entorno fija **3.11** porque es la versión con la que se verificó todo
el material y con la que todas las librerías tienen ruedas precompiladas. Miniconda instala
3.11 dentro del entorno sin tocar tu otro Python.

**Ya tengo Anaconda / otro entorno conda. ¿Se estorban?**
No. Cada entorno es independiente. Solo asegúrate de activar `ml-curso` cuando trabajes en el
curso.

**¿Tengo que activar el entorno cada vez?**
Sí, en cada terminal nueva: `conda activate ml-curso`. En VS Code, una vez elegido el kernel
se recuerda. En JupyterLab, elige el kernel *Python (ml-curso)* en cada notebook nuevo.

**¿Puedo instalar paquetes adicionales?**
Sí, con el entorno activo: `conda install -c conda-forge <paquete>` o, si no existe en conda,
`pip install <paquete>`. No instales nada que no necesites: cada paquete extra es una
posible incompatibilidad. Y nunca uses `pip install` con `(base)` activo.

**¿Puedo trabajar en Windows con WSL?**
Sí, y es una buena opción si ya lo usas: sigue las instrucciones de Linux dentro de WSL. No lo
instales solo por el curso; Windows nativo funciona perfectamente.

**¿Sirve un Mac con chip Apple Silicon (M1/M2/M3/M4)?**
Sí. Usa el instalador de Miniconda para Apple Silicon (arm64). Todas las librerías del curso
tienen versión nativa.

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

**Mi antivirus / el proxy de la empresa bloquea las descargas de conda.**
Prueba desde otra red (los datos del móvil suelen bastar para la instalación inicial). Si es
un equipo corporativo con políticas, usa el Plan B.

**¿Qué hago si nada de esto funciona?**
Escríbele al docente **antes** de la primera sesión con: sistema operativo, qué paso falló y
el texto completo del error (copiado, no en foto). Parte de la S1 se reserva para resolver
instalaciones, pero llegar con el problema identificado ahorra mucho tiempo.

## 14. Problemas frecuentes y su solución

| Síntoma | Causa probable | Solución |
|---|---|---|
| `'conda' no se reconoce como un comando…` (Windows) | Estás en PowerShell o CMD normal, no en Anaconda Prompt | Abre **Anaconda Prompt** desde el menú Inicio. Si quieres conda en PowerShell: ejecuta `conda init powershell` desde Anaconda Prompt y reinicia PowerShell |
| `conda: command not found` (macOS/Linux) | La terminal no cargó la configuración de conda | Cierra y abre la terminal. Si persiste: `~/miniconda3/bin/conda init zsh` (o `bash`) y reinicia |
| PowerShell: `…no se puede cargar porque la ejecución de scripts está deshabilitada` | Política de ejecución de PowerShell | Ejecuta en PowerShell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y confirma con `S` |
| `CondaError: Run 'conda init' before 'conda activate'` | conda no está inicializado en esa terminal | `conda init` (elige tu shell) y reinicia la terminal |
| `Solving environment` lleva más de 20 minutos | *Solver* clásico | Ctrl + C, luego `conda config --set solver libmamba` y vuelve a crear el entorno |
| `CondaHTTPError` / `Connection timed out` | Red que bloquea o corta la descarga | Reintenta; cambia de red; si hay proxy, configúralo con `conda config --set proxy_servers.https http://…` |
| `EnvironmentNameNotFound: Could not find conda environment: ml-curso` | El entorno no se creó (falló a mitad) o estás en otra instalación de conda | `conda env list` para ver qué hay; vuelve a ejecutar `conda env create -f environment.yml` |
| `No such file or directory: environment.yml` | No estás en la raíz del repositorio | `cd` hasta la carpeta `machine_learning` (comprueba con `dir` / `ls` que ves `environment.yml`) |
| `ModuleNotFoundError: No module named 'sklearn'` en la terminal | El entorno no está activo | `conda activate ml-curso` y repite |
| `ModuleNotFoundError` **dentro de un notebook** aunque en la terminal funciona | El notebook usa otro kernel | Arriba a la derecha selecciona **Python (ml-curso)**. Si no aparece, ejecuta el comando de `ipykernel install` del Paso 4 |
| El kernel "muere" al importar `lightgbm` en macOS | Falta la librería OpenMP | `conda install -c conda-forge llvm-openmp` (o `brew install libomp`) |
| `FileNotFoundError: ../datos/…csv` | Jupyter se abrió desde otra carpeta o el notebook se movió | Abre JupyterLab / VS Code desde la raíz del repositorio y no muevas los notebooks fuera de su carpeta |
| `jupyter lab` no abre el navegador | Terminal remota, WSL o navegador por defecto no configurado | Copia en el navegador la URL `http://localhost:8888/lab?token=…` que aparece en la terminal |
| `Port 8888 is already in use` | Otro JupyterLab sigue abierto | Ciérralo con Ctrl + C en su terminal, o usa `jupyter lab --port 8889` |
| Las gráficas no aparecen | Backend de matplotlib | Añade `%matplotlib inline` en la primera celda de código |
| `UnicodeDecodeError` al leer un CSV con tildes | Codificación del sistema (Windows) | `pd.read_csv(ruta, encoding="utf-8")` |
| Errores raros con rutas que tienen tildes, eñes o espacios | Algunas librerías no las manejan bien | Reinstala Miniconda y clona el repositorio en una ruta sin esos caracteres (`C:\proyectos`) |
| El entorno se rompe o se vuelve lentísimo sin razón | Carpeta sincronizada por OneDrive / Drive / iCloud | Mueve el repositorio y (si aplica) Miniconda fuera de la carpeta sincronizada |
| Windows: `error: could not create '…': Filename too long` | Límite de longitud de rutas | Ejecuta como administrador: `git config --system core.longpaths true` |
| El notebook funciona a trozos pero *Run All* falla | Celdas ejecutadas en desorden; variables que ya no existen | *Kernel → Restart Kernel and Run All* y corrige de arriba hacia abajo |
| `git pull` dice `Your local changes would be overwritten` | Editaste un notebook del curso | Guarda tu copia con otro nombre, `git checkout -- <archivo>` y repite `git pull` |
| `import torch` falla con `OSError: [WinError 127] … shm.dll` (Windows) | Se instaló la rueda de pip de PyTorch dentro de un entorno conda; no es compatible | Con el entorno activo: `pip uninstall -y torch` y luego `conda install -c conda-forge pytorch-cpu` |
| La creación del entorno falla por falta de espacio en disco | El entorno ocupa ~4 GB instalado | Libera espacio y vuelve a ejecutar `conda env create -f environment.yml` |

## 15. Glosario mínimo

| Término | Qué es |
|---|---|
| **Terminal** (consola, shell) | Ventana donde escribes comandos de texto en vez de hacer clic |
| **Prompt** | El texto al inicio de la línea de la terminal que indica que está lista para recibir un comando. Muestra el entorno activo entre paréntesis: `(ml-curso)` |
| **Ruta** (*path*) | Dirección de un archivo o carpeta. *Absoluta* si empieza desde la raíz del disco (`C:\proyectos\…`); *relativa* si parte de la carpeta actual (`../datos/archivo.csv`, donde `..` es "la carpeta de arriba") |
| **Paquete / librería** | Código de terceros que se instala y se importa (`import pandas`) |
| **Entorno virtual** | Carpeta aislada con su propio Python y sus propios paquetes; en este curso, `ml-curso` |
| **conda** | Gestor de paquetes y de entornos; `pip` es el gestor de paquetes propio de Python (conda puede usarlo por dentro) |
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
- [ ] `conda --version` responde en la terminal.
- [ ] Cloné el repositorio en una carpeta sin espacios ni tildes, fuera de OneDrive/Drive.
- [ ] `conda activate ml-curso` cambia el *prompt* a `(ml-curso)`.
- [ ] `python modulo-0-instalacion/verificar-entorno.py` termina con "Entorno listo para el
      curso".
- [ ] Abrí `01-primer-modelo-aplicado.ipynb` con el kernel *Python (ml-curso)* y las primeras
      celdas se ejecutan sin error.
- [ ] (Recomendado) VS Code instalado con las extensiones Python y Jupyter, y sabe encontrar
      el kernel `ml-curso`.
- [ ] Sé cómo traer actualizaciones del repositorio (`git pull`).

Cuando todo esté marcado, estás listo para la **Sesión 1**:
[`../modulo-1-fundamentos-ciclo-vida/`](../modulo-1-fundamentos-ciclo-vida/).

---

> Versión corta de estas instrucciones: [`../docs/guia-entorno.md`](../docs/guia-entorno.md).
> Programa completo del curso: [`../docs/programa.md`](../docs/programa.md).

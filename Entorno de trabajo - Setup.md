<p style="text-align: center">
    <img src="./assets/images/untref-logo-negro.svg" style="height: 50px;" />
</p>

<h3 style="text-align: center">Estructuras de Datos</h3>

<h2 style="text-align: center">Entorno de trabajo: Setup</h3>

### Python

Instalar el intérprete de Python desde: https://www.python.org

En Windows, seguir el siguiente paso a paso: [Instalación de Python en Windows](https://docs.google.com/presentation/d/e/2PACX-1vQiVJDxx3hmVxbisIlkxYQstgI-SlN3bKamBId0GmNJ2g9m6d8UryGeQFZqt-WwZp0pPEatTR9nUMgD/pub)

Si surgen problemas, esta sección explica en detalle el proceso de instalación y configuración de Python en Windows: [Uso de Python en Windows](https://docs.python.org/es/3/using/windows.html)

### Entornos virtuales en Python

Son entornos aislados que permiten instalar paquetes para que los use una aplicación en particular, en lugar de instalarlos en todo el sistema.

#### `venv`

Administrador de entornos que está incluido en la biblioteca estándar de Python, viene incluido al instalar el intérprete.

La documentación oficial se encuentra en [venv — Creation of virtual environments](https://docs.python.org/es/3/library/venv.html).

Otro recurso muy completo es: [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

#### `pyenv`

Un administrador de entornos virtuales que permite instalar diferentes versiones de Python.

##### Linux / MacOS

[pyenv](https://github.com/pyenv/pyenv) + [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

##### Windows

[pyenv-win](https://github.com/pyenv-win/pyenv-win) + [pyenv-win-venv](https://github.com/pyenv-win/pyenv-win-venv)

### Dependencias necesarias

```shell
pip install jupyterlab
```


# edd

Este paquete de Python contiene el código de las estructuras de datos y
funciones que se utilizan durante las clases de la materia Estructuras de Datos.

## Instalación

Hay dos formas de instalar este paquete en sus sistemas. _(Siempre recomendamos
crear un entorno virtual al momento de instalar paquetes)_.

### Desde GitHub

```sh
pip install --editable "git+https://github.com/untref-edd/edd.git#egg=edd&subdirectory=code"
```

si tuvieran que actualizar el paquete, deben ejecutar:

```sh
pip install --upgrade --editable "git+https://github.com/untref-edd/edd.git#egg=edd&subdirectory=code"
```

### Clonando este mismo repositorio (_recomendado_)

```sh
git clone ${GIT_URL}
cd edd
pip install --editable ./code
```

Para actualizar en este caso, solo debemos hacer `git-pull` de los últimos
cambios en el repositorio.

### ¿Cómo usar el módulo `edd`?

Una vez instalado podemos verificar que el paquete esté disponible ejecutando:

```sh
python -c "import edd"
```

La ausencia de un mensaje indica que todo se instaló correctamente. De lo
contrario veremos algo como:

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'edd'
```

Luego, podemos probar el paquete con este pequeño programa de ejemplo, en un
archivo llamado `prueba_grafo.py` copiamos:

```python
from edd.grafo import DiGrafo


def main() -> None:
    G = DiGrafo()
    G.agregar_arista("A", "B", 2)
    G.agregar_arista("B", "C", 3)
    G.agregar_arista("B", "D", 1)
    G.agregar_arista("D", "A", 2)
    print(G)


if __name__ == "__main__":
    main()
```

luego ejecutamos:

```sh
python ./prueba_grafo.py
```

y deberíamos ver:

```text
Vertices: {C, B, A, D}

    B --1--> D
    B --3--> C
    A --2--> B
    D --2--> A
```

## Desinstalación

Simplemente desinstalamos el paquete `edd` como en cualquier otro caso:

```sh
pip uninstall edd
```

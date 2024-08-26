# Notas para el setup en MacOS

Si al momento de hacer `make install`, se presenta el siguiente error:

```text
Failed to build pygraphviz
ERROR: Could not build wheels for pygraphviz, which is required to install pyproject.toml-based projects
```

Instalar utilizando el siguiente comando y luego volver a ejecutar `make install`.

```sh
pip install --config-settings="--global-option=build_ext" \
            --config-settings="--global-option=-I$(brew --prefix graphviz)/include/" \
            --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/" \
            pygraphviz
```

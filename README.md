# pyvista-mypy-plugin
Mypy plugin for the PyVista project.

This plugin is primarily used for type-promotion between related classes that do not
inherit from each other. For example, the abstract class `pyvista.DataSet` does not
inherit from `vtk.vtkDataSet`, and will generate type errors wherever a `vtk.vtkDataSet`
is expected. Without this plugin, the following is a type error:

``` python
from pyvista import DataSet
from vtkmodules.vtkCommonDataModel import vtkDataSet

x: vtkDataSet
x = DataSet()  # error: Incompatible types in assignment (expression has type "DataSet", variable has type "vtkDataSet")'
```

(Note that the example above is not valid at runtime since `DataSet` is an abstract
class and cannot be instantiated.)

With this plugin, `DataSet` is promoted as type `vtkDataSet`, allowing `DataSet`
type to be used wherever `vtkDataSet` is used.

## Installation

Dependencies:
- [mypy](https://github.com/python/mypy)
- [pyvista](https://github.com/pyvista/pyvista)
- [vtk](https://pypi.org/project/vtk/)

Install it with:

``` bash
python -m pip install pyvista-mypy-plugin
```

Alternatively, add `pyvista-mypy-plugin` as a project dependency wherever `mypy` is
used, e.g. as an optional dev requirement in `pyproject.toml`:

``` toml
[project.optional-dependencies]
dev = ["mypy", "pyvista-mypy-plugin"]
```

## Usage

To enable the plugin, it must be added to your project's mypy configuration file.
E.g. add the following to `pyproject.toml`:

``` toml
[tool.mypy]
plugins = [
  'pyvista_mypy_plugin',
]
```

## Testing

First, install `pyvista-mypy-plugin` with dev requirements:
``` bash
python -m pip install pyvista-mypy-plugin[dev]
```

To run the tests, execute:
``` bash
pytest
```

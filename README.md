
## Introduction

This package is an extension of the symbolical C++ library lib3d_mec_ginac for Python.

[lib3d_mec_ginac](http://www.imem.unavarra.es/3d_mec/download/lib3d-mec-ginac/eccomas2007_paper.pdf) provides all the features of a modern symbolic kernel (matrix algebra, expressions atomization, trigonometric simplifications, ...).
It is designed specifically to pose and solve equations in dynamical mechanical multibody systems.

pylib3d_mec_ginac brings all the features of this library to a high level interpreted language with a clean and easy to use API and a graphical user interface to visualize mechanical simulations.


## Installation

You will need al least python==3.7 and ubuntu OS ( 64-bit ). For the time being, only
ubuntu 18.04 system was tested succesfully. Later versions of ubuntu and python may also work.


You can use [this script](install.sh) to install this library and its dependencies in your system, or just run the next code in your bash console:

```bash
curl https://raw.githubusercontent.com/Vykstorm/pylib3d-mec-ginac/stable/install.sh | bash
```

### Debugging

```bash
python setup.py --debug install
```

### Compiling and Installing

To compile and install the Python library with full GUI and 3D viewer support:

```bash
INSTALL_GUI=yes python setup.py install
```

To compile and install only the core symbolic engine without GUI dependencies:

```bash
INSTALL_GUI=no python setup.py install
```

## Usage

This software can be used in different ways.

#### As a python module

Import all the functions & classes of this library inside the python interpreter
and embed its features to your applications.

```bash
python
>>> from lib3d_mec_ginac import *
>>> ...
```

### PyQt IDE

A standalone IDE built with PyQt5 that provides three integrated panels in a single window:

```
┌────────────────────┬──────────────────────────┐
│                    │                          │
│   Code Editor      │   3D VTK Visualizer     │
│   (Python syntax   │   (mechanical scene,    │
│    highlighting,   │    mouse interaction,    │
│    line numbers)   │    object picking)       │
│                    │                          │
├────────────────────┴──────────────────────────┤
│                                               │
│   Interactive Python Console (>>> prompt)      │
│   (shared namespace with the editor)          │
│                                               │
└───────────────────────────────────────────────┘
```

**Features:**
- **Code Editor**: Python syntax highlighting (QScintilla), line numbers, auto-indentation, dark theme
- **3D Viewer**: VTK-based 3D visualizer with mouse rotation/zoom/pan and object picking
- **Interactive Console**: Python REPL with shared namespace — execute a script with ▶ Run and then inspect variables in the console
- **Clean execution**: Each ▶ Run resets the namespace, so every execution starts fresh
- **Menus**: File (New/Open/Save), Edit (Run/Reset), Simulation (Start/Stop/Pause), Scene (toggle visibility of points, vectors, frames, solids, grid)
- **Keyboard shortcuts**: `F5` Run, `Ctrl+S` Save, `Ctrl+O` Open, `Ctrl+N` New, `Ctrl+Q` Quit

**Launch it as a standalone program:**
```bash
python src/gui/pyqt/mec_ginac_ide.py
```

**Dependencies:** `PyQt5`, `QScintilla` (install with `pip install PyQt5 QScintilla`)


## Documentation

Most of the classes and methods of the API are documented.
You can use the command ```help``` inside the Python interpreter to get information about them
e.g:
```python
from lib3d_mec_ginac import System
help(System)
```
## Examples


This library provides a few usage examples under the directory [examples/](examples/)
Here we list a few of them

#### Four bar linkage

Go to the directory where you downloaded this
repository and run this example with:
```
python -m lib3d_mec_ginac examples/four_bar
```


#### Simple pendulum

Go to the directory where you downloaded this repository and run this example with:
```
python -m lib3d_mec_ginac examples/simple_pendulum
```



## License

This project is under [GPLv2 license](LICENSE.txt)

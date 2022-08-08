# Pycell
## Cellular automata simulation written in Python
### Features
- Basic rectangular grid (currently not zoomable/scrollable)
- Cells represented through a sparse matrix
- Ability to run simulation at different speeds, view statistics, and configure the display
- Support for multiple automata rulesets

### Planned Features (in order of priority)
- Zoomable/scrollable infinite grid with optional grid lines
- Saving and loading of sheets
- Cell selection and copy/paste
- Benchmark step speed (as fast as possible, several steps per frame)
- Option to limit grid size (with the option to wrap cells to the other side)
- More automata rulesets
- Support for more cell states
- Support for different grid types (hexagonal?)

### Requirements
- pyglet
- PyOpenGL
- pyimgui

### Recommendations
- Install numpy to prevent PyOpenGL warnings
- Run under [PyPy](http://https://www.pypy.org/ "PyPy") to increase performance
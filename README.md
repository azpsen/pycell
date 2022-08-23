# pycell
## Cellular automata simulation written in Python
![image](https://user-images.githubusercontent.com/58403923/186240347-9ec4c31e-f01d-4fd1-9df9-ca46d13753fb.png)
### Features
- Basic rectangular grid
- Cells represented through a sparse matrix
- Ability to run simulation at different speeds, view statistics, and configure the display
- Support for multiple automata rulesets

### Planned Features (in order of priority)
- Improved zoomable/scrollable infinite grid with optional grid lines
- Move grid calculations to a C module on a separate thread
- Saving and loading of sheets
- Cell selection and copy/paste
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

# pycell
## cellular automata simulation written in Python
![image](https://user-images.githubusercontent.com/58403923/186241217-2acf3c8e-6882-4047-bec3-86579b8963d8.png)
### features
- basic rectangular grid
- cells represented through a sparse matrix
- ability to run simulation at different speeds, view statistics, and configure the display
- support for multiple automata rulesets

### planned features (in order of priority)
- improved zoomable/scrollable infinite grid with optional grid lines
- move grid calculations to a C module on a separate thread
- saving and loading of sheets
- cell selection and copy/paste
- option to limit grid size (with the option to wrap cells to the other side)
- more automata rulesets
- support for more cell states
- support for different grid types (hexagonal?)

### requirements
- pyglet
- PyOpenGL
- pyimgui

### recommendations
- install numpy to prevent PyOpenGL warnings
- run under [PyPy](http://https://www.pypy.org/ "PyPy") to increase performance

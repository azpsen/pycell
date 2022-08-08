import pyglet
from pyglet import shapes


class Grid:
    def __init__(self, config, w_x, w_y):
        self.w_x, self.w_y = w_x, w_y
        self.config = config

        self.cells_updated = False

        self.cell_count = 0

        self.batch = pyglet.graphics.Batch()
        self.cells = {}
        self.cell_shapes = {}
        self.draw_cells()

    def set_cell(self, pos, value):
        """
        Sets status of cell (alive, dead, dying, growing, etc.)
        :param pos: Position of cell to set
        :param value: Integer value of cell status
        :return:
        """
        if value == 0:
            if pos not in self.cells:
                return
            self.cells.pop(pos)
            self.cell_shapes[pos][0].delete()
            self.cell_shapes.pop(pos)
        else:
            self.cells[pos] = value
        self.draw_cells()

    def cell_status(self, pos):
        """
        Gets cell status (alive, dead, dying, growing, etc.)
        :param pos: Position of cell to get status of
        :return: Cell status
        """
        if pos not in self.cells:
            return 0
        return self.cells[pos]

    def cell_neighbors(self, pos):
        """
        Gets number of living neighbors
        :param pos: Position of cells to check neighbors of
        :return: Number of living neighbors
        """
        neighbors = 0
        x_coords = (pos[0] - 1, pos[0], pos[0] + 1)
        y_coords = (pos[1] - 1, pos[1], pos[1] + 1)
        for i in x_coords:
            for j in y_coords:
                if (i, j) in self.cells and self.cell_status((i, j)) == 1:
                    neighbors += 1
        return neighbors

    def clear(self):
        """
        Clears the entire grid
        :return:
        """
        self.cells = {}
        for _, s in self.cell_shapes.items():
            s[0].delete()
        self.cell_shapes = {}
        self.draw_cells()

    def mouse_pos(self, pos):
        """
        Converts global mouse coordinates to grid-space coordinates
        :param pos: Global mouse position
        :return: Grid-space mouse coordinates
        """
        return int(pos[0] / self.config.cell_size), int(pos[1] / self.config.cell_size)

    def draw_cells(self):
        """
        Refreshes the squares that are drawn to the screen
        :return:
        """
        self.cells_updated = True

        for cell in self.cells:
            if (not cell in self.cell_shapes) or (cell in self.cell_shapes and not self.cell_status(cell) == self.cell_shapes[cell][1]):
                self.cell_shapes[cell] = (shapes.Rectangle(
                    cell[0] * self.config.cell_size,
                    cell[1] * self.config.cell_size,
                    self.config.cell_size,
                    self.config.cell_size,
                    color=self.config.cell_color_on,# if self.cell_status(cell) == 1 else self.config.cell_color_off,
                    batch=self.batch
                ), self.cell_status(cell))

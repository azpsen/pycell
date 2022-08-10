import pyglet
from pyglet import shapes

from camera import Camera


class Grid:
    def __init__(self, config, window):
        self.w_x, self.w_y = window.width, window.height
        self.config = config

        self.cells_updated = False

        self.cell_count = 0

        self.cam_group = Camera(window)
        self.cam_offset = (0, 0)

        self.cell_batch = pyglet.graphics.Batch()
        self.cells = {}
        self.cell_shapes = {}
        self.draw_cells()

        self.lines_x, self.lines_y = [], []
        self.line_batch = pyglet.graphics.Batch()
        self.draw_lines()

        self.mouse_pos = (0, 0)

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

    def set_zoom(self, zoom):
        """
        Set the camera zoom level
        :param zoom: Level to set the camera zoom to
        """
        if zoom > self.config.min_zoom:
            zoom = self.config.min_zoom
        if zoom < self.config.max_zoom:
            zoom = self.config.max_zoom
        self.cam_group.zoom = zoom
        # self.draw_lines()

    def inc_zoom(self, amount):
        """
        Increment the camera zoom level
        :param amount: Amount to increment the zoom by
        :return:
        """
        self.set_zoom(self.cam_group.zoom * amount)

    def set_offset(self, offset):
        """
        Set the camera offset amount
        :param offset: New camera offset
        :return:
        """

        # Handle grid offset
        # self.draw_lines()
        # for line in self.lines_x:
        #     line.

        # Handle cell offset
        self.cam_group.set_offset(offset)
        # self.cam_group.set_state()

    def pan_offset(self, amount):
        """
        Increment the camera offset by specified pan amount
        :param amount: Amount to increment camera offset by
        :return:
        """
        self.set_offset((self.cam_group.offset[0] * self.config.mouse_sensitivity + amount[0],
                         self.cam_group.offset[1] * self.config.mouse_sensitivity + amount[1]))

    def screen_to_cell(self, pos):
        """
        Converts screen coordinates to the cell at that point in grid-space
        :param pos: Screen coordinates to convert
        :return: Grid-space cell coordinates
        """
        return (int((pos[0] - self.cam_group.offset[0]) / self.config.cell_size / self.cam_group.zoom),
                int((pos[1] - self.cam_group.offset[1]) / self.config.cell_size / self.cam_group.zoom))

    def screen_to_grid(self, pos):
        """
        Converts screen coordinates to pixel-perfect grid-space coordinates (useful for zoom offset)
        :param pos: Screen coordinates to convert
        :return: Grid-space pixel-perfect coordinates
        """
        return (int((pos[0] - self.cam_group.offset[0]) / self.cam_group.zoom),
                int((pos[1] - self.cam_group.offset[1]) / self.cam_group.zoom))

    def update(self, mouse_pos):
        self.mouse_pos = mouse_pos

    def draw_cells(self):
        """
        Refreshes the squares that are drawn to the screen
        :return:
        """
        self.cells_updated = True

        for cell in self.cells:
            if (cell not in self.cell_shapes) or (
                    cell in self.cell_shapes and not self.cell_status(cell) == self.cell_shapes[cell][1]):
                self.cell_shapes[cell] = (shapes.Rectangle(
                    cell[0] * self.config.cell_size,
                    cell[1] * self.config.cell_size,
                    self.config.cell_size,
                    self.config.cell_size,
                    color=self.config.cell_color_on,  # if self.cell_status(cell) == 1 else self.config.cell_color_off,
                    batch=self.cell_batch, group=self.cam_group
                ), self.cell_status(cell))

    # def update_line_offset(self):
    #     for l_x in self.lines_x:
    #         l_x.x = l_x.x + self.cam_group.offset[0]
    #
    #     for l_y in self.lines_y:
    #         l_y.y = l_y.y + self.cam_group.offset[1]

    def draw_lines(self):
        for x in range(0, self.w_x, self.config.cell_size):
            # if x not in self.lines_x.keys():
            self.lines_x.append(shapes.Line(
                x, 0, x, self.w_y, width=self.config.grid_width,
                color=self.config.grid_color, batch=self.line_batch#, group=self.cam_group
            ))

        for y in range(0, self.w_y, self.config.cell_size):
            # if y not in self.lines_y.keys():
            self.lines_y.append(shapes.Line(
                0, y, self.w_x, y, width=self.config.grid_width,
                color=self.config.grid_color, batch=self.line_batch#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        , group=self.cam_group
            ))

from .ruleset import Ruleset


class ConwayLife(Ruleset):
    name = "Conway's Game of Life"

    @classmethod
    def step(cls, grid):
        req = cls.required_neighbors(grid)
        live, dead = [], []
        for i in req:
            n = grid.cell_neighbors(i)
            if i not in grid.cells and n == 3:
                live.append(i)
            elif i in grid.cells and (n < 3 or n > 4):
                dead.append(i)
        for d in dead:
            if d in grid.cells.keys():
                grid.cells.pop(d)
                grid.cell_shapes[d][0].delete()
                grid.cell_shapes.pop(d)
        for l in live:
            grid.cells[l] = 1
        return grid

    @classmethod
    def required_neighbors(cls, grid):
        cells = []
        for x, y in grid.cells.keys():
            x_coords = (x-1, x, x+1)
            y_coords = (y-1, y, y+1)
            for x_coord in x_coords:
                for y_coord in y_coords:
                    if (x_coord, y_coord) not in cells:
                        cells.append((x_coord, y_coord))
        return cells

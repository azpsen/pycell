

class Ruleset:
    name = "Base Ruleset (nonfunctional)"

    @classmethod
    def step(cls, grid):
        """
        Performs the next step in the simulation
        :param grid: Grid of cells to perform the step on
        :return: Altered grid
        """
        pass

    @classmethod
    def required_neighbors(cls, grid):
        """
        Finds the empty neighbors that should be checked before the next step
        :param grid: Grid to check
        :return: List of empty cell coordinates that should be checked
        """
        pass
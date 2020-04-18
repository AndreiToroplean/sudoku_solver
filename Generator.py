import random
import copy

from Solver_01 import Solver
from Grid import Grid
from core import Verbosity

# random.seed(0)


class Generator:
    def __init__(self, category=3, verbosity=Verbosity.none):
        self.grid = Grid(category=category)
        self.verbosity = verbosity

    def generate(self):
        solver = Solver(self.grid)
        self.grid = solver.solve()[0]
        indices = list(range(self.grid.numbers_len))
        random.shuffle(indices)
        for index in indices:
            new_grid = copy.deepcopy(self.grid)
            new_grid.del_nb(index)
            solver = Solver(new_grid)
            if len(solver.solve(2)) > 1:
                if self.verbosity >= Verbosity.all:
                    print(f"2 solutions found after deleting number at {self.grid.to_index2(index)}.")
                    self.grid.draw()

                continue
            self.grid = new_grid
            if self.verbosity >= Verbosity.some:
                print(f"New grid with {self.grid.unknowns_len} unknowns:")
                self.grid.draw()
        return self.grid

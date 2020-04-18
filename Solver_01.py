import copy
import random

from math import isclose

from core import Verbosity

# random.seed(0)


class Solver:
    def __init__(self, grid, base_solver=None, level=0, verbosity=Verbosity.none):
        self.grid = copy.deepcopy(grid)
        self.level = level
        self.verbosity = verbosity

        if base_solver is None:
            self.completion = 0.0
            self.possibilities_grid = []
            for index in range(self.grid.numbers_len):
                if self.grid.is_completed(index):
                    self.completion += 1
                    continue
                accepted_numbers_copy = self.grid.accepted_numbers.copy()
                random.shuffle(accepted_numbers_copy)
                self.possibilities_grid.append((index, accepted_numbers_copy))
            random.shuffle(self.possibilities_grid)
        else:
            self.completion = base_solver.completion
            self.possibilities_grid = base_solver.possibilities_grid

        self.initial_completion = self.completion

    @classmethod
    def from_base_solver(cls, base_solver):
        copied_solver = copy.deepcopy(base_solver)
        copied_grid = copied_solver.grid
        return cls(copied_grid, copied_solver, copied_solver.level + 1, copied_solver.verbosity)

    def guess(self, index, guess, possibilities_len):
        self.possibilities_grid = [x for x in self.possibilities_grid if x[0] != index]
        self.grid.set_nb(index, guess)
        self.update_completion(1, possibilities_len)

        if self.verbosity >= Verbosity.some:
            print(f"Guessing {guess} at {self.grid.to_index2(index)}. Level {self.level}.")
            self.grid.draw()

    def update_completion(self, possibilities_len_2, possibilities_len_1):
        row_len = self.grid.row_len
        self.completion += (row_len/possibilities_len_2 - row_len/possibilities_len_1) / (row_len - 1)

    def solve(self, max_solutions=1):
        solved_grids = []
        do_guess = False

        while self.completion < self.grid.numbers_len and not isclose(self.completion, self.grid.numbers_len):
            previous_completion = self.completion

            for iter_index, possibilities_tuple in enumerate(self.possibilities_grid):
                index, possibilities = possibilities_tuple
                checked_possibilities = []
                if do_guess:
                    do_guess = False

                    guess = possibilities[0]
                    new_solver = Solver.from_base_solver(self)
                    new_solver.guess(index, guess, len(possibilities))
                    new_solved_grids = new_solver.solve(max_solutions - len(solved_grids))
                    if len(new_solved_grids) > 0:
                        solved_grids += new_solved_grids

                    if len(solved_grids) == max_solutions:
                        if self.verbosity >= Verbosity.some:
                            print('Hit the requested max number of solutions.')
                        return solved_grids

                    checked_possibilities = possibilities[1:]

                else:
                    for proposition in possibilities:
                        if self.grid.is_valid(index, proposition):
                            checked_possibilities.append(proposition)

                if len(checked_possibilities) == 0:
                    if self.verbosity >= Verbosity.some:
                        print(f"Impossible grid. No solutions at {self.grid.to_index2(index)}. "
                              f"Back to level {self.level - 1}.")
                        self.grid.draw()
                    return solved_grids

                self.update_completion(len(checked_possibilities), len(possibilities))

                if len(checked_possibilities) == 1:
                    self.grid.set_nb(index, checked_possibilities[0])
                    self.possibilities_grid[iter_index] = None
                    continue

                self.possibilities_grid[iter_index] = (index, checked_possibilities)

            self.possibilities_grid = [x for x in self.possibilities_grid if x is not None]

            self.possibilities_grid.sort(key=lambda x: len(x[1]))

            if previous_completion == self.completion:
                do_guess = True

            if self.verbosity >= Verbosity.all:
                print(f"Completion: {self.completion * 100 / self.grid.numbers_len:.1f}%, level: {self.level}.")
                self.grid.draw()

        solved_grids.append(self.grid)
        if self.verbosity >= Verbosity.some:
            print("Found solution:")
            self.grid.draw()

        return solved_grids

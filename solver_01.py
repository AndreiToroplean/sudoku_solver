import copy

from enum import Enum


class Solver:
    def __init__(self, grid, base_solver=None, guessing_level=0, logging_verbosity=0):
        self.grid = grid
        self.numbers_len = len(self.grid.numbers)
        self.guessing_level = guessing_level
        self.logging_verbosity = logging_verbosity

        if base_solver is None:
            self.completion = 0.0
            self.possibilities_grid = []
            for index in range(self.numbers_len):
                if self.grid.is_completed(index):
                    self.completion += 1
                    continue
                self.possibilities_grid.append((index, self.grid.accepted_numbers.copy()))
        else:
            self.completion = base_solver.completion
            self.possibilities_grid = base_solver.possibilities_grid

        self.initial_completion = self.completion

    class LoggingVerbosity:
        none = 0
        some = 2
        all = 3

    @classmethod
    def from_base_solver(cls, base_solver):
        copied_solver = copy.deepcopy(base_solver)
        copied_grid = copied_solver.grid
        return cls(copied_grid, copied_solver, copied_solver.guessing_level+1, copied_solver.logging_verbosity)

    def guess(self, index, guess, possibilities_len):
        self.possibilities_grid = [x for x in self.possibilities_grid if x[0] != index]
        self.grid.set_nb(index, guess)
        self.update_completion(1, possibilities_len)

        if self.logging_verbosity >= self.LoggingVerbosity.some:
            print(f"Guessing {guess} at {self.grid.to_index2(index)}. Level {self.guessing_level}.")
            self.grid.draw()

    def update_completion(self, possibilities_len_2, possibilities_len_1):
        row_len = self.grid.row_len
        self.completion += (row_len/possibilities_len_2 - row_len/possibilities_len_1) / (row_len - 1)

    def solve(self, max_solutions=1):
        solved_grids = []
        do_guess = False

        while self.completion < self.numbers_len:
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
                        if self.logging_verbosity >= self.LoggingVerbosity.some:
                            print('Hit the requested max number of solutions.')
                        return solved_grids

                    checked_possibilities = possibilities[1:]

                else:
                    for proposition in possibilities:
                        if self.grid.is_valid(index, proposition):
                            checked_possibilities.append(proposition)

                if len(checked_possibilities) == 0:
                    if self.logging_verbosity >= self.LoggingVerbosity.some:
                        print(f"Impossible grid. No solutions at {self.grid.to_index2(index)}. "
                              f"Back to level {self.guessing_level-1}.")
                        self.grid.draw()
                    return solved_grids

                self.update_completion(len(checked_possibilities), len(possibilities))

                if len(checked_possibilities) == 1:
                    self.grid.set_nb(index, checked_possibilities[0])
                    self.possibilities_grid[iter_index] = None
                    continue

                self.possibilities_grid[iter_index] = (index, checked_possibilities)

            self.possibilities_grid = [x for x in self.possibilities_grid if x is not None]

            if self.logging_verbosity >= self.LoggingVerbosity.all:
                print(f"Completion: {self.completion * 100 / self.numbers_len:.1f}%, level: {self.guessing_level}.")
                self.grid.draw()

            if previous_completion == self.completion:
                self.possibilities_grid.sort(key=lambda x: len(x[1]))
                do_guess = True

        solved_grids.append(self.grid)
        if self.logging_verbosity >= self.LoggingVerbosity.some:
            print("Found solution:")
            self.grid.draw()

        return solved_grids

import copy

from enum import Enum


class Solver:
    def __init__(self, grid, base_solver=None, guessing_level=0):
        self.grid = grid
        self.numbers_len = len(self.grid.numbers)
        self.guessing_level = guessing_level

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

    @classmethod
    def from_base_solver(cls, base_solver):
        copied_solver = copy.deepcopy(base_solver)
        copied_grid = copied_solver.grid
        return cls(copied_grid, copied_solver, copied_solver.guessing_level+1)

    def guess(self, index, guess, possibilities_len):
        self.possibilities_grid = [x for x in self.possibilities_grid if x[0] != index]
        self.grid.set_nb(index, guess)
        self.completion += self._calc_completion(self.grid.row_len, possibilities_len, 1)
        print(f"Guessing {guess} at {self.grid.to_index2(index)}. Level {self.guessing_level}.")
        self.grid.draw()

    def solve(self, max_solutions=1):
        solved_grids = []

        while self.completion < self.numbers_len:
            previous_completion = self.completion
            for iter_index, possibilities_tuple in enumerate(self.possibilities_grid):
                index, possibilities = possibilities_tuple
                checked_possibilities = []
                for proposition in possibilities:
                    if self.grid.is_valid(index, proposition):
                        checked_possibilities.append(proposition)

                if len(checked_possibilities) == 0:
                    print("Impossible grid:")
                    self.grid.draw()
                    return []

                self.completion += self._calc_completion(
                    self.grid.row_len,
                    len(checked_possibilities),
                    len(possibilities)
                    )

                if len(checked_possibilities) == 1:
                    self.grid.set_nb(index, checked_possibilities[0])
                    self.possibilities_grid[iter_index] = None
                    continue

                self.possibilities_grid[iter_index] = (index, checked_possibilities)

            self.possibilities_grid = [x for x in self.possibilities_grid if x is not None]

            if previous_completion == self.completion:
                self.possibilities_grid.sort(key=lambda x: len(x[1]))
                for iter_index, possibilities_tuple in enumerate(self.possibilities_grid):
                    index, possibilities = possibilities_tuple
                    checked_possibilities = []
                    for guess in possibilities:
                        new_solver = Solver.from_base_solver(self)
                        new_solver.guess(index, guess, len(possibilities))
                        new_solved_grids = new_solver.solve(max_solutions - len(solved_grids))
                        if len(new_solved_grids) > 0:
                            checked_possibilities.append(guess)
                            solved_grids.append(new_solved_grids)

                    if len(solved_grids) == max_solutions:
                        return solved_grids

                    if len(checked_possibilities) == 0:
                        print("Impossible grid:")
                        self.grid.draw()
                        return []

                    self.completion += self._calc_completion(
                        self.grid.row_len,
                        len(checked_possibilities),
                        len(possibilities)
                        )

                    if len(checked_possibilities) == 1:
                        self.grid.set_nb(index, checked_possibilities[0])
                        self.possibilities_grid[iter_index] = None
                        break

                    self.possibilities_grid[iter_index] = (index, checked_possibilities)

                self.possibilities_grid = [x for x in self.possibilities_grid if x is not None]
            print(f"Completion: {self.completion * 100 / self.numbers_len:.1f}%, level: {self.guessing_level}.")

            if not self.possibilities_grid:
                self.grid.draw()
                break

        solved_grids.append(self.grid)
        print(f"Took it from {self.initial_completion * 100 / self.numbers_len:.1f}% "
              f"to {self.completion * 100 / self.numbers_len:.1f}% completed.")

        return solved_grids

    @staticmethod
    def _calc_completion(row_len, possibilities_len_2, possibilities_len_1):
        return (row_len/possibilities_len_2 - row_len/possibilities_len_1) / (row_len - 1)

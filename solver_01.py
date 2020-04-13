class Solver:
    def __init__(self, grid, base_solver=None):
        self.grid = grid
        self.numbers_len = len(self.grid.numbers)

        if base_solver is None:
            self.completion = 0.0
            self.possibilities_grid = []
            for index in range(self.numbers_len):
                if self.grid.is_completed(index):
                    self.possibilities_grid.append(None)
                    self.completion += 1
                    continue
                self.possibilities_grid.append(self.grid.accepted_numbers.copy())
        else:
            self.completion = base_solver.completion
            self.possibilities_grid = base_solver.possibilities_grid

        self.initial_completion = self.completion

    def solve(self):
        while self.completion < self.numbers_len:
            previous_completion = self.completion
            for index, possibilities in enumerate(self.possibilities_grid):
                if possibilities is None:
                    continue

                checked_possibilities = []
                for proposition in possibilities:
                    if self.grid.is_valid(index, proposition):
                        checked_possibilities.append(proposition)

                self.completion += (self._calc_completion(len(checked_possibilities), self.grid.row_len)
                               - self._calc_completion(len(possibilities), self.grid.row_len))

                if len(checked_possibilities) == 1:
                    self.grid.set_nb(index, checked_possibilities[0])
                    self.possibilities_grid[index] = None
                    continue

                self.possibilities_grid[index] = checked_possibilities

            if previous_completion == self.completion:
                break

        print(
            f"Took it from {self.initial_completion * 100 / self.numbers_len:.1f}% to {self.completion * 100 / self.numbers_len:.1f}% completed.")

    @staticmethod
    def _calc_completion(possibilities_len, row_len):
        return (row_len - possibilities_len) / ((row_len - 1) * possibilities_len)

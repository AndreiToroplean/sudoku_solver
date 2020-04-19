import random

seed = 0
random.seed(seed)


# todo: A single filled grid, with a second corresponding confidence grid... With every iteration, updating the numbers
#   in an order depending on the confidence. Not sure if it would work...
class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.possibilities_grid = []
        for index in range(self.grid.numbers_len):
            if self.grid.is_completed(index):
                continue
            accepted_numbers_copy = self.grid.accepted_numbers.copy()
            random.shuffle(accepted_numbers_copy)
            self.possibilities_grid.append((index, accepted_numbers_copy))
        random.shuffle(self.possibilities_grid)

    def solve(self):
        while True:
            for iter_index, possibilities_tuple in self.possibilities_grid:
                index, possibilities = possibilities_tuple

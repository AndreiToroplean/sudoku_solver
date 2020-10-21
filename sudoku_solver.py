import copy
import random
from math import isclose


class Verbosity:
    none = 0
    some = 2
    all = 3


class Grid:
    unknown_nb = '.'

    def __init__(self, numbers="", category=3):
        assert category > 1, "category should be at least 2."
        self.category = category
        self.row_len = self.category ** 2
        self.numbers_len = self.row_len ** 2
        self.accepted_numbers = [str(x) for x in range(1, self.row_len + 1)]

        self.numbers = [self._parse_nb(x) for x in numbers]

        numbers_len = len(self.numbers)
        if numbers_len < self.numbers_len:
            self.numbers += [self.unknown_nb for _ in range(self.numbers_len - numbers_len)]

    def _parse_nb(self, nb):
        try:
            nb_str = str(nb)
        except ValueError:
            pass
        else:
            if nb_str in self.accepted_numbers:
                return nb_str
        return self.unknown_nb

    def row(self, row_index):
        return self.numbers[
        self.row_len * row_index:
        self.row_len * (row_index + 1)
        ]

    def col(self, col_index):
        return [row[col_index] for row in self.rows]

    def cell(self, cell_index):
        rtn = []
        for row in self.rows[
        self.category * cell_index[0]:
        self.category * (cell_index[0] + 1)
        ]:
            rtn += row[
            self.category * cell_index[1]:
            self.category * (cell_index[1] + 1)
            ]
        return rtn

    @property
    def rows(self):
        rtn = []
        for row_index in range(self.row_len):
            rtn.append(self.row(row_index))
        return rtn

    @property
    def cols(self):
        rtn = []
        for col_index in range(self.row_len):
            rtn.append(self.col(col_index))
        return rtn

    @property
    def cells(self):
        rtn = []
        for cell_row_index in range(self.category):
            for cell_col_index in range(self.category):
                rtn.append(self.cell((cell_row_index, cell_col_index)))
        return rtn

    def to_index1(self, index):
        try:
            return index[0] * self.row_len + index[1]
        except TypeError:
            return index
        except IndexError:
            return index[0]

    def to_index2(self, index):
        try:
            row_index = int(index / self.row_len)
        except TypeError:
            return index
        else:
            col_index = index - row_index * self.row_len
            return row_index, col_index

    def to_cell_index(self, index):
        index = self.to_index2(index)
        return int(index[0] / self.category), int(index[1] / self.category)

    def get_nb(self, index):
        return self.numbers[self.to_index1(index)]

    def set_nb(self, index, value):
        self.numbers[self.to_index1(index)] = value

    def del_nb(self, index):
        self.numbers[self.to_index1(index)] = self.unknown_nb

    def row_from_index(self, index):
        row_index, _ = self.to_index2(index)
        return self.row(row_index)

    def col_from_index(self, index):
        _, col_index = self.to_index2(index)
        return self.col(col_index)

    def cell_from_index(self, index):
        cell_index = self.to_cell_index(index)
        return self.cell(cell_index)

    def is_completed(self, index):
        if self.get_nb(index) == self.unknown_nb:
            return False
        return True

    previous_index = None
    previous_used_numbers = set()

    def is_valid(self, index, proposition):
        if index == self.previous_index:
            return proposition not in self.previous_used_numbers
        self.previous_index = index

        used_numbers = set(self.row_from_index(index)).union(self.col_from_index(index), self.cell_from_index(index))
        self.previous_used_numbers = used_numbers
        return proposition not in used_numbers

    def __str__(self):
        h_pad = 2
        v_pad = 0
        h_f_seg = '-' * ((h_pad + 1) * self.category + h_pad)
        h_f_line = f"+{h_f_seg}" * self.category + "+\n"
        h_e_seg = ' ' * ((h_pad + 1) * self.category + h_pad)
        h_e_line = f"|{h_e_seg}" * self.category + "|\n"

        rtn = ""
        for row_index, row in enumerate(self.rows):
            if row_index % self.category == 0:
                rtn += h_f_line + h_e_line * v_pad
            rtn += '|'
            for number_index, number in enumerate(row):
                if number_index % self.category == 0 and number_index != 0:
                    rtn += ' ' * h_pad + '|'
                rtn += ' ' * (h_pad - len(number) + 1) + number
            rtn += ' ' * h_pad + "|\n" + h_e_line * v_pad
        rtn += h_f_line

        return rtn

    def __repr__(self):
        return f"Grid(\"{''.join(self.numbers)}\")"

    @property
    def numbers_as_string(self):
        return ''.join(self.numbers)

    @property
    def unknowns_len(self):
        return self.numbers.count(self.unknown_nb)

    def draw(self):
        print(self)


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
        self.completion += (row_len / possibilities_len_2 - row_len / possibilities_len_1) / (row_len - 1)

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


class ParsingError(Exception):
    pass


class SolutionError(Exception):
    pass


def parse_from_codewars(puzzle):
    if len(puzzle) != 9:
        raise ParsingError

    grid_str = ""
    for row in puzzle:
        if len(row) != 9:
            raise ParsingError

        for number in row:
            if not isinstance(number, int):
                raise ParsingError
            if number == 0:
                grid_str += "."
                continue

            if number not in range(1, 10):
                raise ParsingError

            grid_str += str(number)

    return grid_str


def parse_for_codewars(solution):
    solution_array = []
    for row_i in range(9):
        solution_array.append([])
        for nb_i in range(9):
            solution_array[-1].append(int(solution[row_i * 9 + nb_i]))

    return solution_array


def random_grid_str():
    grid_str = ""
    for _ in range(81):
        grid_str += str(random.randint(1, 9))

        if random.random() < 0.5:
            grid_str = grid_str[:-1] + "."

    return grid_str


def sudoku_solver(puzzle):
    grid_str = parse_from_codewars(puzzle)
    grid = Grid(grid_str)
    solver = Solver(grid)
    solutions = solver.solve(max_solutions=2)
    n_unique_solutions = len(set(solution.numbers_as_string for solution in solutions))
    if n_unique_solutions != 1:
        raise SolutionError

    return parse_for_codewars(solutions[0].numbers_as_string)


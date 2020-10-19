from grid import Grid
from generator import Generator
from solver import Solver
from core import Verbosity


class ParsingError(Exception):
	pass


class SolutionError(Exception):
	pass


def _parse_from_codewars(puzzle):
	if len(puzzle) != 9:
		raise ParsingError

	grid_str = ""
	for row in puzzle:
		if len(row) != 9:
			raise ParsingError

		for number in row:
			if number == 0:
				grid_str += "."
				continue

			if number not in range(1, 9):
				raise ParsingError

			grid_str += str(number)

	return grid_str


def _parse_for_codewars(solution):
	solution_array = []
	for row_i in range(9):
		solution_array.append([])
		for nb_i in range(9):
			solution_array.append(int(solution[row_i*nb_i]))

	return solution_array


def sudoku_solver(puzzle):
	grid_str = _parse_from_codewars(puzzle)
	grid = Grid(grid_str)
	solver = Solver(grid)
	solutions = solver.solve(max_solutions=2)
	n_unique_solutions = len(set(solution.numbers_as_string for solution in solutions))
	if n_unique_solutions != 1:
		raise SolutionError

	return _parse_for_codewars(solutions[0])

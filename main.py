from Grid import Grid
from solver_01 import Solver

if __name__ == "__main__":
	# grid = Grid("3.59..8...8.3....7.9...56........3.......2.7.2......5.9...7...6.7.4........8.3..4")
	# grid = Grid("..59..8...8.3....7.9...56........3.......2.7.2......5.9...7...6.7.4........8.3..4")  # modified manually
	grid = Grid("...9..8...8.3....7.9...56........3.......2.7.2......5.9...7...6.7.4........8.3..4")  # modified manually
	# grid = Grid(".......67....9.2.468..2..3...56.37..42...95..8.3......9.8..........3...9....5.678")
	# grid = Grid("...2.3......4..6..36.....7.68.7.......23.1..7..5.2..4.2...8....7..6...3...81.4...")
	# grid = Grid("632...4.5....5.........8......1.6.2..149.....5.........2...3....68.1....1.36842..")
	# grid = Grid(".72..6.....5.28.7........46.8......924.....5.1.9.4...8....9.6.........846...8...1")
	# grid = Grid("1" + "."*80) # modified manually

	print("Solving:")
	grid.draw()

	solver = Solver(grid)
	solutions = solver.solve(1)
	print()

	print(f"Solutions (found {len(solutions)}):")
	for solution in solutions:
		solution.draw()

	unique_solutions = set(x.get_numbers_as_string() for x in solutions)
	if len(unique_solutions) == len(solutions) > 1:
		print(f"All {len(solutions)} solutions are unique.")

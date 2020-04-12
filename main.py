import time

from Grid import Grid
from solver_01 import solver

if __name__ == "__main__":
	# grid = Grid("3.59..8...8.3....7.9...56........3.......2.7.2......5.9...7...6.7.4........8.3..4")
	# grid = Grid("632...4.5....5.........8......1.6.2..149.....5.........2...3....68.1....1.36842..")
	grid = Grid(".72..6.....5.28.7........46.8......924.....5.1.9.4...8....9.6.........846...8...1")

	print("Original grid:")
	grid.draw()

	grid.solve(solver)

	print("Solution:")
	grid.draw()

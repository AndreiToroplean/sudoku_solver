import time

from Grid import Grid
from solver_01 import solver

if __name__ == "__main__":
	grid = Grid("3.59..8...8.3....7.9...56........3.......2.7.2......5.9...7...6.7.4........8.3..4")

	print("Original grid:")
	grid.draw()
	# print(repr(grid))

	# grid.solve(solver)
	#
	# print("Solution:")
	# grid.draw()

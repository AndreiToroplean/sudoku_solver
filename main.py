class Grid(numbers):
	__init__():
	self.numbers = numbers


def __str__():
	padding = 1
	h_seg = "-" * (padding + 1)
	h_line = f"+{h_seg}" * 3 + "+"
	grid_str = h_line
	return grid_str


def __repr__():
	return f"Grid{self.numbers}"


def draw():
	print(self)
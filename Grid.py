class Grid:

	def __init__(self, numbers):
		self.h_nb_per_cell = 3
		self.v_nb_per_cell = 3
		self.h_cells = 3
		self.v_cells = 3

		self.numbers = "".join(self.parse_nb(x) for x in numbers)

	@staticmethod
	def parse_nb(nb):
		accepted_numbers = "123456789"
		unknown_nb = "."
		try:
			nb_str = str(nb)
			if nb_str in accepted_numbers:
				return nb_str
		except ValueError:
			pass
		return unknown_nb

	def __str__(self):
		h_pad = 2
		v_pad = 0
		h_f_seg = "-" * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_f_line = f"+{h_f_seg}" * self.h_cells + "+\n"
		h_e_seg = " " * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_e_line = f"|{h_e_seg}" * self.h_cells + "|\n"
		grid_str = ""
		for cell_row_index in range(self.v_cells):
			grid_str += h_f_line
			grid_str += h_e_line * v_pad
			for line_index in range(self.v_nb_per_cell):
				for index, number in enumerate(self.numbers[cell_row_index*line_index
					:cell_row_index*line_index+(self.h_nb_per_cell * self.h_cells)]):
					if index % self.h_nb_per_cell == 0:
						grid_str += "|"
						grid_str += " " * h_pad
					grid_str += str(number)
					grid_str += " " * h_pad
				grid_str += "|\n"
				grid_str += h_e_line * v_pad
		grid_str += h_f_line
		return grid_str

	def __repr__(self):
		return f"Grid({repr(self.numbers)})"

	def draw(self):
		print(self)

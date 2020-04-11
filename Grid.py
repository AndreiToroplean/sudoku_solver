class Grid:

	def __init__(self, numbers):
		self.h_nb_per_cell = 3
		self.v_nb_per_cell = 3
		self.h_cells = 3
		self.v_cells = 3

		self.numbers = "".join(self._parse_nb(x) for x in numbers)

	@staticmethod
	def _parse_nb(nb):
		accepted_numbers = "123456789"
		unknown_nb = "."
		try:
			nb_str = str(nb)
			if nb_str in accepted_numbers:
				return nb_str
		except ValueError:
			pass
		return unknown_nb

	@property
	def row_len(self):
		return self.h_nb_per_cell * self.h_cells

	@property
	def rows_len(self):
		return self.v_nb_per_cell * self.v_cells

	@property
	def rows(self):
		for row_index in range(self.rows_len):
			yield self.row(row_index)

	@property
	def cols(self):
		for col_index in range(self.row_len):
			yield self.col(col_index)

	def row(self, index):
		return self.numbers[
			self.row_len * index:
			self.row_len * (index+1)
			]

	def col(self, index):
		return ''.join(row[index] for row in self.rows)

	def __str__(self):
		h_pad = 2
		v_pad = 0
		h_f_seg = "-" * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_f_line = f"+{h_f_seg}" * self.h_cells + "+\n"
		h_e_seg = " " * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_e_line = f"|{h_e_seg}" * self.h_cells + "|\n"

		rtn = ""
		for row_index, row in enumerate(self.rows):
			if row_index % self.v_nb_per_cell == 0:
				rtn += h_f_line + h_e_line * v_pad
			for number_index, number in enumerate(row):
				if number_index % self.h_nb_per_cell == 0:
					rtn += "|" + " " * h_pad
				rtn += str(number) + " " * h_pad
			rtn += "|\n" + h_e_line * v_pad
		rtn += h_f_line

		return rtn

	def __repr__(self):
		return f"Grid({repr(self.numbers)})"

	def draw(self):
		print(self)

	def solve(self, solver):
		solver(self)

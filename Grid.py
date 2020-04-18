class Grid:
	unknown_nb = '.'

	def __init__(self, numbers="", category=3):
		self.category = category
		self.h_nb_per_cell = self.category
		self.v_nb_per_cell = self.category
		self.h_cells = self.category
		self.v_cells = self.category
		self.accepted_numbers = list("1234567890abcdef")[:self.category ** 2]
		# todo: deal with the situation where category > 4.

		self.numbers = [self._parse_nb(x) for x in numbers]

		numbers_len = len(self.numbers)
		expected_numbers_len = self.category ** 4
		if numbers_len < expected_numbers_len:
			self.numbers += [self.unknown_nb for _ in range(expected_numbers_len - numbers_len)]
			print("Autocompleted incomplete grid.")

	def _parse_nb(self, nb):
		try:
			nb_str = str(nb)
		except ValueError:
			pass
		else:
			if nb_str in self.accepted_numbers:
				return nb_str
		return self.unknown_nb

	@property
	def row_len(self):
		return self.h_nb_per_cell * self.h_cells

	@property
	def rows_len(self):
		return self.v_nb_per_cell * self.v_cells

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
				self.v_nb_per_cell * cell_index[0]:
				self.v_nb_per_cell * (cell_index[0]+1)
				]:
			rtn += row[
					self.h_nb_per_cell * cell_index[1]:
					self.h_nb_per_cell * (cell_index[1]+1)
					]
		return rtn

	@property
	def rows(self):
		rtn = []
		for row_index in range(self.rows_len):
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
		for cell_row_index in range(self.h_cells):
			for cell_col_index in range(self.v_cells):
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
			row_index = int(index/self.row_len)
		except TypeError:
			return index
		else:
			col_index = index - row_index * self.row_len
			return row_index, col_index

	def to_cell_index(self, index):
		index = self.to_index2(index)
		return int(index[0]/self.v_cells), int(index[1]/self.h_cells)

	def get_nb(self, index):
		return self.numbers[self.to_index1(index)]

	def set_nb(self, index, value):
		self.numbers[self.to_index1(index)] = value

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

	def is_valid(self, index, proposition):
		# print("proposition", proposition)
		if self.is_completed(index):
			return False
		# print("row", self.row_from_index(index))
		if proposition in self.row_from_index(index):
			return False
		# print("col", self.col_from_index(index))
		if proposition in self.col_from_index(index):
			return False
		# print("cell", self.cell_from_index(index))
		if proposition in self.cell_from_index(index):
			return False

		# print("ok")
		return True

	def __str__(self):
		h_pad = 2
		v_pad = 0
		h_f_seg = '-' * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_f_line = f"+{h_f_seg}" * self.h_cells + "+\n"
		h_e_seg = ' ' * ((h_pad + 1) * self.h_nb_per_cell + h_pad)
		h_e_line = f"|{h_e_seg}" * self.h_cells + "|\n"

		rtn = ""
		for row_index, row in enumerate(self.rows):
			if row_index % self.v_nb_per_cell == 0:
				rtn += h_f_line + h_e_line * v_pad
			for number_index, number in enumerate(row):
				if number_index % self.h_nb_per_cell == 0:
					rtn += '|' + ' ' * h_pad
				rtn += number + ' ' * h_pad
			rtn += "|\n" + h_e_line * v_pad
		rtn += h_f_line

		return rtn

	def __repr__(self):
		return f"Grid({repr(self.numbers)})"

	def get_numbers_as_string(self):
		return ''.join(self.numbers)

	def draw(self):
		print(self)

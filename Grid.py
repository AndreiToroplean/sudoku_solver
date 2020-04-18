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
			row_index = int(index/self.row_len)
		except TypeError:
			return index
		else:
			col_index = index - row_index * self.row_len
			return row_index, col_index

	def to_cell_index(self, index):
		index = self.to_index2(index)
		return int(index[0]/self.category), int(index[1] / self.category)

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
		return f"Grid({repr(self.numbers)})"

	def get_numbers_as_string(self):
		return ''.join(self.numbers)

	def draw(self):
		print(self)

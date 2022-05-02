import Signal

class Gate:
	"""Class Gate depicts a basic logic gate with 1 or 2 inputs and 1 output """
	def __init__(self, name, gate_type):
		"""Initialises the Gate object.
		Inputs:
		name : str
			name of the gate
		gate_type : str
			logic gate type - ex. "INV", "OR", "AND", etc.

		Exceptions:
		ValueError
			If the given gate type didn't match one of the handled types
		"""
		self._input1 = None # value of input1
		self._input2 = None  # value of input2
		self._output = None # value of output
		if gate_type not in ("INV", "OR", "AND", "XOR", "NOR", "NAND", "XNOR", "BUFFER"):
			raise ValueError(f"{gate_type} is not a valid Gate type")
		self._gate_type = gate_type # Gate name
		self._name = name

	def connect_inputs(self, input1, input2=None):
		"""Connects the inputs to the gate
		Inputs:
		input1 : int
			Logic 0 or 1 first input of the gate (only input for INV and BUFFER types)
		input2 : int
			Logic 0 or 1 second input of the gate (default is None for the INV and BUFFER types)

		Exceptions:
		ValueError
			If input2 is given and gate type is INV or BUFFER.
			If one of the inputs is not legal - not 0 or 1 (second input can be None for INV and BUFFER types)
		"""
		if input2 is None and self._gate_type not in ("INV", "BUFFER"):
			raise ValueError(f"{self._gate_type} only has one input")
		if input1 not in (0, 1) or input2 not in (None, 0, 1):
			raise ValueError(f"At least one of the inputs is invalid")
		self._input1, self._input2 = input1, input2

	def update_output(self):
		"""Updates the output of the gate as a logic function of the inputs depicted by the gate type
		Exceptions:
		ValueError
		If one of the inputs (in case of INV and BUFFER input 1) is not connected
		"""
		if self._input1 is None or (self._input2 is None and self._gate_type not in ("INV", "BUFFER")):
			raise ValueError("Inputs are not connected")
		match self._gate_type:
			case "INV":
				self.NOT()
			case "OR":
				self.OR()
			case "AND":
				self.AND()
			case "XOR":
				self.XOR()
			case "NOR":
				self.NOR()
			case "NAND":
				self.NAND()
			case "XNOR":
				self.XNOR()
			case "BUFFER":
				self._output = self._input1

	def NOT(self):
		"""NOT logic function - used on the gate input and the result stored in the gate output"""
		if self._input1 == 0:
			self._output = 1
		elif self._input1 == 1:
			self._output = 0

	def AND(self):
		"""AND logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) == (1, 1):
			self._output = 1
		elif (self._input1, self._input2) in ((0, 0), (0, 1), (1, 0)):
			self._output = 0

	def OR(self):
		"""OR logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) in ((0, 1), (1, 0), (1, 1)):
			self._output = 1
		elif (self._input1, self._input2) == (0, 0):
			self._output = 0

	def XOR(self):
		"""XOR logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) in ((0, 0), (1, 1)):
			self._output = 0
		elif (self._input1, self._input2) in ((0, 1), (1, 0)):
			self._output = 1

	def NAND(self):
		"""NAND logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) == (1, 1):
			self._output = 0
		elif (self._input1, self._input2) in ((0, 0), (0, 1), (1, 0)):
			self._output = 1

	def NOR(self):
		"""NOR logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) in ((0, 1), (1, 0), (1, 1)):
			self._output = 0
		elif (self._input1, self._input2) == (0, 0):
			self._output = 1

	def XNOR(self):
		"""XNOR logic function - used on the gate inputs and the result stored in the gate output"""
		if (self._input1, self._input2) in ((0, 0), (1, 1)):
			self._output = 1
		elif (self._input1, self._input2) in ((0, 1), (1, 0)):
			self._output = 0

	def __hash__(self):
		return hash(id(self))

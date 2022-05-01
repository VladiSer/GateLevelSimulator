import Signal

class Gate:
	"""TODO: class Gate documentation """

	def __init__(self, name, gate_type):
		"""TODO: class Gate __init__ documentation"""
		self._input1 = None # value of input1
		self._input2 = None  # value of input2
		self._output = None # value of output
		if gate_type not in ("INV", "OR", "AND", "XOR", "NOR", "NAND", "XNOR", "BUFFER"):
			raise ValueError(f"{gate_type} is not a valid Gate type")
		self._gate_type = gate_type # Gate name
		self._name = name

	def connect_inputs(self, input1, input2=None):
		"""TODO: class Gate connect_inputs documentation"""
		if input2 is None and self._gate_type not in ("INV", "BUFFER"):
			raise ValueError(f"{self._gate_type} only has one input")
		if input1 not in (0, 1) or input2 not in (None, 0, 1):
			raise ValueError(f"At least one of the inputs is invalid")
		self._input1, self._input2 = input1, input2


	def update_output(self):
		"""TODO: class Gate update_output documentation"""
		if self._input1 is None:
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
		if self._input1 == 0:
			self._output = 1
		elif self._input1 == 1:
			self._output = 0

	def AND(self):
		if (self._input1, self._input2) == (1, 1):
			self._output = 1
		elif (self._input1, self._input2) in ((0, 0), (0, 1), (1, 0)):
			self._output = 0

	def OR(self):
		if (self._input1, self._input2) in ((0, 1), (1, 0), (1, 1)):
			self._output = 1
		elif (self._input1, self._input2) == (0, 0):
			self._output = 0

	def XOR(self):
		if (self._input1, self._input2) in ((0, 0), (1, 1)):
			self._output = 0
		elif (self._input1, self._input2) in ((0, 1), (1, 0)):
			self._output = 1

	def NAND(self):
		if (self._input1, self._input2) == (1, 1):
			self._output = 0
		elif (self._input1, self._input2) in ((0, 0), (0, 1), (1, 0)):
			self._output = 1

	def NOR(self):
		if (self._input1, self._input2) in ((0, 1), (1, 0), (1, 1)):
			self._output = 0
		elif (self._input1, self._input2) == (0, 0):
			self._output = 1

	def XNOR(self):
		if (self._input1, self._input2) in ((0, 0), (1, 1)):
			self._output = 1
		elif (self._input1, self._input2) in ((0, 1), (1, 0)):
			self._output = 0

	def __hash__(self):
		return hash(id(self))

class Port:
	"""Class Port depicts a port with 1 input and 1 output, connected at the inputs or outputs of a circuit"""
	def __init__(self, name):
		"""Initialises the Port object.
		Inputs:
		name : str
			Name of the port
		"""
		self._name = name

	@property
	def name(self):
		"""Returns the name of the port"""
		return self._name

	def get_output(self, inputs):
		"""Updates the output of the port by taking a list of input vectors, for port - outputs = inputs
		Inputs:
		inputs: list[list[int]] - list of lists of ints
			List of input vectors

		Outputs:
		list[int] - list of ints
			An output vector

		Exceptions:
		ValueError
			If number of input vectors is not 1, as a port has only 1 input
		"""
		if len(inputs) != 1:
			raise ValueError("Invalid number of inputs to the port")
		return inputs[0]

	def __hash__(self):
		return hash(id(self))


class Gate:
	"""Class Gate depicts a basic logic gate with 1 or 2 inputs and at least 1 output """
	def __init__(self, name, gate_type):
		"""Initialises the Gate object.
		Inputs:
		name : str
			Name of the gate
		gate_type : str
			Logic gate type - ex. "INV", "OR", "AND", etc.

		Outputs:
		list[int] - list of ints
			An output vector

		Exceptions:
		ValueError
			If the given gate type didn't match one of the handled types
		"""
		if gate_type not in ("INV", "OR", "AND", "XOR", "NOR", "NAND", "XNOR"):
			raise ValueError(f"{gate_type} is not a valid Gate type")
		self._gate_type = gate_type  # Gate name
		self._name = name

	def get_output(self, inputs):
		"""Updates the output of the gate as a logic function of the inputs depicted by the gate type
		Inputs:
		inputs: list[list[int]] - list of lists of ints
			List of input vectors

		Outputs:
		list[int] - list of ints
			An output vector

		Exceptions:
		ValueError
			If one of the inputs (in case of INV and BUFFER input 1) is not connected
		"""
		if len(inputs) > 2 or (len(inputs) > 1 and self._gate_type == "INV"):
			raise ValueError("Invalid number of inputs to the gate")

		if len(inputs) == 2 and len(inputs[0]) != len(inputs[1]):
			raise ValueError("Invalid input lengths")

		if self._gate_type == "INV":
			return self.__NOT(inputs[0])
		elif self._gate_type == "OR":
			return self.__OR(inputs[0], inputs[1])
		elif self._gate_type == "AND":
			return self.__AND(inputs[0], inputs[1])
		elif self._gate_type == "XOR":
			return self.__XOR(inputs[0], inputs[1])
		elif self._gate_type == "NOR":
			return self.__NOT(self.__OR(inputs[0], inputs[1]))
		elif self._gate_type == "NAND":
			return self.__NOT(self.__AND(inputs[0], inputs[1]))
		elif self._gate_type == "XNOR":
			return self.__NOT(self.__XOR(inputs[0], inputs[1]))

	def __NOT(self, input_vec):
		"""NOT logic function - used on the gate input and the result stored in the gate output
		Inputs:
		input_vec: list[int] - list of ints
			Input vectors for the function

		Outputs:
		list[int] - list of ints
			An output vector
		"""
		output_vec = []
		for inp in input_vec:
			if inp == 0:
				output_vec.append(1)
			elif inp == 1:
				output_vec.append(0)
		return output_vec

	def __AND(self, input_vec1, input_vec2):
		"""AND logic function - used on the gate inputs and the result stored in the gate output
		Inputs:
		input_vec1: list[int] - list of ints
			1st input vectors for the function
		input_vec2: list[int] - list of ints
			2nd input vectors for the function

		Outputs:
		list[int] - list of ints
			An output vector
		"""
		output_vec = []
		for i in range(len(input_vec1)):
			if (input_vec1[i], input_vec2[i]) in ((0, 0), (0, 1), (1, 0)):
				output_vec.append(0)
			elif (input_vec1[i], input_vec2[i]) == (1, 1):
				output_vec.append(1)
		return output_vec

	def __OR(self, input_vec1, input_vec2):
		"""OR logic function - used on the gate inputs and the result stored in the gate output
		Inputs:
		input_vec1: list[int] - list of ints
			1st input vectors for the function
		input_vec2: list[int] - list of ints
			2nd input vectors for the function

		Outputs:
		list[int] - list of ints
			An output vector
		"""
		output_vec = []
		for i in range(len(input_vec1)):
			if (input_vec1[i], input_vec2[i]) == (0, 0):
				output_vec.append(0)
			elif (input_vec1[i], input_vec2[i]) in ((0, 1), (1, 0), (1, 1)):
				output_vec.append(1)
		return output_vec

	def __XOR(self, input_vec1, input_vec2):
		"""XOR logic function - used on the gate inputs and the result stored in the gate output
		Inputs:
		input_vec1: list[int] - list of ints
			1st input vectors for the function
		input_vec2: list[int] - list of ints
			2nd input vectors for the function

		Outputs:
		list[int] - list of ints
			An output vector
		"""
		output_vec = []
		for i in range(len(input_vec1)):
			if (input_vec1[i], input_vec2[i]) in ((0, 0), (1, 1)):
				output_vec.append(0)
			elif (input_vec1[i], input_vec2[i]) in ((0, 1), (1, 0)):
				output_vec.append(1)
		return output_vec

	def __hash__(self):
		return hash(id(self))
from Gate import Gate, Port
from Signal import Signal


class Circuit:

	def __init__(self, name, gate_level_file): # TODO: get only file name
		self._name = name
		self._ingoing = {} # key = Dst Gate : value = { Src Gate : Signal }
		self._outgoing = {} # key = Src Gate : value = { Dst Gate : Signal }
		self._inputs = {} # key = input Port name, value = input Port
		self._outputs = {} # key = output Port name, value = output Port
		self.__parse_file(gate_level_file)


	def __parse_file(self, gate_level_file):

		if not str(gate_level_file).endswith(".gatelevel"):
			raise Exception("Incompatible file format")
		try:
			f = open(gate_level_file)
		except:
			raise Exception("File couldn't be opened")

		gate_dict = {}
		for line in f:
			line = line.split()
			gate = Gate(line[0], line[-1])
			gate_dict[gate] = line[1:-1]

		f.close()

		for gate in gate_dict:
			self._ingoing[gate] = {}
			self._outgoing[gate] = {}

		for gate1 in gate_dict:
			inputs, outp = gate_dict[gate1][0:-1], gate_dict[gate1][-1]
			for inp in inputs:
				found_output = False
				for gate2 in gate_dict:
					if gate1 is gate2:
						continue
					if inp == gate_dict[gate2][-1]:
						found_output = True
						sig = Signal(inp, gate2, gate1)
						self._ingoing[gate1][gate2] = sig
						self._outgoing[gate2][gate1] = sig
						break
				if not found_output:
					try:
						port = self._inputs[inp]
					except KeyError:
						port = Port(inp, is_input=True)
						self._inputs[inp] = port
						self._outgoing[port] = {}

					sig = Signal(inp, port, gate1)
					self._ingoing[gate1][port] = sig
					self._outgoing[port][gate1] = sig

		for gate in gate_dict:
			if not self._outgoing[gate]:
				outp = gate_dict[gate][-1]
				port = Port(outp, is_input=False)
				sig = Signal(outp, gate, port)
				self._outputs[outp] = port
				try:
					self._ingoing[port][gate] = sig
				except KeyError:
					self._ingoing[port] = {gate : sig}
				self._outgoing[gate][port] = sig


	def get_output_vectors_file(self, input_vector_file):

		output_vectors_dict = self.get_output_from_file(input_vector_file)
		alpha_sorted_output_names = sorted(output_vectors_dict.keys())

		f = open("data/" + self._name + ".out", 'w')

		f.write(','.join(alpha_sorted_output_names)+'\n')
		for i in range(len(output_vectors_dict[alpha_sorted_output_names[0]])):
			outputs = [str(output_vectors_dict[name][i]) for name in alpha_sorted_output_names]
			f.write(','.join(outputs) + '\n')

		f.close()

	def get_output_from_file(self, input_vector_file):

		if not str(input_vector_file).endswith(".vec"):
			raise Exception("Incompatible file format")

		try:
			f = open(input_vector_file)
		except:
			raise Exception("File couldn't be opened")

		input_vectors = tuple((input_name, []) for input_name in f.readline().strip().split(','))

		for line in f:
			inputs = line.strip().split(',')
			for i in range(len(inputs)):
				input_vectors[i][1].append(int(inputs[i]))

		f.close()
		return self.get_outputs({inp[0]: inp[1] for inp in input_vectors})

	def memoize_outputs(self, output_func):
		outputs_dict = {} ## dict = Gate : out vector
		def outputs(gate):
			if gate not in outputs_dict:
				outputs_dict[gate] = output_func(gate)
			return outputs_dict[gate]

		return outputs


	@memoize_outputs
	def __get_outputs_rec(self, vertex):
		input_vector = []
		for signal in self._ingoing[vertex].values():
			if not signal.value_vector:
				# signal.value_vector = self.__get_outputs_rec(signal.get_opposite(vertex))
				signal.set_val_vec(self.__get_outputs_rec(signal.get_opposite(vertex)))
			input_vector.append(signal.value_vector)
		a = vertex.get_output(input_vector)
		return a

# TODO: try to do memoization
	def get_outputs(self, inputs):
		if not inputs:
			raise ValueError("No inputs have been given")

		if len(inputs) != len(self._inputs):
			raise ValueError("Incompatible inputs")

		for inp in self._inputs.values():
			input_vector = inputs[inp.name]
			for signal in self._outgoing[inp].values():
				signal.value_vector = input_vector
		a = {output.name: self.__get_outputs_rec(output) for output in self._outputs.values()}
		return a

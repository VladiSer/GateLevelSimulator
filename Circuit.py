from Gate import Gate, Port
from Signal import Signal


class Circuit:

	def __init__(self, name, gate_level_file): # TODO: get only file name
		self._name = name
		self._ingoing = {} # key = Dst Gate : value = { Src Gate : Signal }
		self._outgoing = {} # key = Src Gate : value = { Dst Gate : Signal }
		self._inputs = {} # key = input Port name, value = input Port
		self._outputs = {} # key = output Port name, value = output Port
		self._Gate_outputs_values = {} # key = Gate/Port, value = vector of values (0/1)
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

		output_vectors_dict = self.get_output_values_from_file(input_vector_file)
		alpha_sorted_output_names = sorted(output_vectors_dict.keys())

		f = open("data/" + self._name + ".out", 'w')

		f.write(','.join(alpha_sorted_output_names)+'\n')
		for i in range(len(output_vectors_dict[alpha_sorted_output_names[0]])):
			outputs = [str(output_vectors_dict[name][i]) for name in alpha_sorted_output_names]
			f.write(','.join(outputs) + '\n')

		f.close()

	def get_output_values_from_file(self, input_vector_file):

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

	def __get_outputs_rec(self, gate):
		input_vector = []
		for src_gate in self._ingoing[gate]:
			if src_gate not in self._Gate_outputs_values:
				self._Gate_outputs_values[src_gate] = self.__get_outputs_rec(src_gate)
			input_vector.append(self._Gate_outputs_values[src_gate])
		return gate.get_output(input_vector)

	def get_outputs(self, inputs):
		if not inputs:
			raise ValueError("No inputs have been given")

		if len(inputs) != len(self._inputs):
			raise ValueError("Incompatible inputs")

		for inp in self._inputs.values():
			try:
				self._Gate_outputs_values[inp] = inputs[inp.name]
			except KeyError:
				raise Exception(".vec file is incompatible with the .gatelevel file")

		return {output.name: self.__get_outputs_rec(output) for output in self._outputs.values()}

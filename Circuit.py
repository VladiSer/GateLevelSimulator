from Gate import Gate, Port
from Signal import Signal


class Circuit:

	def __init__(self, name, gate_level_file):
		self._name = name
		self._ingoing = {}
		self._outgoing = {}
		self._inputs = []
		self._outputs = []
		self.__parse_file(gate_level_file)



	def __parse_file(self, gate_level_file):

		if not str(gate_level_file).endswith(".gatelevel"):
			raise Exception("Incompatible file format")
		try:
			f = open(gate_level_file)
		except:
			raise Exception("File couldn't be opened")

		# TODO: THAT

		f.close()
		raise NotImplementedError()

	def get_output_vectors_file(self, input_vector_file):

		output_vectors_dict = self.get_output_from_file(input_vector_file)
		alpha_sorted_output_names = sorted(output_vectors_dict.keys())

		f = open(self._name, 'W',)

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

		input_vectors = ((input_name, []) for input_name in f.readline().strip().split(','))

		for line in f:
			inputs = line.strip().split(',')
			for i in range(len(inputs)):
				input_vectors[i][1].append(inputs[i])

		f.close()

		return self.get_outputs({inp[0]: inp[1] for inp in input_vectors})

	def __get_outputs_rec(self, vertex):

		input_vector = []
		for signal in self._ingoing[vertex]:
			if not signal.value_vector:
				signal.value_vector = self.__get_outputs_rec(signal.get_opposite(vertex))
			input_vector.append(signal.value_vector)
		return vertex.get_output(input_vector)

	def get_outputs(self, **inputs):
		if not inputs:
			raise ValueError("No inputs have been given")

		if len(list(inputs.keys())) != len(inputs):
			raise ValueError("Incompatible inputs")

		for inp in self._inputs:
			input_vector = inputs[inp.name]
			for signal in self._outgoing[inp]:
				signal.value_vector = input_vector
		return {output.name: self.__get_outputs_rec(output) for output in self._outputs}

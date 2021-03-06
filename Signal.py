class Signal:
	"""Class signal, depicts a wire/signal connecting between two gates.
	Connection occurs from the output of the source gate to one of the inputs of the destination gate.
	"""
	def __init__(self, name, src_gate, dst_gate):
		"""Initialises the Signal object.
		Inputs:
		name : str
			Name of the signal
		src_gate : Gate
			Source gate
		dst_gate : Gate
			Destination gate
		"""
		self._name = name
		self._src_gate = src_gate
		self._dst_gate = dst_gate

	def get_end_points(self):
		"""Gets the gates that the signal connects between them.
		Outputs:
		tuple (Gate, Gate)
			A tuple consisting of source gate at index 0 and destination gate at index 1
		"""
		return self._src_gate, self._dst_gate

	def get_opposite(self, gate):
		"""Gets the gate from the opposite side of the gate given
		Inputs:
		gate : Gate
			One of the gates connected to the signal

		Exceptions:
		ValueError
			If the given gate is not one of the two gates connected to the signal

		Outputs:
		Gate
			The gate on the opposite connection of the function input gate
		"""
		if gate is self._src_gate:
			return self._dst_gate
		elif gate is self._dst_gate:
			return self._src_gate
		raise ValueError(f"{gate.name} is not connected to this signal")

	def __hash__(self):
		return hash((self._src_gate, self._dst_gate))

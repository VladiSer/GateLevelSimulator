
class Signal:

	def __init__(self, name, src_gate, dst_gate):
		self._name = name
		self._src_gate = src_gate
		self._dst_gate = dst_gate

	def end_points(self):
		return self._src_gate, self._dst_gate

	def opposite(self, gate):
		if gate is self._src_gate:
			return self._dst_gate
		elif gate is self._dst_gate:
			return self._src_gate
		raise ValueError(f"{gate.name} is not connected to this signal")

	def __hash__(self):
		return hash((self._src_gate, self._dst_gate))
from Circuit import Circuit


for i in range(1, 5):
	circuit = Circuit(f"data/cir{i}.gatelevel", f"Circuit{i}")
	circuit.get_output_vectors_file(f"data/cir{i}.vec")
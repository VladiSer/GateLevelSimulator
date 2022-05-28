from Circuit import Circuit
import os

input_files = []
for file in os.listdir("data\\"):
	if os.path.isfile(os.path.join("data\\", file)) and file.endswith(".gatelevel"):
		vec_file_name = file.removesuffix(".gatelevel") + ".vec"
		if vec_file_name in os.listdir("data\\"):
			gatelevel_file_name = "data/" + file
			vec_file_name = "data/" + vec_file_name
			input_files.append((gatelevel_file_name, vec_file_name))


for i in range(len(input_files)):
	gatelevel_file, vec_file = input_files[i][0], input_files[i][1]
	circuit = Circuit(gatelevel_file)
	circuit.get_output_vectors_file(vec_file)
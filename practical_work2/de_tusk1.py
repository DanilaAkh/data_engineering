import numpy as np
import json


file_name = "matrix_10"
mat = np.load(f"{file_name}.npy")
#print(mat)
length = len(mat)
data = {
    "sum" : 0,
    "avg" : 0,
    "sum_main" : 0,
    "avg_main" : 0,
    "sum_side" : 0,
    "avg_side" : 0,
    "max" : 0,
    "min" : 1000
    }
for i in range(length):
    for j in range(length):
        data["sum"] += mat[i][j]
        if i == j:
            data["sum_main"] += mat[i][j]
        if i + j == length:
            data["sum_side"] += mat[i][j]
        data["max"] = max(data["max"], mat[i][j])
        data["min"] = min(data["min"], mat[i][j])

data["avg"] = data["sum"] / length ** 2
data["avg_main"] = data["sum_main"] / length
data["avg_side"] = data["sum_side"] / length

for key in data.keys():
    data[key] = float(data[key])

with open(f"out_{file_name}.json", 'w') as f:
    f.write(json.dumps(data))

norm_mat = np.ndarray(shape=(length, length), dtype=float)

for i in range(length):
    for j in range(length):
        norm_mat[i][j] = mat[i][j] / data["sum"]
        
np.save(f"out_norm_{file_name}.npy", norm_mat)
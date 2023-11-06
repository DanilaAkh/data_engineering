import numpy as np
import os


file_name = "matrix_10_2"
mat = np.load(f"{file_name}.npy")

x,y,z = [],[],[]

for i, line in enumerate(mat):
    for j, num in enumerate(line):
        if num > 510:                  # Вариант 10
            x.append(i)
            y.append(j)
            z.append(num)

np.savez(f"out_{file_name}.npz", x=x,y=y,z=z)
np.savez_compressed(f"out_{file_name}_comp.npz", x=x,y=y,z=z)

ratio = os.path.getsize(f"out_{file_name}.npz") / os.path.getsize(f"out_{file_name}_comp.npz")
print(f"Сжатый файл меньше в {ratio} раз")
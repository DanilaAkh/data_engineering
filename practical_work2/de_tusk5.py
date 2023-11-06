import csv
import json
import pickle
import msgpack
import numpy as np
import os


file_name = "Electric_Vehicle_Population_Data"
lines = []
data_to_json = {
    "Postal_Code_max": float(0),
    "Postal_Code_min": float(10000000),
    "Postal_Code_avg": float(0),
    "Postal_Code_sum": float(0),
    "Postal_Code_sko": float(0),
    "Model_Year_max": float(0),
    "Model_Year_min": float(10000000),
    "Model_Year_avg": float(0),
    "Model_Year_sum": float(0),
    "Model_Year_sko": float(0)
}
with open(f"{file_name}.csv", "r") as f:
    reader = csv.reader(f)    
    for line in reader:
        lines.append(line[1:8])

list_to_std_my = []
list_to_std_pc = []

for line in lines[1:]:
    if line[0]+"_county" not in data_to_json and line[0] != '':
        data_to_json[line[0]+"_county"] = 1
    elif line[0]+"_county" in data_to_json:
        data_to_json[line[0]+"_county"] += 1

    if line[1]+"_city" not in data_to_json and line[1] != '':
        data_to_json[line[1]+"_city"] = 1
    elif line[1]+"_city" in data_to_json:
        data_to_json[line[1]+"_city"] += 1

    if line[2]+"_state" not in data_to_json and line[2] != '':
        data_to_json[line[2]+"_state"] = 1
    elif line[2]+"_state" in data_to_json:
        data_to_json[line[2]+"_state"] += 1

    if line[3] != '':
        data_to_json["Postal_Code_max"] = max(data_to_json["Postal_Code_max"], float(line[3]))
        data_to_json["Postal_Code_min"] = min(data_to_json["Postal_Code_min"], float(line[3]))
        data_to_json["Postal_Code_sum"] += float(line[3])
        list_to_std_pc.append(float(line[3]))
    
    if line[4] != '':
        data_to_json["Model_Year_max"] = max(data_to_json["Model_Year_max"], float(line[4]))
        data_to_json["Model_Year_min"] = min(data_to_json["Model_Year_min"], float(line[4]))
        data_to_json["Model_Year_sum"] += float(line[4])
        list_to_std_my.append(float(line[4]))
    
    if line[5]+"_make" not in data_to_json and line[5] != '':
        data_to_json[line[5]+"_make"] = 1
    elif line[5]+"_make" in data_to_json:
        data_to_json[line[5]+"_make"] += 1
    
    if line[6]+"_model" not in data_to_json and line[6] != '':
        data_to_json[line[6]+"_model"] = 1
    elif line[6]+"_model" in data_to_json:
        data_to_json[line[6]+"_model"] += 1

data_to_json["Postal_Code_avg"] = data_to_json["Postal_Code_sum"] / len(lines)
data_to_json["Model_Year_avg"] = data_to_json["Model_Year_sum"] / len(lines)

data_to_json["Postal_Code_sko"] = np.std(list_to_std_pc, ddof=1)
data_to_json["Model_Year_sko"] = np.std(list_to_std_my, ddof=1)

with open(f"out_processed_data.json", 'w') as f:
    f.write(json.dumps(data_to_json))


with open(f"out_{file_name}.csv", 'w', newline='') as f:
    wrt = csv.writer(f)
    wrt.writerows(lines)

with open(f"out_{file_name}.json", "w") as f:
    f.write(json.dumps(lines))

with open(f"out_{file_name}.msgpack", "wb") as f:
    f.write(msgpack.dumps(lines))

with open(f"out_{file_name}.pkl", "wb") as f:
    f.write(pickle.dumps(lines))

print("csv       =", os.path.getsize(f"out_{file_name}.csv"), "bytes")
print("json      =", os.path.getsize(f"out_{file_name}.json"), "bytes")
print("msgpack   =", os.path.getsize(f"out_{file_name}.msgpack"), "bytes")
print("pkl       =", os.path.getsize(f"out_{file_name}.pkl"), "bytes")
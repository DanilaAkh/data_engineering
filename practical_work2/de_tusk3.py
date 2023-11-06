import json
import msgpack
import os


file_name = "products_10"
data = {}
products = {}
with open(f"{file_name}.json", "r") as f:
    data = json.load(f)

for item in data:
    if item["name"] in products:
        products[item["name"]].append(item["price"])
    else:
        products[item["name"]] = []
        products[item["name"]].append(item["price"])

data_out = []
for key, value in products.items():
    data_out.append({
            "name": key,
            "avg" : sum(value)/len(value),
            "max" : max(value),
            "min" : min(value)
        }
    )


with open(f"out_{file_name}.json", "w") as f:
    f.write(json.dumps(data_out))

with open(f"out_{file_name}.msgpack", "wb") as f:
    f.write(msgpack.dumps(data_out))

ratio =  os.path.getsize(f"out_{file_name}.json") / os.path.getsize(f"out_{file_name}.msgpack")
print(f"json файл больше чем msgpack в {ratio} раз")
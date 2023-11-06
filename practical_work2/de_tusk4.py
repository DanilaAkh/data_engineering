import json
import pickle


file_name_json = "price_info_10"
file_name_pkl = "products_10"
data_json = {}
data_pkl = {}

with open(f"{file_name_json}.json", "r") as f:
    data_json = json.load(f)

with open(f"{file_name_pkl}.pkl", "rb") as f:
    data_pkl = pickle.load(f)

for item_pkl in data_pkl:
    for item_json in data_json:
        if item_pkl["name"] == item_json["name"]:
            if item_json["method"] == "sum":
                item_pkl["price"] += item_json["param"]
            elif item_json["method"] == "sub":
                item_pkl["price"] -= item_json["param"]
            elif item_json["method"] == "percent+":
                item_pkl["price"] += item_pkl["price"] * item_json["param"]
            elif item_json["method"] == "percent-":
                item_pkl["price"] -= item_pkl["price"] * item_json["param"]

with open(f"out_{file_name_pkl}.pkl", "wb") as f:
    f.write(pickle.dumps(data_pkl))
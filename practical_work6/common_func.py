import json
import pandas as pd



def read_data(file_name, i=1):
    if i == 1:
        return pd.read_csv(file_name, low_memory=False)
    elif i == 2:
       pass


def write_to_json(file_name, data):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(json.dumps(data))
    print(f"Запись успешно выполнена в {file_name}")
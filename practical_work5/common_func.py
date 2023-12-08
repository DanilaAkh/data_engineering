import json


def write_json(file_name, data, task_num : int):
    with open(f".\\task{task_num}\\out_{file_name}.json", "w", encoding="UTF-8")as f:
        f.write(json.dumps(data, ensure_ascii=False))


def insert_data(collection, data):
    collection.insert_many(data)
import json
import os
from bs4 import BeautifulSoup
import numpy as np


def handler_file(file_name):
    with open(f".\\zip_4_var_10\\{file_name}", "r", encoding="UTF-8") as f:
        items = []
        text = ""
        for row in f.readlines():
            text += row
        clothing = BeautifulSoup(text, "xml")
        products = clothing.find_all("clothing")
        for product in products:
            item = {}
            for el in product:
                if el.name is not None:
                    item[el.name] = el.get_text().strip()
                    if item[el.name].isdigit():
                        item[el.name] = int(item[el.name])
            items.append(item)
            item["rating"] = float(item["rating"])
        return items

items = []
for filename in os.listdir('.\\zip_4_var_10'):
    if filename[filename.rfind(".") + 1:] in ['xml']:
        items += handler_file(filename)

# Сортировка по цене (по возрастанию)
items = sorted(items, key=lambda x: x["price"])

with open("out_tusk4.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# Фильтрация продуктов с рейтингом > 4.5
filtered_data = []
for item in items:
    if item["rating"] > 4.5:
        filtered_data.append(item)

print("Количество продуктов с рейтингом больше 4.5:", len(filtered_data))

# Подсчет статистических характеристик для поля reviews
sum_ = 0
max_ = 0
min_ = 1000000000
list_to_std = []
for item in items:
    list_to_std.append(item["reviews"])
    sum_ += item["reviews"]
    max_ = max(max_, item["reviews"])
    min_ = min(min_, item["reviews"])

avg = sum_ / len(items)
std = np.std(list_to_std, ddof=1)
print("Суммарное количество просмотров:", sum_)
print("Минимальное количество просмотров:", min_)
print("Максимальный количество просмотров:", max_)
print("Среднее количество просмотров:", avg)
print("СКО:", std)

# Подсчет частоты меток category
data_category = {}
for item in items:    
    if item["category"] in data_category:
        data_category[item["category"]] += 1
    elif item["category"] not in data_category:
        data_category[item["category"]] = 1

print(data_category)
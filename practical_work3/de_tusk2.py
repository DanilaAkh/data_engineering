from bs4 import BeautifulSoup
import os
import json
import numpy as np


def handler_file(file_name):
    items = []
    with open(f".\\zip_2_var_10\\{file_name}", "r", encoding="UTF-8") as f:
        text = ""
        for row in f.readlines():
            text += row
    site = BeautifulSoup(text, "lxml")
    products = site.find_all("div", attrs={"class": "product-item"})
        
    for product in products:
        item = {}
        item["id"] = int(product.a["data-id"])
        item["link"] = product.find_all("a")[1]["href"]
        item["img"] = product.find_all("img")[0]["src"]
        item["product"] = product.find_all("span")[0].get_text().strip()
        item["price"] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
        item["bonus"] = int(product.strong.get_text().replace("+ начислим", "").replace("бонусов", "").strip())
        props = product.ul.find_all("li")
        for prop in props:
            item[prop["type"]] = prop.get_text().strip()
        items.append(item)
    return items

items = []
for filename in os.listdir('.\\zip_2_var_10'):
    if filename[filename.rfind(".") + 1:] in ['html']:
        items += handler_file(filename)

# Сортировка по id
items = sorted(items, key=lambda x: x["id"])
print("Всего продуктов:", len(items))

with open("out_tusk2.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# Сортировка по цене (более 200000)
filtered_data = []
for product in items:
    if product["price"] >= 200000:
        filtered_data.append(product["price"])

print("Количество продуктов со стоимостью > 200000:", len(filtered_data))

# Статистические характеристики поля бонус
sum_ = 0
max_ = 0
min_ = 1000000
list_to_std = []
for product in items:
    list_to_std.append(product["bonus"])
    sum_ += product["bonus"]
    max_ = max(max_, product["bonus"])
    min_ = min(min_, product["bonus"])

avg = sum_ / len(items)
std = np.std(list_to_std, ddof=1)
print("Суммарное количество бонусов:", sum_)
print("Максимальное количество бонусов:", max_)
print("Минимальное количество бонусов:", min_)
print("Среднее количество бонусов:", avg)
print("СКО:", std)

# Подсчет частоты продуктов с количеством sim слотов
data_sim = {}
for product in items:
    if "sim" not in product:
        continue
    if product["sim"] in data_sim:
        data_sim[product["sim"]] += 1
    elif product["sim"] not in data_sim:
        data_sim[product["sim"]] = 1

print(data_sim)
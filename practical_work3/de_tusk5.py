from bs4 import BeautifulSoup
import os
import json
import numpy as np


def handler_files(file_name):
    with open(f".\\tusk5_1\\{file_name}", "r", encoding="UTF-8") as f:
        text = ""
        for row in f.readlines():
            text += row
    site = BeautifulSoup(text, "lxml")
    item = {}
    item["name"] = site.find_all("h1", attrs={"class" : "product-info__name"})[0].get_text().strip()
    item["img"] = site.find_all("img", attrs={"class" : "product-info-images__image"})[0]["src"]
    item["price"] = float(site.find_all("div", attrs={"class" : "product-price__wrapper"})[0].get_text().strip())
    item["proteins"] = float(site.find_all("span", attrs={"class" : "product-info-nutritional-value__value"})[0].get_text().strip())
    item["fats"] = float(site.find_all("span", attrs={"class" : "product-info-nutritional-value__value"})[1].get_text().strip())
    item["carbohydrates"] = float(site.find_all("span", attrs={"class" : "product-info-nutritional-value__value"})[2].get_text().strip())
    item["kcal"] = float(site.find_all("span", attrs={"class" : "product-info-nutritional-value__value"})[3].get_text().strip())
    item["expiration"] = site.find_all("span", attrs={"class" : "product-description__info-value"})[1].get_text().strip()
    return item

def handler_files_2(file_name):
    items = []
    with open(f".\\tusk5_2\\{file_name}", "r", encoding="UTF-8") as f:
        text = ""
        for row in f.readlines():
            text += row
    site = BeautifulSoup(text, "lxml")
    products = site.find_all("a", attrs={"class": "product-tile category-products__item category-products__item_order"})
    
    for product in products:
        item = {}
        item["name"] = product.find_all("img")[0]["alt"].split(",")[0].strip()
        item["img"] = product.find_all("img")[0]["src"]        
        item["price"] = float(product.find_all("span", attrs={"class" : "product-price__value"})[0].get_text().replace(" ", "").strip())
        item["unit_measure"] = int(product.find_all("span", attrs={"class" : "product-tile__unit-measure"})[0].get_text().split()[1].strip())
        items.append(item)
    return items

items = []
for filename in os.listdir('.\\tusk5_1'):
    if filename[filename.rfind(".") + 1:] in ['html']:
        item = handler_files(filename)
        items.append(item)

# Сортировка по полю kcal (по убыванию)
items = sorted(items, key=lambda x: x["kcal"], reverse=True)

with open("out_tusk5_1.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# фильтрация данных с жирами < 9
filtered_data = []
for item in items:
    if item["fats"] < 9:
        filtered_data.append(item) 
print("Количество продуктов с жирами менее 9:", len(filtered_data))

# Подсчет статистических характеристик для поля proteins
sum_ = 0
max_ = 0
min_ = 1000000000
list_to_std = []
for item in items:
    list_to_std.append(item["proteins"])
    sum_ += item["proteins"]
    max_ = max(max_, item["proteins"])
    min_ = min(min_, item["proteins"])

avg = sum_ / len(items)
std = np.std(list_to_std, ddof=1)
print("Суммарное количество белков:          ", sum_)
print("Минимальное количество белков:        ", min_)
print("Максимальный количество белков:       ", max_)
print("Среднее количество белков:            ", avg)
print("СКО:                                  ", std)

# Подсчет частоты меток carbohydrates
data_carbohydrates = {}
for item in items:    
    if item["carbohydrates"] in data_carbohydrates:
        data_carbohydrates[item["carbohydrates"]] += 1
    elif item["carbohydrates"] not in data_carbohydrates:
        data_carbohydrates[item["carbohydrates"]] = 1

print(data_carbohydrates)
########################################################################################
items = []
for filename in os.listdir('.\\tusk5_2'):
    if filename[filename.rfind(".") + 1:] in ['html']:
        items += handler_files_2(filename)

# Сортировка по полю price (по убыванию)
items = sorted(items, key=lambda x: x["price"], reverse=True)

with open("out_tusk5_2.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# фильтрация данных с массой < 120
filtered_data = []
for item in items:
    if item["unit_measure"] < 120:
        filtered_data.append(item) 
print("Количество продуктов массой менее 120:", len(filtered_data))

# Подсчет статистических характеристик для поля price
sum_ = 0
max_ = 0
min_ = 1000000000
list_to_std = []
for item in items:
    list_to_std.append(item["price"])
    sum_ += item["price"]
    max_ = max(max_, item["price"])
    min_ = min(min_, item["price"])

avg = sum_ / len(items)
std = np.std(list_to_std, ddof=1)
print("Суммарное цена продуктов:             ", sum_)
print("Минимальная цена за продукт:          ", min_)
print("Максимальная цена за продукт:         ", max_)
print("Средняя цена за продукт:              ", avg)
print("СКО:                                  ", std)

# Подсчет частоты меток category
data_unit_measure = {}
for item in items:    
    if item["unit_measure"] in data_unit_measure:
        data_unit_measure[item["unit_measure"]] += 1
    elif item["unit_measure"] not in data_unit_measure:
        data_unit_measure[item["unit_measure"]] = 1

print(data_unit_measure)
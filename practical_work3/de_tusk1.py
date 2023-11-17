from bs4 import BeautifulSoup
import os
import re
import json
import numpy as np


def handler_file(file_name):
    with open(f".\\zip_1_var_10\\{file_name}", "r", encoding="UTF-8") as f:
        text = ""
        for row in f.readlines():
            text += row
        site = BeautifulSoup(text, "lxml")
        item = {}
        item["city"] = site.find_all("span", string=re.compile("Город:"))[0].get_text().replace("Город:", "").strip()
        item["structure"] = site.find_all("h1", string=re.compile("Строение:"))[0].get_text().replace("Строение:", "").strip()
        item["street"] = site.find_all("p", string=re.compile("Улица:"))[0].get_text().split("Индекс:")[0].replace("Улица:", "").strip()
        item["index"] = int(site.find_all("p", string=re.compile("Улица:"))[0].get_text().split("Индекс:")[1].strip())
        item["floors"] = int(site.find_all("span", attrs="floors")[0].get_text().split("Этажи:")[1].strip())
        item["built"] = int(site.find_all("span", attrs="year")[0].get_text().split("Построено в")[1].strip())
        item["rating"] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().replace("Рейтинг: ", "").strip())
        item["views"] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().replace("Просмотры: ", "").strip())
        return item

items = []
for filename in os.listdir('.\\zip_1_var_10'):
    if filename[filename.rfind(".") + 1:] in ['html']:
        item = handler_file(filename)
        items.append(item)

# Сортировка по рейтингу
items = sorted(items, key=lambda x: x["rating"], reverse=True)

with open(f"out_tusk1.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

# Фильтрация по полю количества этажей
filtered_data = []
for building in items:
    if building["floors"] >= 5:
        filtered_data.append(building["floors"]) 

print("Количество зданий с пятью и более этажами:", len(filtered_data))

# Статистические характеристики поля просмотры
sum_ = 0
max_ = 0
min_ = 1000000
list_to_std = []
for building in items:
    list_to_std.append(building["views"])
    sum_ += building["views"]
    max_ = max(max_, building["views"])
    min_ = min(min_, building["views"])

avg = sum_ / len(items)
std = np.std(list_to_std, ddof=1)
print("Суммарное количество просмотров:", sum_)
print("Максимальное количество просмотров:", max_)
print("Минимальное количество просмотров:", min_)
print("Среднее количество просмотров:", avg)
print("СКО:", std)

# Подсчет частоты зданий в городах
data_city = {}
for building in items:
    if building["city"] in data_city:
        data_city[building["city"]] += 1
    elif building["city"] not in data_city:
        data_city[building["city"]] = 1

print(data_city)
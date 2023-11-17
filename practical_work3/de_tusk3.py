from bs4 import BeautifulSoup
import os
import json
import numpy as np


def handler_file(file_name):
    with open(f".\\zip_3_var_10\\{file_name}", "r", encoding="UTF-8") as f:
        text = ""
        for row in f.readlines():
            text += row
        star = BeautifulSoup(text, "xml").star
        item = {}
        for el in star.contents:
            if el.name is not None:
                item[el.name] = el.get_text().strip()
        item["radius"] = int(item["radius"])        
        return item

    
stars = []
for filename in os.listdir('.\\zip_3_var_10'):
    if filename[filename.rfind(".") + 1:] in ['xml']:
        data = handler_file(filename)
        stars.append(data)

# Сортировка по distance (по возрастанию)
stars = sorted(stars, key=lambda x: x["distance"])

with open("out_tusk3.json", "w", encoding="UTF-8") as f:
    f.write(json.dumps(stars, ensure_ascii=False))

# Запись всех звезд с созвездием Стрелец
filtered_data = []
for star in stars:
    if star["constellation"] == "Стрелец":
        filtered_data.append(star)

print("Количество звезд в списке из созвездия Стрелец:", len(filtered_data))

# Подсчет статистических характеристик для поля radius
sum_ = 0
max_ = 0
min_ = 1000000000
list_to_std = []
for star in stars:
    list_to_std.append(star["radius"])
    sum_ += star["radius"]
    max_ = max(max_, star["radius"])
    min_ = min(min_, star["radius"])

avg = sum_ / len(stars)
std = np.std(list_to_std, ddof=1)
print("Суммарный радиус звезд:", sum_)
print("Минимальный радиус:", min_)
print("Максимальный радиус:", max_)
print("Средний радиус:", avg)
print("СКО:", std)

# Подсчет частоты меток constellation
data_constellation = {}
for star in stars:    
    if star["constellation"] in data_constellation:
        data_constellation[star["constellation"]] += 1
    elif star["constellation"] not in data_constellation:
        data_constellation[star["constellation"]] = 1

print(data_constellation)
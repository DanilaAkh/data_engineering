from bs4 import BeautifulSoup
import csv


file_name = "text_5_var_10"
data_to_csv = []

with open(file_name, "r", encoding="UTF-8") as f:
    soup = BeautifulSoup(f, "lxml")
    count_of_cit = len(soup.find_all("tr"))
    all_data = soup.find_all("td")

for i in range(0, len(all_data), 5):
    temp_list = []
    for j in range(i, i+5):
        temp_list.append(*all_data[j])
    data_to_csv.append(temp_list)

with open(f"out_{file_name}", "w", encoding="UTF-8", newline='') as f:
    csv_wrt = csv.writer(f)
    csv_wrt.writerows(data_to_csv)
import csv


file_name = "text_4_var_10"
lines = []
avg_salary = 0
with open(file_name, 'r', encoding="UTF-8")as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        lines.append(line[:-1])

for i in range(len(lines)):
    avg_salary += int(lines[i][-1][:-1])
    lines[i][1] = " ".join([lines[i][1], lines[i][2]])
    lines[i].pop(2)
avg_salary /= len(lines)

# Фильтр по доходу больше среднего
for i in range(len(lines)-1, -1, -1):    
    if int(lines[i][-1][:-1]) < avg_salary:
        lines.pop(i)

# Фильтр по возрасту больше 25, вариант №10
for i in range(len(lines)-1, -1, -1):    
    if int(lines[i][-2]) <= 25:
        lines.pop(i)

lines = sorted(lines, key=lambda row: int(row[0]))

tmp = lines.copy()



with open(f"out_{file_name}", "w", encoding="UTF-8", newline='') as csv_f:
    wrt = csv.writer(csv_f)
    wrt.writerows(lines)
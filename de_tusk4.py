import csv


file_name = "text_4_var_10"
lines = []
avg_salary = 0
with open(file_name, 'r', encoding="UTF-8")as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        lines.append(line[:-1])

for i in range(len(lines)):
    avg_salary += int(lines[i][-1][:-1])asd
avg_salary /= len(lines)

for i in range(len(lines)-i):
    if int(lines[i][-1][:-1]) < avg_salary:
        lines[i]


for line in lines:
    print(line)
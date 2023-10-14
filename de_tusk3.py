file_name = "text_3_var_10"
lines = ""
with open(file_name, "r") as f:
    lines = f.readlines()

lines_2 = []
for line in lines:
    list_line = line.split(",")
    for i in range(len(list_line)):
        if list_line[i] == "NA" and (i != 0 or i != len(list_line)-1):
            list_line[i] = str((int(list_line[i-1])+int(list_line[i+1])) // 2)
        elif list_line[i] == "NA" and i == 0:
            list_line[i]= list_line[i+1]
        elif list_line[i] == "NA" and i == len(list_line)-1:
            list_line[i]= list_line[i-1]
        
    lines_2.append(list_line)

with open(f"out_{file_name}", "w") as f:
    for i in range(len(lines_2)):
        for j in range(len(lines_2[i])):
            if int(lines_2[i][j]) < 60 ** 2: # Вариант = 10 (+50)
                continue  
            if j != len(lines_2[i])-1:
                f.write(lines_2[i][j]+",")
            else:
                f.write(lines_2[i][j])
file_name = "text_2_var_10"
sum = 0
list_sum = []
with open(file_name, 'r') as f:
    lines = f.readlines()
    for line in lines:
        digits = line.split(sep="|")
        for num in digits:
            sum += int(num)
        list_sum.append(str(sum))

with open(f"out_{file_name}", "w") as f:
    for line in list_sum:
        f.write(line+"\n")
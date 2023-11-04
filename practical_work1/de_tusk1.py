MARKS = [',', ':', "\n", ".", ";", "!", "\"", "\'", "{", "\\", "/", "}", "[", "]", "*", "?", "^", "(", ")", "-", "_"]
def marks_to_space(input_str: str) -> str:    
    string1 = input_str
    for i in range(len(string1)):
        if string1[i] in MARKS:
            string1 = string1[:i] + ' ' + string1[i+1:]
    string2 = string1
    out_string = ''
    j = 0
    for i in range(len(string2)-1):
        if string2[i] == ' ' and string2[i+1] == ' ':
            out_string += string2[j:i]
            j = i+1
    out_string += string2[j:i+2]
    if out_string[-1] == ' ':
        out_string = out_string[:-1]
    return out_string

line = ""
file_name = "text_1_var_10"

with open(file_name, "r") as f:
    lines = f.readlines()
    line = "".join(lines)

line = marks_to_space(line)
list_ = line.split()
out_dict = {}

for i in range(len(list_)):
    if list_[i] in out_dict:
        out_dict[list_[i]] += 1
    else:
        out_dict[list_[i]] = 1

out_dict = dict(sorted(out_dict.items(), key=lambda item: item[1], reverse=True))

with open(f"out_{file_name}", "w") as f:
    for key, value in out_dict.items():
        f.write(f"{key}: {value}\n")
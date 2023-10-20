from bs4 import BeautifulSoup
import json


file_name = "text_6_var_10"
data = {}
with open(f"{file_name}.json", 'r') as f:
    data = dict(json.load(f))

html_str = "<table>\n    <tr>\n"

for key in data:
    html_str += f"      <td>{key}</td>\n"

html_str += "    </tr>\n    <tr>\n"

for key, value in data.items():
    html_str += f"      <td>{value}</td>\n"

html_str += "    </tr>\n</table>"

with open(f"out_{file_name}", 'w') as f:
    f.write(html_str)
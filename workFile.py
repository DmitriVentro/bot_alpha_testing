import os
import json
import requests
token = "ya29.a0AfH6SMD7d5o2rHPVZGankouZ3qaWMA_SlzI6nRsOY2Nbe602gKheSzEfzDAYZV8ZJVT22-JoE6gaOOcsxzr17kVnOxVt4XTdRniOoXhNBwXxuSqryg-O1FHXtWJYR3ZkV12PXoWB2BZfpJd2j_mUPrxkvqYepEuKltbC"
nInfo = 'absInfo.txt'
g = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/1Nc3gkg-sGfrj84ludywF-eixv4oNoul38lsYq456t-Y/values/A:O?access_token={token}&majorDimension=COLUMNS")
gg = json.loads(g.text)
a = gg['values']
print(a)
for i in a:
    print(i)
with open("type.txt", "w+") as file:
    for i in a:
        f = " ".join(i[1:])
        file.write(f + '\n')



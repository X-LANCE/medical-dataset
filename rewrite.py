import json
import pandas as pd

with open('resource/dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
rewrite_excel = pd.read_excel('resource/医疗数据集改写.xlsx')
for i in range(len(rewrite_excel)):
    assert dataset[i]['id'] == rewrite_excel['ID'][i]
    dataset[i]['question'] = rewrite_excel['改写问句'][i]
with open('resource/dataset_rewrite.json', 'w', encoding='utf-8') as file:
    json.dump(dataset, file, ensure_ascii=False, indent=4)

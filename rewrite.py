import editdistance as edt
import json
import pandas as pd


def get_change_rate(str1, str2):
    return edt.eval(str1, str2) / (len(str1) + len(str2))


with open('resource/dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
rewrite_excel1, rewrite_excel2 = pd.read_excel('resource/医疗数据集改写1.xlsx'), pd.read_excel('resource/医疗数据集改写2.xlsx')
cnt1, cnt2 = 0, 0
for i in range(len(dataset)):
    assert dataset[i]['id'] == rewrite_excel1['ID'][i] == rewrite_excel2['ID'][i]
    q0, q1, q2 = dataset[i]['question'], rewrite_excel1['改写问句'][i], rewrite_excel2['改写问句'][i]
    if get_change_rate(q0, q1) > get_change_rate(q0, q2):
        dataset[i]['question'] = q1
        cnt1 += 1
    else:
        dataset[i]['question'] = q2
        cnt2 += 1
print(f'file1: {round(cnt1 / len(dataset) * 100, 2)}%')
print(f'file2: {round(cnt2 / len(dataset) * 100, 2)}%')
with open('resource/dataset_rewrite.json', 'w', encoding='utf-8') as file:
    json.dump(dataset, file, ensure_ascii=False, indent=4)

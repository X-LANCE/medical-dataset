import json
from openpyxl import Workbook

with open('dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
workbook = Workbook()
worksheet = workbook.active
worksheet.title = '医疗数据集'
worksheet['A1'] = '模板ID'
worksheet['B1'] = '数据库schema'
worksheet['C1'] = 'SQL查询语句'
worksheet['D1'] = '原始问句'
worksheet['E1'] = '改写问句'
for i in range(len(dataset)):
    worksheet[f'A{i + 2}'] = dataset[i]['template']
    worksheet[f'B{i + 2}'] = dataset[i]['schema']
    worksheet[f'C{i + 2}'] = dataset[i]['sql']
    worksheet[f'D{i + 2}'] = dataset[i]['question']
workbook.save('医疗数据集.xlsx')

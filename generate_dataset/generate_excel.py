from openpyxl import Workbook


def generate_excel(dataset):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = '医疗数据集'
    worksheet['A1'] = '模板ID'
    worksheet['B1'] = '数据库schema'
    worksheet['C1'] = 'SQL查询语句'
    worksheet['D1'] = '原始问句'
    worksheet['E1'] = '改写问句'
    for i, example in enumerate(dataset):
        worksheet[f'A{i + 2}'] = example['template']
        worksheet[f'B{i + 2}'] = example['schema']
        worksheet[f'C{i + 2}'] = example['sql']
        worksheet[f'D{i + 2}'] = example['question']
    workbook.save('dataset/医疗数据集.xlsx')

from openpyxl import Workbook


def generate_excel(dataset):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = '医疗数据集'
    worksheet['A1'] = 'ID'
    worksheet['B1'] = '模板ID'
    worksheet['C1'] = '数据库schema'
    worksheet['D1'] = 'SQL查询语句'
    worksheet['E1'] = '原始问句'
    worksheet['F1'] = '改写问句'
    for i, example in enumerate(dataset):
        worksheet[f'A{i + 2}'] = example['id']
        worksheet[f'B{i + 2}'] = example['template']
        worksheet[f'C{i + 2}'] = example['schema']
        worksheet[f'D{i + 2}'] = example['sql']
        worksheet[f'E{i + 2}'] = example['question']
    workbook.save('resource/医疗数据集.xlsx')

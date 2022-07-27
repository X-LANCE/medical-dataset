import json
import os
import pymysql

with open('dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
database = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='yibao')
cursor = database.cursor()
i = 0
while i < len(dataset):
    if dataset[i]['schema'] != '医保表':
        i += 1
        continue
    cursor.execute(dataset[i]['sql'])
    result = cursor.fetchall()
    os.system('cls')
    print(json.dumps(dataset[i], ensure_ascii=False, indent=4))
    print(result)
    command = input()
    i += 1
    if command != '':
        while i < len(dataset) and dataset[i - 1]['template'] == dataset[i]['template']:
            i += 1

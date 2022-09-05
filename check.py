import argparse
import json
import os
from utils import connect_database

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--database', type=str, required=True)
arg_parser.add_argument('--schema', type=str, required=True)
arg_parser.add_argument('--start', default=0, type=int)
args = arg_parser.parse_args()
with open('dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
_, cursor = connect_database(args.database)
i = 0
while i < len(dataset):
    if dataset[i]['template'] < args.start or dataset[i]['schema'] != args.schema:
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

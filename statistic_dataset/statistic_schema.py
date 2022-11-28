import json
import pandas as pd
import sys
from util.constant import SINGLE_DOMAIN_DATASET_NAMES, DATASET_NAMES


def count_schema_complexity(dataset_name):
    print(dataset_name.ljust(12), end='')
    if dataset_name in ['ylsql', 'spider', 'dusql']:
        with open(f'data/{dataset_name}/tables.json', 'r', encoding='utf-8') as file:
            schemata = json.load(file)
        table_nums = [len(schema['table_names']) for schema in schemata]
        print(str(round(sum(table_nums) / len(table_nums), 2)).rjust(12), end='')
        print(str(round(sum([len(schema['column_names']) - 1 for schema in schemata]) / sum(table_nums), 2)).rjust(12), end='')
        print(str(round(sum([len(schema['primary_keys']) for schema in schemata]) / sum(table_nums), 2)).rjust(12), end='')
        print(str(round(sum([len(schema['foreign_keys']) for schema in schemata]) / sum(table_nums), 2)).rjust(12))
    elif dataset_name in SINGLE_DOMAIN_DATASET_NAMES:
        schema = pd.read_csv(f'data/{dataset_name}/tables.csv')
        tables = set(schema['Table Name'])
        if '-' in tables:
            tables.remove('-')
        print(str(len(tables)).rjust(12), end='')
        print(str(round(sum([column != '-' for column in schema['Field Name']]) / len(tables), 2)).rjust(12), end='')
        print(str(round(sum([pk.lower() in ['y', 'pri'] for pk in schema['Is Primary Key']]) / len(tables), 2)).rjust(12), end='')
        print(str(round(sum([fk.lower() in ['y', 'yes'] for fk in schema['Is Foreign Key']]) / len(tables), 2)).rjust(12))
    elif dataset_name == 'wikisql':
        schemata = pd.read_csv('data/wikisql/tables.csv')
        schema_names = set(schemata['Database Name'])
        print('1'.rjust(12), end='')
        print(str(round(len(schemata) / len(schema_names), 2)).rjust(12), end='')
        print(str(round(sum(schemata['Is Primary Key']) / len(schema_names), 2)).rjust(12), end='')
        print(str(round(sum(schemata['Is Foreign Key']) / len(schema_names), 2)).rjust(12))
    else:
        raise ValueError(f'wrong dataset name {dataset_name}')


def statistic_schema():
    with open('log/statistic_schema.txt', 'w') as file:
        sys.stdout, original_stdout = file, sys.stdout
        print(''.rjust(12), end='')
        print('avg t/s'.rjust(12), end='')
        print('avg c/t'.rjust(12), end='')
        print('avg p/t'.rjust(12), end='')
        print('avg f/t'.rjust(12))
        for dataset_name in DATASET_NAMES:
            count_schema_complexity(dataset_name)
        sys.stdout = original_stdout

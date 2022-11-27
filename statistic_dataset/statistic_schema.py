import json
import sys
from util.constant import DATASET_NAMES


def count_schema_complexity(dataset_name):
    print(dataset_name.ljust(12), end='')
    if dataset_name == 'ylsql':
        with open('data/ylsql/tables.json', 'r', encoding='utf-8') as file:
            schemata = json.load(file)
        table_nums = [len(schema['table_names']) for schema in schemata]
        column_nums = [len(schema['column_names']) - 1 for schema in schemata]
        primary_key_nums = [len(schema['primary_keys']) for schema in schemata]
        foreign_key_nums = [len(schema['foreign_keys']) * 2 for schema in schemata]
        print(str(round(sum(table_nums) / len(table_nums), 2)).rjust(12), end='')
        print(str(round(sum(column_nums) / sum(table_nums), 2)).rjust(12), end='')
        print(str(round(sum(primary_key_nums) / sum(table_nums), 2)).rjust(12), end='')
        print(str(round(sum(foreign_key_nums) / sum(table_nums), 2)).rjust(12))
    else:
        print()


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

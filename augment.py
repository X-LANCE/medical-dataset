import json

with open('data/css/tables.json', 'r', encoding='utf-8') as file:
    tables = json.load(file)
if len(tables) == 2:
    with open('data/css/tables_gen.json', 'r', encoding='utf-8') as file:
        tables_gen = json.load(file)
    tables += tables_gen
    with open('data/css/tables.json', 'w', encoding='utf-8') as file:
        json.dump(tables, file, ensure_ascii=False, indent=4)
with open('data/css/db_content.json', 'r', encoding='utf-8') as file:
    db_content = json.load(file)
if len(db_content) == 2:
    for table in tables:
        if table['db_id'] in ['医保表', '医疗表']:
            continue
        empty_tables = {}
        for i, table_name in enumerate(table['table_names']):
            headers, types = [], []
            for j, column_name in enumerate(table['column_names_original']):
                if column_name[0] == i:
                    headers.append(column_name[1])
                    types.append(table['column_types'][j])
            empty_tables[table_name] = {
                'cell': [],
                'header': headers,
                'table_name': table['table_names_original'][i],
                'type': types
            }
        db_content.append({
            'db_id': table['db_id'],
            'tables': empty_tables
        })
    with open('data/css/db_content.json', 'w', encoding='utf-8') as file:
        json.dump(db_content, file, ensure_ascii=False, indent=4)
with open('data/css/all.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
if len(data) == 4340:
    with open('data/css/all_gen.json', 'r', encoding='utf-8') as file:
        data_gen = json.load(file)
    data += data_gen
    for i in range(len(data)):
        data[i]['question_id'] = f'qid{str(i + 1).zfill(5)}'
    with open('data/css/all.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

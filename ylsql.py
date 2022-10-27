import argparse
import json
from util.constant import INSU_TYPE_MAPPING, INSURED_STS_MAPPING, SERVANT_FLG_MAPPING, \
    CLINIC_TYPE_MAPPING, REMOTE_SETTLE_FLG_MAPPING, MED_INV_ITEM_TYPE_MAPPING, \
    SCHEMA_MAPPING, TABLE_MAPPING, COLUMN_MAPPING, TYPE_MAPPING, COLUMNS, PRIMARY_KEYS, FOREIGN_KEYS, \
    SQL_AGGS, SQL_CONDS, SQL_KEYWORDS
from util.util import str_to_number, random_split_array, connect_database, skip_nested


def preprocess_sql(sql):
    is_value = False
    i = 0
    while i < len(sql):
        if sql[i] in [',', '(', ')'] and (not is_value):
            sql = f'{sql[:i]} {sql[i]} {sql[i + 1:]}'
            i += 3
        else:
            if sql[i] == "'":
                is_value = not is_value
            i += 1
    tokens = sql.split()
    while '' in tokens:
        tokens.remove('')
    for i in range(len(tokens)):
        if tokens[i] in SQL_KEYWORDS:
            tokens[i] = tokens[i].lower()
        elif tokens[i] == '=':
            tokens[i] = '=='
        elif tokens[i] == '<>':
            tokens[i] = '!='
        if tokens[i] in SQL_CONDS:
            if 'INSU_TYPE' in tokens[i - 1]:
                tokens[i + 1] = f"'{INSU_TYPE_MAPPING[tokens[i + 1]]}'"
            elif 'INSURED_STS' in tokens[i - 1]:
                tokens[i + 1] = f"'{INSURED_STS_MAPPING[tokens[i + 1]]}'"
            elif 'SERVANT_FLG' in tokens[i - 1]:
                tokens[i + 1] = f"'{SERVANT_FLG_MAPPING[tokens[i + 1]]}'"
            elif 'CLINIC_TYPE' in tokens[i - 1]:
                tokens[i + 1] = f"'{CLINIC_TYPE_MAPPING[tokens[i + 1]]}'"
            elif 'REMOTE_SETTLE_FLG' in tokens[i - 1]:
                tokens[i + 1] = f"'{REMOTE_SETTLE_FLG_MAPPING[tokens[i + 1]]}'"
            elif 'MED_INV_ITEM_TYPE' in tokens[i - 1]:
                tokens[i + 1] = f"'{MED_INV_ITEM_TYPE_MAPPING[tokens[i + 1]]}'"
    return ' '.join(tokens)


def tokenize_sql(sql):
    tokens = []
    i = 0
    while i < len(sql):
        if sql[i] == '(':
            j = i + 1
            while sql[j] == '(':
                j += 1
            if sql[j] == 'select':
                j = skip_nested(sql, i + 1)
                tokens.append(tokenize_sql(sql[i + 1:j - 1]))
                i = j
                continue
        if sql[i] == 'not':
            assert sql[i + 1] in ['in', 'like']
            tokens.append(f'not {sql[i + 1]}')
            i += 2
        else:
            tokens.append(sql[i])
            i += 1
    if 'from' in tokens:
        table_name = tokens[tokens.index('from') + 1]
        for i in range(len(tokens)):
            if isinstance(tokens[i], str) and tokens[i] in COLUMNS:
                tokens[i] = f'{table_name}.{tokens[i]}'
    return tokens


def parse_sql(schema, sql):
    def find_clause(start, end_keywords):
        end = start + 1
        while end < len(sql):
            if isinstance(sql[end], str) and sql[end] in end_keywords:
                break
            end += 1
        return start, end

    if isinstance(sql[1], str) and sql[1] in ['intersect', 'union', 'except']:
        assert len(sql) == 3
        result = parse_sql(schema, sql[0])
        result[sql[1]] = parse_sql(schema, sql[2])
        return result
    result = {
        'select': [],
        'from': None,
        'where': [],
        'groupBy': [],
        'having': [],
        'orderBy': [],
        'limit': None,
        'intersect': None,
        'union': None,
        'except': None
    }
    start, end = find_clause(0, ['from'])
    result['select'] = parse_select(schema, sql[start:end])
    if end == len(sql):
        return result
    start, end = find_clause(end, ['where', 'group', 'order'])
    result['from'] = parse_from(schema, sql[start:end])
    if end == len(sql):
        return result
    if sql[end] == 'where':
        start, end = find_clause(end, ['group', 'order'])
        result['where'] = parse_conds(schema, sql[start + 1:end])
        if end == len(sql):
            return result
    if sql[end] == 'group':
        start, end = find_clause(end, ['order'])
        result['groupBy'], result['having'] = parse_group_by(schema, sql[start:end])
        if end == len(sql):
            return result
    result['orderBy'], result['limit'] = parse_order_by(schema, sql[end:])
    return result


def parse_select(schema, select):
    assert isinstance(select[0], str) and select[0] == 'select'
    result = []
    i = 1
    while i < len(select):
        j = i + 1
        while j < len(select):
            if isinstance(select[j], str) and select[j] == ',':
                break
            j += 1
        result.append(parse_val_unit(schema, select[i:j]))
        i = j + 1
    return result


def parse_from(schema, from_clause):
    assert isinstance(from_clause[0], str) and from_clause[0] == 'from'
    result = {
        'table_units': [],
        'conds': []
    }
    for i in range(1, len(from_clause), 2):
        if isinstance(from_clause[i], str):
            result['table_units'].append(['table_unit', schema['table_ids'][from_clause[i]]])
        else:
            result['table_units'].append(['sql', parse_sql(schema, from_clause[i])])
        if i < len(from_clause) - 1:
            assert isinstance(from_clause[i + 1], str)
            if from_clause[i + 1] == 'on':
                result['conds'] = parse_conds(schema, from_clause[i + 2:])
                break
            if from_clause[i + 1] == 'as':
                break
            assert from_clause[i + 1] == 'join'
    return result


def parse_group_by(schema, group_by):
    assert isinstance(group_by[0], str) and group_by[0] == 'group' and isinstance(group_by[1], str) and group_by[1] == 'by'
    result = []
    for i in range(2, len(group_by), 2):
        result.append(parse_col_unit(schema, [group_by[i]]))
        if i < len(group_by) - 1:
            assert isinstance(group_by[i + 1], str)
            if group_by[i + 1] == 'having':
                return result, parse_conds(schema, group_by[i + 2:])
            assert group_by[i + 1] == ','
    return result, []


def parse_order_by(schema, order_by):
    assert isinstance(order_by[0], str) and order_by[0] == 'order' and isinstance(order_by[1], str) and order_by[1] == 'by'
    result = [[]]
    i = 2
    while i < len(order_by):
        j = i + 1
        while j < len(order_by):
            if isinstance(order_by[j], str) and order_by[j] in [',', 'asc', 'desc']:
                break
            j += 1
        result[0].append(parse_val_unit(schema, order_by[i:j]))
        i = j + 1
        if order_by[j] in ['asc', 'desc']:
            result.insert(0, order_by[j])
            break
    if i < len(order_by):
        assert i == len(order_by) - 2 and isinstance(order_by[i], str) and order_by[i] == 'limit'
        return result, int(order_by[i + 1])
    return result, None


def parse_conds(schema, conds):
    result = []
    i = 0
    while i < len(conds):
        if isinstance(conds[i], str) and conds[i] == '(':
            j = skip_nested(conds, i + 1)
            result.append(parse_conds(schema, conds[i + 1:j - 1]))
        else:
            is_between = False
            j = i + 1
            while j < len(conds):
                if isinstance(conds[j], str):
                    if conds[j] == 'between':
                        is_between = True
                    elif conds[j] == 'and' and is_between:
                        is_between = False
                    elif conds[j] in ['and', 'or']:
                        break
                j += 1
            result.append(parse_cond(schema, conds[i:j]))
        if j < len(conds):
            result.append(conds[j])
        i = j + 1
    return result


def parse_cond(schema, cond):
    def parse_value(value):
        if isinstance(value, list):
            return parse_sql(schema, value)
        if '.' in value and value[value.find('.') + 1:] in COLUMNS:
            return parse_col_unit(schema, [value])[1]
        return value[1:-1] if "'" in value else str_to_number(value)

    for i in range(len(cond)):
        if isinstance(cond[i], str) and cond[i].upper() in SQL_CONDS:
            break
    result = parse_val_unit(schema, cond[:i])
    result.insert(1, SQL_CONDS.index(cond[i].upper()))
    if cond[i] != 'between':
        assert i == len(cond) - 2
        result += [parse_value(cond[i + 1]), None]
    else:
        assert i == len(cond) - 4 and isinstance(cond[i + 2], str) and cond[i + 2] == 'and'
        result += [parse_value(cond[i + 1]), parse_value(cond[i + 3])]
    return result


def parse_val_unit(schema, val_unit):
    result = []
    if isinstance(val_unit[0], str) and val_unit[0].upper() in SQL_AGGS:
        result.append(SQL_AGGS.index(val_unit[0].upper()) + 1)
        assert isinstance(val_unit[1], str) and val_unit[1] == '(' and isinstance(val_unit[-1], str) and val_unit[-1] == ')'
        start = 2
        end = len(val_unit) - 1
    else:
        result.append(0)
        start = 0
        end = len(val_unit)
    assert end - start in [1, 2, 3, 6]
    if end - start < 3:
        result.append([
            0,
            parse_col_unit(schema, val_unit[start:end]),
            None
        ])
    elif end - start == 3:
        result.append([
            [None, '-', '+', '*', '/', None, None, '=='].index(val_unit[start + 1]),
            parse_col_unit(schema, [val_unit[start]]),
            parse_col_unit(schema, [val_unit[end - 1]])
        ])
    else:
        assert isinstance(val_unit[start], str) and val_unit[start] in ['datediff', 'mod']
        assert isinstance(val_unit[start + 1], str) and val_unit[start + 1] == '('
        assert isinstance(val_unit[start + 3], str) and val_unit[start + 3] == ','
        assert isinstance(val_unit[start + 5], str) and val_unit[start + 5] == ')'
        if val_unit[start] == 'datediff':
            result.append([
                5,
                parse_col_unit(schema, [val_unit[start + 2]]),
                parse_col_unit(schema, [val_unit[start + 4]])
            ])
        else:
            result.append([
                6,
                parse_col_unit(schema, [val_unit[start + 2]]),
                str_to_number(val_unit[start + 4])
            ])
    return result


def parse_col_unit(schema, col_unit):
    assert len(col_unit) in [1, 2]
    if len(col_unit) == 1:
        col = col_unit[0]
    else:
        assert isinstance(col_unit[0], str) and col_unit[0] == 'distinct'
        col = col_unit[1]
    if isinstance(col, list):
        return parse_sql(schema, col)
    assert isinstance(col, str)
    return [0, 0 if col == '*' else schema['column_ids'][(col[:col.find('.')], col[col.find('.') + 1:])], len(col_unit) > 1]


def generate_db_content():
    db_content = []
    _, common_cursor = connect_database('information_schema')
    for schema in ['yibao', 'yiliao']:
        tables = {}
        _, cursor = connect_database(schema)
        common_cursor.execute('SELECT table_name FROM tables WHERE table_schema = %s', [schema])
        table_names = [item[0] for item in common_cursor.fetchall()]
        for table_name in table_names:
            cursor.execute(f'SELECT * FROM {table_name}')
            common_cursor.execute('SELECT column_name, data_type FROM columns WHERE table_schema = %s AND table_name = %s', [schema, table_name])
            columns = common_cursor.fetchall()
            tables[TABLE_MAPPING[table_name]] = {
                'cell': [[str(item) for item in record] for record in cursor.fetchall()],
                'header': [column[0] for column in columns],
                'table_name': table_name,
                'type': [TYPE_MAPPING[column[1]] for column in columns]
            }
        db_content.append({
            'db_id': SCHEMA_MAPPING[schema],
            'tables': tables
        })
    with open('data/ylsql/db_content.json', 'w', encoding='utf-8') as file:
        json.dump(db_content, file, ensure_ascii=False, indent=4)


def generate_tables():
    tables = []
    schemata = {}
    _, common_cursor = connect_database('information_schema')
    for schema in ['yibao', 'yiliao']:
        common_cursor.execute('SELECT table_name FROM tables WHERE table_schema = %s', [schema])
        table_names = [item[0] for item in common_cursor.fetchall()]
        column_names = []
        column_types = ['text']
        table_ids = {}
        for i, table_name in enumerate(table_names):
            common_cursor.execute('SELECT column_name, data_type FROM columns WHERE table_schema = %s AND table_name = %s', [schema, table_name])
            columns = common_cursor.fetchall()
            column_names.extend([[i, column[0]] for column in columns])
            column_types.extend([TYPE_MAPPING[column[1]] for column in columns])
            table_ids[table_name] = i
        column_ids = {}
        for i, column_name in enumerate(column_names):
            column_ids[(table_names[column_name[0]], column_name[1])] = i + 1
        tables.append({
            'db_id': SCHEMA_MAPPING[schema],
            'table_names': [TABLE_MAPPING[table_name] for table_name in table_names],
            'column_names': [[-1, '*']] + [[column_name[0], COLUMN_MAPPING[(table_names[column_name[0]], column_name[1])]] for column_name in column_names],
            'table_names_original': table_names,
            'column_names_original': [[-1, '*']] + column_names,
            'column_types': column_types,
            'foreign_keys': [[column_ids[foreign_key[0]], column_ids[foreign_key[1]]] for foreign_key in FOREIGN_KEYS[schema]],
            'primary_keys': [column_ids[primary_key] for primary_key in PRIMARY_KEYS[schema]]
        })
        schemata[SCHEMA_MAPPING[schema]] = {
            'table_ids': table_ids,
            'column_ids': column_ids
        }
    with open('data/ylsql/tables.json', 'w', encoding='utf-8') as file:
        json.dump(tables, file, ensure_ascii=False, indent=4)
    return schemata


def generate_train_or_dev(train_or_dev_set, set_name, schemata):
    result = []
    qid = 1
    for example in train_or_dev_set:
        sql = preprocess_sql(example['sql'])
        result.append({
            'query': sql,
            'db_id': example['schema'],
            'question': example['question'],
            'question_id': f'qid{str(qid).zfill(5)}',
            'sql': parse_sql(schemata[example['schema']], tokenize_sql(sql.split()))
        })
        qid += 1
    with open(f'data/ylsql/{set_name}.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


def generate_train_or_dev_gold(set_name):
    with open(f'data/ylsql/{set_name}.json', 'r', encoding='utf-8') as file:
        train_or_dev_set = json.load(file)
    with open(f'data/ylsql/{set_name}_gold.sql', 'w', encoding='utf-8') as file:
        for example in train_or_dev_set:
            file.write(f"{example['question_id']}\t{example['query']}\t{example['db_id']}\n")


def generate_test(test_set):
    result = []
    for i, example in enumerate(test_set):
        result.append({
            'query': '',
            'db_id': example['schema'],
            'question': example['question'],
            'sql': '',
            'question_id': f'qid{str(i + 1).zfill(5)}'
        })
    with open('data/ylsql/test.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--filename', type=str, required=True)
arg_parser.add_argument('--split', type=str, choices=['example', 'template'], required=True)
args = arg_parser.parse_args()
with open(f'resource/{args.filename}.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
for example in dataset:
    tokens = example['sql'].split()
    for i in range(len(tokens)):
        if '.*' in tokens[i]:
            tokens[i] = '*'
    example['sql'] = ' '.join(tokens)
if args.split == 'example':
    train, dev, test = random_split_array(dataset)
elif args.split == 'template':
    templates = []
    for example in dataset:
        if len(templates) == 0 or example['template'] > templates[-1]:
            templates.append(example['template'])
    train_templates, dev_templates, test_templates = random_split_array(templates)
    train = [example for example in dataset if example['template'] in train_templates]
    dev = [example for example in dataset if example['template'] in dev_templates]
    test = [example for example in dataset if example['template'] in test_templates]
else:
    raise ValueError(f'unknown split method {args.split}')
generate_db_content()
schemata = generate_tables()
generate_train_or_dev(dataset, 'all', schemata)
generate_train_or_dev(train, 'train', schemata)
generate_train_or_dev(dev, 'dev', schemata)
generate_train_or_dev_gold('train')
generate_train_or_dev_gold('dev')
generate_test(test)

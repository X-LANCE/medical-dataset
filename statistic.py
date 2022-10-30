import json
import os
import sys
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTreeYlsql, AbstractSyntaxTreeSpider, AbstractSyntaxTreeDusql
from string import ascii_uppercase
from util.constant import SQL_CONDS
from util.util import skip_nested

SINGLE_DOMAIN_DATASETS = ['atis', 'geoquery', 'restaurants', 'scholar', 'academic', 'yelp', 'imdb', 'advising']
CROSS_DOMAIN_DATASETS = ['spider', 'dusql']
DATASET_NAMES = ['ylsql'] + SINGLE_DOMAIN_DATASETS + CROSS_DOMAIN_DATASETS


def find_keyword(tokens, start, end_keywords):
    end = start + 1
    while end < len(tokens):
        if tokens[end] == '(':
            end = skip_nested(tokens, end + 1)
            continue
        if tokens[end] in end_keywords:
            break
        end += 1
    return start, end


def get_sql_skeleton(sql):
    _, end = find_keyword(sql, 0, ['FROM', 'WHERE', 'GROUP', 'ORDER'])
    assert sql[0] == 'SELECT'
    result = f"SELECT {', '.join(sorted(get_val_units_skeletons(sql[1:end])))} "
    if end == len(sql):
        return result
    if sql[end] == 'FROM':
        start, end = find_keyword(sql, end, ['WHERE', 'GROUP', 'ORDER'])
        result += get_from_skeleton(sql[start:end])
        if end == len(sql):
            return result
    if sql[end] == 'WHERE':
        start, end = find_keyword(sql, end, ['GROUP', 'ORDER'])
        result += f' WHERE {get_conds_skeleton(sql[start + 1:end])}'
        if end == len(sql):
            return result
    if sql[end] == 'GROUP':
        start, end = find_keyword(sql, end, ['ORDER'])
        result += f' {get_group_by_skeleton(sql[start:end])}'
        if end == len(sql):
            return result
    result += f' {get_order_by_skeleton(sql[end:])}'
    return result


def get_from_skeleton(from_clause):
    assert from_clause[0] == 'FROM'
    result = 'FROM '
    i = 1
    while i < len(from_clause):
        if from_clause[i] == '(':
            j = skip_nested(from_clause, i + 1)
            result += f'({get_sql_skeleton(from_clause[i + 1:j - 1])})'
            i = j
        else:
            result += 'tab'
            i += 1
        assert from_clause[i] == 'AS'
        _, i = find_keyword(from_clause, i + 1, [',', 'JOIN'])
        if i < len(from_clause):
            result += ', '
            i += 1
    return result


def get_group_by_skeleton(group_by):
    assert group_by[0] == 'GROUP' and group_by[1] == 'BY'
    result = 'GROUP BY '
    for i in range(2, len(group_by), 2):
        assert '.' in group_by[i]
        result += 'col'
        if i + 1 < len(group_by):
            if group_by[i + 1] == 'HAVING':
                result += f' HAVING {get_conds_skeleton(group_by[i + 2:])}'
                break
            assert group_by[i + 1] == ','
            result += ', '
    return result


def get_order_by_skeleton(order_by):
    assert order_by[0] == 'ORDER' and order_by[1] == 'BY'
    result = 'ORDER BY '
    _, i = find_keyword(order_by, 1, ['ASC', 'DESC', 'LIMIT'])
    if i == len(order_by) or order_by[i] == 'LIMIT':
        order_by.insert(i, 'ASC')
    result += f"{', '.join(get_val_units_skeletons(order_by[2:i]))} {order_by[i]}"
    if i + 1 < len(order_by):
        assert order_by[i + 1] == 'LIMIT'
        result += ' LIMIT value'
    return result


def get_conds_skeleton(conds):
    conds_skeletons = []
    logic_ops = []
    i = 0
    while i < len(conds):
        if conds[i] == 'NOT':
            assert conds[i + 1] == '('
            j = skip_nested(conds, i + 2)
            assert j == len(conds) or conds[j] in ['AND', 'OR']
            conds_skeletons.append(f'NOT ({get_conds_skeleton(conds[i + 2:j - 1])})')
        elif conds[i] == 'EXISTS':
            assert conds[i + 1] == '('
            j = skip_nested(conds, i + 2)
            assert j == len(conds) or conds[j] in ['AND', 'OR']
            conds_skeletons.append(f'EXISTS ({get_sql_skeleton(conds[i + 2:j - 1])})')
        elif conds[i] == '(' and conds[i + 1] != 'SELECT':
            j = skip_nested(conds, i + 1)
            assert j == len(conds) or conds[j] in ['AND', 'OR']
            conds_skeletons.append(f'({get_conds_skeleton(conds[i + 1:j - 1])})')
        else:
            if conds[i] == '(':
                j = skip_nested(conds, i + 1)
                cond_op = conds[j]
                assert cond_op in SQL_CONDS + ['NOT BETWEEN', 'IS', 'IS NOT']
                conds_skeletons.append(f'({get_val_unit_skeleton(conds[i + 1:j - 1])}) {cond_op} ')
            else:
                _, j = find_keyword(conds, i, SQL_CONDS + ['NOT BETWEEN', 'IS', 'IS NOT'])
                cond_op = conds[j]
                conds_skeletons.append(f'{get_val_unit_skeleton(conds[i:j])} {cond_op} ')
            i, j = find_keyword(conds, j, ['AND', 'OR'])
            conds_skeletons[-1] += get_val_unit_skeleton(conds[i + 1:j])
            if cond_op in ['BETWEEN', 'NOT BETWEEN']:
                assert conds[j] == 'AND'
                i, j = find_keyword(conds, j, ['AND', 'OR'])
                conds_skeletons[-1] += f' AND {get_val_unit_skeleton(conds[i + 1:j])}'
        if j < len(conds):
            logic_ops.append(conds[j])
        i = j + 1
    assert len(conds_skeletons) - len(logic_ops) == 1
    if all([logic_op == logic_ops[0] for logic_op in logic_ops[1:]]):
        conds_skeletons.sort()
    result = conds_skeletons[0]
    for i in range(len(logic_ops)):
        result += f' {logic_ops[i]} {conds_skeletons[i + 1]}'
    return result


def get_val_units_skeletons(val_units):
    result = []
    i = 0
    while i < len(val_units):
        _, j = find_keyword(val_units, i, [','])
        result.append(get_val_unit_skeleton(val_units[i:j]))
        i = j + 1
    return result


def get_val_unit_skeleton(val_unit):
    if val_unit[0] in ['ALL', 'DISTINCT']:
        result = f'{val_unit[0]} '
        i = 1
    else:
        result = ''
        i = 0
    if val_unit[i] == '(':
        assert val_unit[-1] == ')'
        if val_unit[i + 1] == 'SELECT':
            result += f'({get_sql_skeleton(val_unit[i + 1:-1])})'
        else:
            result += f"({', '.join(get_val_units_skeletons(val_unit[i + 1:-1]))})"
        return result
    has_agg = False
    if val_unit[i][-1] == '(':
        has_agg = True
        result += val_unit[i]
        i += 1
        if val_unit[i] == 'DISTINCT':
            result += 'DISTINCT '
            i += 1
            if val_unit[i] == '(':
                i += 1
    if val_unit[i] == 'CASE':
        assert val_unit[i + 1] == 'WHEN'
        _, j = find_keyword(val_unit, i + 1, ['THEN'])
        result += f'CASE WHEN {get_conds_skeleton(val_unit[i + 2:j])} THEN '
        i, j = find_keyword(val_unit, j + 1, ['ELSE'])
        result += f'{get_val_unit_skeleton(val_unit[i:j])} ELSE '
        i, j = find_keyword(val_unit, j + 1, ['END'])
        result += f'{get_val_unit_skeleton(val_unit[i:j])} END'
    elif val_unit[i] == 'NULL':
        result += 'NULL'
    elif '.' in val_unit[i] or val_unit[i][0] in ascii_uppercase:
        result += 'col'
    else:
        result += 'value'
    if has_agg:
        result += ')'
    return result


def count_ast(dataset_name):
    def tokenize_sql(sql):
        sql = sql.strip(' ;').replace('=', '==').replace('>==', '>=').replace('<==', '<=').replace('<>', '!=').split()
        i = 0
        while i < len(sql) - 1:
            if (sql[i] == 'NOT' and sql[i + 1] in ['BETWEEN', 'IN', 'LIKE']) or (sql[i] == 'IS' and sql[i + 1] == 'NOT'):
                sql[i] += f' {sql[i + 1]}'
                i += 1
                sql.pop(i)
            else:
                i += 1
        return sql

    with open(f'data/{dataset_name}/all.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    if os.path.exists(f'asdl/grammar/{dataset_name}.txt'):
        grammar = Grammar.from_file(f'asdl/grammar/{dataset_name}.txt')
    if dataset_name == 'ylsql':
        grammar_counter = {}
        for type in grammar.constructors:
            for name in grammar[type]:
                grammar_counter[(type, name)] = 0
    sql_set = set()
    for example in dataset:
        if dataset_name == 'ylsql':
            ast = AbstractSyntaxTreeYlsql.parse_sql(grammar, example['sql'])
            ast.check(grammar)
            ast.count_grammar(grammar_counter)
            sql_set.add(ast.unparse_sql())
        elif dataset_name in SINGLE_DOMAIN_DATASETS:
            for sql in example['sql']:
                sql_set.add(get_sql_skeleton(tokenize_sql(sql)))
        elif dataset_name == 'spider':
            ast = AbstractSyntaxTreeSpider.parse_sql(grammar, example['sql'])
            ast.check(grammar)
            sql_set.add(ast.unparse_sql())
        elif dataset_name == 'dusql':
            ast = AbstractSyntaxTreeDusql.parse_sql(grammar, example['sql'])
            ast.check(grammar)
            sql_set.add(ast.unparse_sql())
        else:
            raise ValueError(f'wrong dataset name {dataset_name}')
    sql_list = sorted(list(sql_set))
    if dataset_name == 'ylsql':
        print('frequencies of grammar rules in ylsql:')
        for item in grammar_counter:
            print(str(grammar_counter[item]).ljust(7), f'{item[0]} = {grammar[item[0]][item[1]]}')
        print()
    print(f'{dataset_name} has {len(sql_set)} different ASTs:')
    for sql in sql_list:
        print(sql)
    print()
    return sql_set


def count_coverage(sql_set1, sql_set2):
    cnt = 0
    for sql in sql_set1:
        cnt += sql in sql_set2
    return round(cnt / len(sql_set1) * 100, 2)


sql_sets = {}
with open('log/log.txt', 'w') as file:
    sys.stdout, original_stdout = file, sys.stdout
    for dataset_name in DATASET_NAMES:
        sql_sets[dataset_name] = count_ast(dataset_name)
    print(''.rjust(12), end='')
    for dataset_name in DATASET_NAMES:
        print(f'{dataset_name}({len(sql_sets[dataset_name])})'.rjust(16), end='')
    print()
    for dataset_name1 in DATASET_NAMES:
        print(dataset_name1.ljust(12), end='')
        for dataset_name2 in DATASET_NAMES:
            if dataset_name1 == dataset_name2:
                print('-'.rjust(16), end='')
            else:
                print(f'{count_coverage(sql_sets[dataset_name1], sql_sets[dataset_name2])}%'.rjust(16), end='')
        print()
    sys.stdout = original_stdout

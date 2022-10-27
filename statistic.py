import json
import os
import sys
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTreeYlsql, AbstractSyntaxTreeSpider, AbstractSyntaxTreeDusql
from util.constant import SQL_AGGS, SQL_CONDS
from util.util import skip_nested

DATASET_NAMES = ['ylsql', 'imdb', 'spider', 'dusql']


def get_sql_skeleton(sql):
    def find_clause(start, end_keywords):
        end = start + 1
        while end < len(sql):
            if sql[end] == '(':
                end = skip_nested(sql, end + 1)
            if sql[end] in end_keywords:
                break
            end += 1
        return start, end

    _, end = find_clause(0, ['FROM'])
    assert sql[0] == 'SELECT'
    result = f"SELECT {', '.join(sorted(get_val_units_skeletons(sql[1:end])))} "
    start, end = find_clause(end, ['WHERE', 'GROUP', 'ORDER'])
    result += get_from_skeleton(sql[start:end])
    if end == len(sql):
        return result
    if sql[end] == 'WHERE':
        start, end = find_clause(end, ['GROUP', 'ORDER'])
        result += f' WHERE {get_conds_skeleton(sql[start + 1:end])}'
        if end == len(sql):
            return result
    if sql[end] == 'GROUP':
        start, end = find_clause(end, ['ORDER'])
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
        i += 2
        if i < len(from_clause):
            assert from_clause[i] == ','
            result += ', '
            i += 1
    return result


def get_group_by_skeleton(group_by):
    return ''


def get_order_by_skeleton(order_by):
    return ''


def get_conds_skeleton(conds):
    result = []
    logic_op = None
    i = 0
    while i < len(conds):
        j = i + 1
        while j < len(conds) and conds[j] not in SQL_CONDS:
            j += 1
        cond_op = conds[j]
        result.append(f'{get_val_unit_skeleton(conds[i:j])} {cond_op} ')
        i = j = j + 1
        while j < len(conds) and conds[j] not in ['AND', 'OR']:
            j += 1
        result[-1] += get_val_unit_skeleton(conds[i:j])
        if cond_op == 'BETWEEN':
            assert conds[j] == 'AND'
            i = j = j + 1
            while j < len(conds) and conds[j] not in ['AND', 'OR']:
                j += 1
            result[-1] += f' AND {get_val_unit_skeleton(conds[i:j])}'
        if j < len(conds):
            logic_op = conds[j]
        i = j + 1
    result.sort()
    return f' {logic_op} '.join(result)


def get_val_units_skeletons(val_units):
    result = []
    i = 0
    while i < len(val_units):
        j = i + 1
        while j < len(val_units) and val_units[j] != ',':
            j += 1
        result.append(get_val_unit_skeleton(val_units[i:j]))
        i = j + 1
    return result


def get_val_unit_skeleton(val_unit):
    if val_unit[0][-1] == '(':
        assert val_unit[0][:-1] in SQL_AGGS
        result = val_unit[0]
        redundant_nested = False
        i = 1
        if val_unit[i] == 'DISTINCT':
            result += 'DISTINCT '
            i += 1
            if val_unit[i] == '(':
                redundant_nested = True
                i += 1
        assert '.' in val_unit[i]
        result += 'col)'
        i += 1
        if redundant_nested:
            assert val_unit[i] == ')'
            i += 1
        assert val_unit[i] == ')'
    else:
        result = 'col' if '.' in val_unit[0] else 'value'
    return result


def count_ast(dataset_name):
    def tokenize_sql(sql):
        return sql.strip(' ;').replace('=', '==').split()

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
        elif dataset_name == 'imdb':
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
    for dataset_name in [''] + DATASET_NAMES:
        print(dataset_name.rjust(8), end='')
    print()
    for dataset_name1 in DATASET_NAMES:
        print(dataset_name1.ljust(8), end='')
        for dataset_name2 in DATASET_NAMES:
            if dataset_name1 == dataset_name2:
                print('-'.rjust(8), end='')
            else:
                print(f'{count_coverage(sql_sets[dataset_name1], sql_sets[dataset_name2])}%'.rjust(8), end='')
        print()
    sys.stdout = original_stdout

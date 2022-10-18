import json
import sys
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTreeYlsql, AbstractSyntaxTreeSpider, AbstractSyntaxTreeDusql


def count_ast(dataset_name):
    with open(f'data/{dataset_name}/all.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    grammar = Grammar.from_file(f'asdl/grammar/{dataset_name}.txt')
    grammar_counter = {}
    for type in grammar.constructors:
        for name in grammar[type]:
            grammar_counter[(type, name)] = 0
    sql_set = set()
    for example in dataset:
        if dataset_name == 'ylsql':
            ast = AbstractSyntaxTreeYlsql.parse_sql(grammar, example['sql'])
        elif dataset_name == 'spider':
            ast = AbstractSyntaxTreeSpider.parse_sql(grammar, example['sql'])
        elif dataset_name == 'dusql':
            ast = AbstractSyntaxTreeDusql.parse_sql(grammar, example['sql'])
        else:
            raise ValueError(f'wrong dataset name {dataset_name}')
        ast.check(grammar)
        ast.count_grammar(grammar_counter)
        sql_set.add(ast.unparse_sql())
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


with open('log/log.txt', 'w') as file:
    sys.stdout, original_stdout = file, sys.stdout
    ylsql_sql_set = count_ast('ylsql')
    spider_sql_set = count_ast('spider')
    dusql_sql_set = count_ast('dusql')
    print(f'{count_coverage(ylsql_sql_set, spider_sql_set)}% ylsql ASTs appear in spider')
    print(f'{count_coverage(ylsql_sql_set, dusql_sql_set)}% ylsql ASTs appear in dusql')
    print(f'{count_coverage(spider_sql_set, ylsql_sql_set)}% spider ASTs appear in ylsql')
    print(f'{count_coverage(dusql_sql_set, ylsql_sql_set)}% dusql ASTs appear in ylsql')
    sys.stdout = original_stdout

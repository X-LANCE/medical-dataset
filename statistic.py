import json
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTreeYlsql, AbstractSyntaxTreeSpider


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
        else:
            raise ValueError(f'wrong dataset name {dataset_name}')
        ast.check(grammar)
        ast.count_grammar(grammar_counter)
        sql = ast.unparse_sql()
        sql_set.add(sql)
    if dataset_name == 'ylsql':
        print('frequencies of grammar rules in ylsql:')
        for item in grammar_counter:
            print(grammar_counter[item], f'{item[0]} = {grammar[item[0]][item[1]]}', sep='\t')
    return sql_set


ylsql_sql_set = count_ast('ylsql')
spider_sql_set = count_ast('spider')
print(f'ylsql has {len(ylsql_sql_set)} different ASTs')
print(f'spider has {len(spider_sql_set)} different ASTs')
cnt = 0
for sql in ylsql_sql_set:
    cnt += sql in spider_sql_set
print(f'{round(cnt / len(ylsql_sql_set) * 100, 2)}% ylsql ASTs appear in spider')
cnt = 0
for sql in spider_sql_set:
    cnt += sql in ylsql_sql_set
print(f'{round(cnt / len(spider_sql_set) * 100, 2)}% spider ASTs appear in ylsql')

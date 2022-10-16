import json
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTree

with open('data/ylsql/all.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
grammar = Grammar.from_file('asdl/grammar/grammar.txt')
grammar_count = {}
for type in grammar.constructors:
    for name in grammar[type]:
        grammar_count[(type, name)] = 0
sql_count_dict = {}
for example in dataset:
    ast = AbstractSyntaxTree.parse_sql(grammar, example['sql'])
    ast.check(grammar)
    ast.count_grammar(grammar_count)
    sql = ast.unparse_sql()
    sql_count_dict[sql] = sql_count_dict.get(sql, 0) + 1
sql_count_list = list(zip(sql_count_dict.values(), sql_count_dict.keys()))
sql_count_list.sort(key=lambda x: x[0], reverse=True)
for item in grammar_count:
    print(grammar_count[item], f'{item[0]} = {grammar[item[0]][item[1]]}', sep='\t')
for item in sql_count_list:
    print(item[0], item[1], sep='\t')

import json
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTree

with open('ylsql/all.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
grammar = Grammar.from_file('asdl/grammar/grammar.txt')
sql_count_dict = {}
for example in dataset:
    ast = AbstractSyntaxTree.parse_sql(grammar, example['sql'])
    ast.check(grammar)
    sql = ast.unparse_sql()
    sql_count_dict[sql] = sql_count_dict.get(sql, 0) + 1
sql_count_list = list(zip(sql_count_dict.values(), sql_count_dict.keys()))
sql_count_list.sort(key=lambda x: x[0], reverse=True)
for item in sql_count_list:
    print(item[0], item[1], sep='\t')
while 1:
    sql = input()
    print(sql_count_dict.get(sql, 0))

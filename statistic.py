import json
from asdl.asdl import Grammar
from asdl.ast import AbstractSyntaxTree

with open('ylsql/all.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)
grammar = Grammar.from_file('asdl/grammar/grammar.txt')
ast_count = {}
for example in dataset:
    ast = AbstractSyntaxTree.parse_sql(grammar, example['sql'])
    ast_count[ast] = ast_count.get(ast, 0) + 1
ast_count = list(zip(ast_count.keys(), ast_count.values()))
ast_count.sort(key=lambda x: x[1], reverse=True)
for item in ast_count:
    print(item[0], item[1])

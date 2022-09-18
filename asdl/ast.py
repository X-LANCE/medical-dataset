import num2word
from asdl.asdl import Constructor


class AbstractSyntaxTree:
    def __init__(self, type):
        self.type = type
        self.sons = []
        self.constructor: Constructor

    def __eq__(self, ast):
        if not (isinstance(ast, AbstractSyntaxTree) and self.type == ast.type and self.constructor == ast.constructor):
            return False
        for i in range(len(self.sons)):
            if self.sons[i] != ast.sons[i]:
                return False
        return True

    def __hash__(self):
        result = hash(self.type) ^ hash(self.constructor)
        for son in self.sons:
            result ^= hash(son)
        return result

    @staticmethod
    def parse_sql(grammar, sql):
        ast = AbstractSyntaxTree('sql')
        for sql_keyword in ['intersect', 'union', 'except']:
            if sql[sql_keyword]:
                ast.constructor = grammar['sql'][sql_keyword.title()]
                ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql))
                ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql[sql_keyword]))
                return ast
        ast.constructor = grammar['sql']['Single']
        ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql))
        return ast

    @staticmethod
    def parse_sql_unit(grammar, sql_unit):
        ast = AbstractSyntaxTree('sql_unit')
        ast.sons.append(AbstractSyntaxTree.parse_select(grammar, sql_unit['select']))
        ast.sons.append(AbstractSyntaxTree.parse_from(grammar, sql_unit['from']['table_units']))
        if sql_unit['where'] and sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['Complete']
            ast.sons.append(AbstractSyntaxTree.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTree.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTree.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoWhere']
            ast.sons.append(AbstractSyntaxTree.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTree.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoGroupBy']
            ast.sons.append(AbstractSyntaxTree.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTree.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['NoOrderBy']
            ast.sons.append(AbstractSyntaxTree.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTree.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['where']:
            ast.constructor = grammar['sql_unit']['OnlyWhere']
            ast.sons.append(AbstractSyntaxTree.parse_cond(grammar, sql_unit['where']))
            return ast
        if sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['OnlyGroupBy']
            ast.sons.append(AbstractSyntaxTree.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['OnlyOrderBy']
            ast.sons.append(AbstractSyntaxTree.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        ast.constructor = grammar['sql_unit']['Simple']
        return ast

    @staticmethod
    def parse_select(grammar, select):
        ast = AbstractSyntaxTree('select')
        ast.constructor = grammar['select'][f'Select{num2word.word(len(select))}']
        for val_unit in select:
            ast.sons.append(AbstractSyntaxTree.parse_val_unit(grammar, val_unit))
        return ast

    @staticmethod
    def parse_from(grammar, table_units):
        ast = AbstractSyntaxTree('from')
        if table_units[0][0] == 'sql':
            ast.constructor = grammar['from']['FromSQL']
            ast.sons.append(AbstractSyntaxTree.parse_sql(table_units[0][1]))
        else:
            ast.constructor = grammar['from'][f'From{num2word.word(len(table_units))}Table']
        return ast

    @staticmethod
    def parse_group_by(grammar, group_by, having):
        ast = AbstractSyntaxTree('group_by')
        ast.constructor = grammar['group_by'][f"{num2word.word(len(group_by))}{'' if having else 'No'}Having"]
        for col_unit in group_by:
            ast.sons.append(AbstractSyntaxTree.parse_col_unit(grammar, col_unit))
        if having:
            ast.sons.append(AbstractSyntaxTree.parse_cond(grammar, having))
        return ast

    @staticmethod
    def parse_order_by(grammar, order_by, limit):
        ast = AbstractSyntaxTree('order_by')
        ast.constructor = grammar['order_by'][f"{num2word.word(len(order_by[1]))}{order_by[0].title()}{'Limit' if limit else ''}"]
        for val_unit in order_by[1]:
            ast.sons.append(AbstractSyntaxTree.parse_val_unit(grammar, val_unit))
        return ast

    @staticmethod
    def parse_cond(grammar, cond):
        pass

    @staticmethod
    def parse_val_unit(grammar, val_unit):
        ast = AbstractSyntaxTree('val_unit')
        if val_unit[0] > 0:
            val_unit[1][1][0] = val_unit[0]
        val_unit = val_unit[1]
        ast.sons.append(AbstractSyntaxTree.parse_col_unit(grammar, val_unit[1]))
        if val_unit[0] == 0:
            ast.constructor = grammar['val_unit']['Unary']
            return ast
        ast.sons.append(AbstractSyntaxTree.parse_col_unit(grammar, val_unit[2]))
        if val_unit[0] == 1:
            ast.constructor = grammar['val_unit']['Minus']
        elif val_unit[0] == 2:
            ast.constructor = grammar['val_unit']['Plus']
        elif val_unit[0] == 3:
            ast.constructor = grammar['val_unit']['Times']
        elif val_unit[0] == 4:
            ast.constructor = grammar['val_unit']['Divide']
        else:
            raise ValueError(f'unknown operator {val_unit[0]}')
        return ast

    @staticmethod
    def parse_col_unit(grammar, col_unit):
        ast = AbstractSyntaxTree('col_unit')
        if col_unit[0] == 0:
            ast.constructor = grammar['col_unit']['None']
        elif col_unit[0] == 1:
            ast.constructor = grammar['col_unit']['Max']
        elif col_unit[0] == 2:
            ast.constructor = grammar['col_unit']['Min']
        elif col_unit[0] == 3:
            ast.constructor = grammar['col_unit']['CountDistinct'] if col_unit[2] else grammar['col_unit']['Count']
        elif col_unit[0] == 4:
            ast.constructor = grammar['col_unit']['Sum']
        elif col_unit[0] == 5:
            ast.constructor = grammar['col_unit']['Avg']
        else:
            raise ValueError(f'unknown aggregate function {col_unit[0]}')
        return ast

    def check(self, grammar):
        i = 0
        for field in self.constructor.fields:
            if field in grammar.constructors:
                assert self.sons[i].type == field
                self.sons[i].check(grammar)
                i += 1

import num2word
from asdl.asdl import Constructor


class AbstractSyntaxTree:
    def __init__(self, type):
        self.type = type
        self.sons = []
        self.constructor: Constructor

    def check(self, grammar):
        i = 0
        for field in self.constructor.fields:
            if field in grammar.constructors:
                assert self.sons[i].type == field
                self.sons[i].check(grammar)
                i += 1

    def count_grammar(self, counter):
        counter[(self.type, self.constructor.name)] += 1
        for son in self.sons:
            son.count_grammar(counter)

    def unparse_sql(self):
        assert self.type == 'sql'
        sql_unit0 = self.sons[0].unparse_sql_unit()
        if self.constructor.name == 'Single':
            return sql_unit0
        sql_unit1 = self.sons[1].unparse_sql_unit()
        return f'({sql_unit0}) {self.constructor.name.upper()} ({sql_unit1})'

    def unparse_sql_unit(self):
        assert self.type == 'sql_unit'
        select = self.sons[0].unparse_select()
        if self.constructor.name == 'Complete':
            from_clause = self.sons[1].unparse_from()
            cond = self.sons[2].unparse_cond()
            if cond[0] == '(' and cond[-1] == ')':
                cond = cond[1:-1]
            group_by = self.sons[3].unparse_group_by()
            order_by = self.sons[4].unparse_order_by()
            return f'{select} {from_clause} WHERE {cond} {group_by} {order_by}'
        if self.constructor.name == 'NoWhere':
            from_clause = self.sons[1].unparse_from()
            group_by = self.sons[2].unparse_group_by()
            order_by = self.sons[3].unparse_order_by()
            return f'{select} {from_clause} {group_by} {order_by}'
        if self.constructor.name == 'NoGroupBy':
            from_clause = self.sons[1].unparse_from()
            cond = self.sons[2].unparse_cond()
            if cond[0] == '(' and cond[-1] == ')':
                cond = cond[1:-1]
            order_by = self.sons[3].unparse_order_by()
            return f'{select} {from_clause} WHERE {cond} {order_by}'
        if self.constructor.name == 'NoOrderBy':
            from_clause = self.sons[1].unparse_from()
            cond = self.sons[2].unparse_cond()
            if cond[0] == '(' and cond[-1] == ')':
                cond = cond[1:-1]
            group_by = self.sons[3].unparse_group_by()
            return f'{select} {from_clause} WHERE {cond} {group_by}'
        if self.constructor.name == 'OnlyWhere':
            from_clause = self.sons[1].unparse_from()
            cond = self.sons[2].unparse_cond()
            if cond[0] == '(' and cond[-1] == ')':
                cond = cond[1:-1]
            return f'{select} {from_clause} WHERE {cond}'
        if self.constructor.name == 'OnlyGroupBy':
            from_clause = self.sons[1].unparse_from()
            group_by = self.sons[2].unparse_group_by()
            return f'{select} {from_clause} {group_by}'
        if self.constructor.name == 'OnlyOrderBy':
            from_clause = self.sons[1].unparse_from()
            order_by = self.sons[2].unparse_order_by()
            return f'{select} {from_clause} {order_by}'
        if self.constructor.name == 'Simple':
            from_clause = self.sons[1].unparse_from()
            return f'{select} {from_clause}'
        return select

    def unparse_select(self):
        assert self.type == 'select'
        val_units = []
        for son in self.sons:
            val_units.append(son.unparse_val_unit())
        return f"SELECT {', '.join(val_units)}"

    def unparse_from(self):
        assert self.type == 'from'
        if self.constructor.name == 'FromSQL':
            return f'FROM ({self.sons[0].unparse_sql()})'
        return f"FROM {', '.join(['tab'] * len(self.constructor.fields))}"

    def unparse_group_by(self):
        assert self.type == 'group_by'
        col_units = []
        for i, field in enumerate(self.constructor.fields):
            if field == 'col_unit':
                col_units.append(self.sons[i].unparse_col_unit())
            else:
                having = self.sons[i].unparse_cond()
                if having[0] == '(' and having[-1] == ')':
                    having = having[1:-1]
                return f"GROUP BY {', '.join(col_units)} HAVING {having}"
        return f"GROUP BY {', '.join(col_units)}"

    def unparse_order_by(self):
        assert self.type == 'order_by'
        val_units = []
        for son in self.sons:
            val_units.append(son.unparse_val_unit())
        return f"ORDER BY {', '.join(val_units)} {'ASC' if 'Asc' in self.constructor.name else 'DESC'}{' LIMIT value' if 'Limit' in self.constructor.name else ''}"

    def unparse_cond(self):
        assert self.type == 'cond'
        if self.constructor.name[:3] == 'And':
            cond_op = ' AND '
        elif self.constructor.name[:2] == 'Or':
            cond_op = ' OR '
        else:
            cond_op = None
        if cond_op:
            conds = []
            for son in self.sons:
                conds.append(son.unparse_cond())
            return f'({cond_op.join(conds)})'
        val_unit = self.sons[0].unparse_val_unit()
        if self.constructor.name == 'Between':
            return f'{val_unit} BETWEEN value AND value'
        if self.constructor.name == 'Eq':
            return f'{val_unit} == value'
        if self.constructor.name == 'Gt':
            return f'{val_unit} > value'
        if self.constructor.name == 'Lt':
            return f'{val_unit} < value'
        if self.constructor.name == 'Ge':
            return f'{val_unit} >= value'
        if self.constructor.name == 'Le':
            return f'{val_unit} <= value'
        if self.constructor.name == 'Neq':
            return f'{val_unit} != value'
        if self.constructor.name == 'Like':
            return f'{val_unit} LIKE value'
        if self.constructor.name == 'NotLike':
            return f'{val_unit} NOT LIKE value'
        sql = self.sons[1].unparse_sql()
        if self.constructor.name == 'BetweenSQL':
            return f'{val_unit} BETWEEN ({sql}) AND value'
        if self.constructor.name == 'EqSQL':
            return f'{val_unit} == ({sql})'
        if self.constructor.name == 'GtSQL':
            return f'{val_unit} > ({sql})'
        if self.constructor.name == 'LtSQL':
            return f'{val_unit} < ({sql})'
        if self.constructor.name == 'GeSQL':
            return f'{val_unit} >= ({sql})'
        if self.constructor.name == 'LeSQL':
            return f'{val_unit} <= ({sql})'
        if self.constructor.name == 'NeqSQL':
            return f'{val_unit} != ({sql})'
        if self.constructor.name == 'InSQL':
            return f'{val_unit} IN ({sql})'
        if self.constructor.name == 'NotInSQL':
            return f'{val_unit} NOT IN ({sql})'

    def unparse_val_unit(self):
        assert self.type == 'val_unit'
        col_unit0 = self.sons[0].unparse_col_unit()
        if self.constructor.name == 'Unary':
            return col_unit0
        if self.constructor.name == 'Mod':
            return f'MOD({col_unit0}, value)'
        col_unit1 = self.sons[1].unparse_col_unit()
        if self.constructor.name == 'Minus':
            return f'{col_unit0} - {col_unit1}'
        if self.constructor.name == 'Plus':
            return f'{col_unit0} + {col_unit1}'
        if self.constructor.name == 'Times':
            return f'{col_unit0} * {col_unit1}'
        if self.constructor.name == 'Divide':
            return f'{col_unit0} / {col_unit1}'
        if self.constructor.name == 'DateDiff':
            return f'DATEDIFF({col_unit0}, {col_unit1})'
        if self.constructor.name == 'Equal':
            return f'{col_unit0} == {col_unit1}'

    def unparse_col_unit(self):
        assert self.type == 'col_unit'
        if self.constructor.name == 'None':
            return 'col'
        if self.constructor.name == 'Distinct':
            return 'DISTINCT col'
        if self.constructor.name == 'CountDistinct':
            return 'COUNT(DISTINCT col)'
        if self.constructor.name == 'SQL':
            return f'({self.sons[0].unparse_sql_unit()})'
        return f'{self.constructor.name.upper()}(col)'


class AbstractSyntaxTreeYlsql(AbstractSyntaxTree):
    def __init__(self, type):
        super().__init__(type)

    @staticmethod
    def parse_sql(grammar, sql):
        ast = AbstractSyntaxTreeYlsql('sql')
        for sql_keyword in ['intersect', 'union', 'except']:
            if sql[sql_keyword]:
                ast.constructor = grammar['sql'][sql_keyword.title()]
                ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql_unit(grammar, sql))
                ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql_unit(grammar, sql[sql_keyword]))
                return ast
        ast.constructor = grammar['sql']['Single']
        ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql_unit(grammar, sql))
        return ast

    @staticmethod
    def parse_sql_unit(grammar, sql_unit):
        ast = AbstractSyntaxTreeYlsql('sql_unit')
        ast.sons.append(AbstractSyntaxTreeYlsql.parse_select(grammar, sql_unit['select']))
        if sql_unit['where'] and sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['Complete']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoWhere']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoGroupBy']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['NoOrderBy']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['where']:
            ast.constructor = grammar['sql_unit']['OnlyWhere']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, sql_unit['where']))
            return ast
        if sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['OnlyGroupBy']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['OnlyOrderBy']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['from']:
            ast.constructor = grammar['sql_unit']['Simple']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_from(grammar, sql_unit['from']['table_units']))
            return ast
        ast.constructor = grammar['sql_unit']['VerySimple']
        return ast

    @staticmethod
    def parse_select(grammar, select):
        ast = AbstractSyntaxTreeYlsql('select')
        ast.constructor = grammar['select'][f'Select{num2word.word(len(select))}']
        for val_unit in select:
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_val_unit(grammar, val_unit))
        return ast

    @staticmethod
    def parse_from(grammar, table_units):
        ast = AbstractSyntaxTreeYlsql('from')
        if table_units[0][0] == 'sql':
            ast.constructor = grammar['from']['FromSQL']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql(grammar, table_units[0][1]))
        else:
            ast.constructor = grammar['from'][f'From{num2word.word(len(table_units))}Table']
        return ast

    @staticmethod
    def parse_group_by(grammar, group_by, having):
        ast = AbstractSyntaxTreeYlsql('group_by')
        ast.constructor = grammar['group_by'][f"{num2word.word(len(group_by))}{'' if having else 'No'}Having"]
        for col_unit in group_by:
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_col_unit(grammar, col_unit))
        if having:
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, having))
        return ast

    @staticmethod
    def parse_order_by(grammar, order_by, limit):
        ast = AbstractSyntaxTreeYlsql('order_by')
        ast.constructor = grammar['order_by'][f"{num2word.word(len(order_by[1]))}{order_by[0].title()}{'Limit' if limit else ''}"]
        for val_unit in order_by[1]:
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_val_unit(grammar, val_unit))
        return ast

    @staticmethod
    def parse_cond(grammar, cond):
        ast = AbstractSyntaxTreeYlsql('cond')
        if len(cond) == 1:
            cond = cond[0]
        elif cond[1] in ['and', 'or']:
            ast.constructor = grammar['cond'][f'{cond[1].title()}{num2word.word((len(cond) + 1) // 2)}']
            for i in range(0, len(cond), 2):
                ast.sons.append(AbstractSyntaxTreeYlsql.parse_cond(grammar, cond[i]))
            return ast
        ast.sons.append(AbstractSyntaxTreeYlsql.parse_val_unit(grammar, [cond[0], cond[2]]))
        is_sql = 'SQL' if isinstance(cond[3], dict) else ''
        if cond[1] == 0:
            ast.constructor = grammar['cond'][f'NotIn{is_sql}']
        elif cond[1] == 1:
            ast.constructor = grammar['cond'][f'Between{is_sql}']
        elif cond[1] == 2:
            ast.constructor = grammar['cond'][f'Eq{is_sql}']
        elif cond[1] == 3:
            ast.constructor = grammar['cond'][f'Gt{is_sql}']
        elif cond[1] == 4:
            ast.constructor = grammar['cond'][f'Lt{is_sql}']
        elif cond[1] == 5:
            ast.constructor = grammar['cond'][f'Ge{is_sql}']
        elif cond[1] == 6:
            ast.constructor = grammar['cond'][f'Le{is_sql}']
        elif cond[1] == 7:
            ast.constructor = grammar['cond'][f'Neq{is_sql}']
        elif cond[1] == 8:
            ast.constructor = grammar['cond'][f'In{is_sql}']
        elif cond[1] == 9:
            ast.constructor = grammar['cond'][f'Like{is_sql}']
        elif cond[1] == 10:
            ast.constructor = grammar['cond'][f'NotLike{is_sql}']
        else:
            raise ValueError(f'unknown conditional operator {cond[1]}')
        if is_sql:
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql(grammar, cond[3]))
        return ast

    @staticmethod
    def parse_val_unit(grammar, val_unit):
        ast = AbstractSyntaxTreeYlsql('val_unit')
        if val_unit[0] > 0:
            val_unit[1][1][0] = val_unit[0]
        val_unit = val_unit[1]
        ast.sons.append(AbstractSyntaxTreeYlsql.parse_col_unit(grammar, val_unit[1]))
        if val_unit[0] == 0:
            ast.constructor = grammar['val_unit']['Unary']
            return ast
        if val_unit[0] == 6:
            ast.constructor = grammar['val_unit']['Mod']
            return ast
        ast.sons.append(AbstractSyntaxTreeYlsql.parse_col_unit(grammar, val_unit[2]))
        if val_unit[0] == 1:
            ast.constructor = grammar['val_unit']['Minus']
        elif val_unit[0] == 2:
            ast.constructor = grammar['val_unit']['Plus']
        elif val_unit[0] == 3:
            ast.constructor = grammar['val_unit']['Times']
        elif val_unit[0] == 4:
            ast.constructor = grammar['val_unit']['Divide']
        elif val_unit[0] == 5:
            ast.constructor = grammar['val_unit']['DateDiff']
        elif val_unit[0] == 7:
            ast.constructor = grammar['val_unit']['Equal']
        else:
            raise ValueError(f'unknown operator {val_unit[0]}')
        return ast

    @staticmethod
    def parse_col_unit(grammar, col_unit):
        ast = AbstractSyntaxTreeYlsql('col_unit')
        if isinstance(col_unit, dict):
            ast.constructor = grammar['col_unit']['SQL']
            ast.sons.append(AbstractSyntaxTreeYlsql.parse_sql_unit(grammar, col_unit))
            return ast
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


class AbstractSyntaxTreeSpider(AbstractSyntaxTree):
    def __init__(self, type):
        super().__init__(type)

    @staticmethod
    def parse_sql(grammar, sql):
        ast = AbstractSyntaxTreeSpider('sql')
        for sql_keyword in ['intersect', 'union', 'except']:
            if sql[sql_keyword]:
                ast.constructor = grammar['sql'][sql_keyword.title()]
                ast.sons.append(AbstractSyntaxTreeSpider.parse_sql_unit(grammar, sql))
                ast.sons.append(AbstractSyntaxTreeSpider.parse_sql_unit(grammar, sql[sql_keyword]))
                return ast
        ast.constructor = grammar['sql']['Single']
        ast.sons.append(AbstractSyntaxTreeSpider.parse_sql_unit(grammar, sql))
        return ast

    @staticmethod
    def parse_sql_unit(grammar, sql_unit):
        ast = AbstractSyntaxTreeSpider('sql_unit')
        ast.sons.append(AbstractSyntaxTreeSpider.parse_select(grammar, sql_unit['select']))
        ast.sons.append(AbstractSyntaxTreeSpider.parse_from(grammar, sql_unit['from']['table_units']))
        if sql_unit['where'] and sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['Complete']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeSpider.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTreeSpider.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['groupBy'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoWhere']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            ast.sons.append(AbstractSyntaxTreeSpider.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['NoGroupBy']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeSpider.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        if sql_unit['where'] and sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['NoOrderBy']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, sql_unit['where']))
            ast.sons.append(AbstractSyntaxTreeSpider.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['where']:
            ast.constructor = grammar['sql_unit']['OnlyWhere']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, sql_unit['where']))
            return ast
        if sql_unit['groupBy']:
            ast.constructor = grammar['sql_unit']['OnlyGroupBy']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_group_by(grammar, sql_unit['groupBy'], sql_unit['having']))
            return ast
        if sql_unit['orderBy']:
            ast.constructor = grammar['sql_unit']['OnlyOrderBy']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_order_by(grammar, sql_unit['orderBy'], sql_unit['limit']))
            return ast
        ast.constructor = grammar['sql_unit']['Simple']
        return ast

    @staticmethod
    def parse_select(grammar, select):
        ast = AbstractSyntaxTreeSpider('select')
        ast.constructor = grammar['select'][f'Select{num2word.word(len(select[1]))}']
        for val_unit in select[1]:
            ast.sons.append(AbstractSyntaxTreeSpider.parse_val_unit(grammar, val_unit, select[0]))
        return ast

    @staticmethod
    def parse_from(grammar, table_units):
        ast = AbstractSyntaxTreeSpider('from')
        if table_units[0][0] == 'sql':
            ast.constructor = grammar['from']['FromSQL']
            ast.sons.append(AbstractSyntaxTreeSpider.parse_sql(grammar, table_units[0][1]))
        else:
            ast.constructor = grammar['from'][f'From{num2word.word(len(table_units))}Table']
        return ast

    @staticmethod
    def parse_group_by(grammar, group_by, having):
        ast = AbstractSyntaxTreeSpider('group_by')
        ast.constructor = grammar['group_by'][f"{num2word.word(len(group_by))}{'' if having else 'No'}Having"]
        for col_unit in group_by:
            ast.sons.append(AbstractSyntaxTreeSpider.parse_col_unit(grammar, col_unit))
        if having:
            ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, having))
        return ast

    @staticmethod
    def parse_order_by(grammar, order_by, limit):
        ast = AbstractSyntaxTreeSpider('order_by')
        ast.constructor = grammar['order_by'][f"{num2word.word(len(order_by[1]))}{order_by[0].title()}{'Limit' if limit else ''}"]
        for val_unit in order_by[1]:
            ast.sons.append(AbstractSyntaxTreeSpider.parse_val_unit(grammar, [0, val_unit]))
        return ast

    @staticmethod
    def parse_cond(grammar, cond):
        ast = AbstractSyntaxTreeSpider('cond')
        if len(cond) == 1:
            cond = cond[0]
        elif cond[1] in ['and', 'or']:
            ast.constructor = grammar['cond'][cond[1].title()]
            for i in range(0, len(cond), 2):
                ast.sons.append(AbstractSyntaxTreeSpider.parse_cond(grammar, cond[i]))
            return ast
        ast.sons.append(AbstractSyntaxTreeSpider.parse_val_unit(grammar, [0, cond[2]]))
        is_not = 'Not' if cond[0] else ''
        is_sql = 'SQL' if isinstance(cond[3], dict) else ''
        if cond[1] == 1:
            ast.constructor = grammar['cond'][f'Between{is_sql}']
        elif cond[1] == 2:
            ast.constructor = grammar['cond'][f'Eq{is_sql}']
        elif cond[1] == 3:
            ast.constructor = grammar['cond'][f'Gt{is_sql}']
        elif cond[1] == 4:
            ast.constructor = grammar['cond'][f'Lt{is_sql}']
        elif cond[1] == 5:
            ast.constructor = grammar['cond'][f'Ge{is_sql}']
        elif cond[1] == 6:
            ast.constructor = grammar['cond'][f'Le{is_sql}']
        elif cond[1] == 7:
            ast.constructor = grammar['cond'][f'Neq{is_sql}']
        elif cond[1] == 8:
            ast.constructor = grammar['cond'][f'{is_not}In{is_sql}']
        elif cond[1] == 9:
            ast.constructor = grammar['cond'][f'{is_not}Like{is_sql}']
        else:
            raise ValueError(f'unknown conditional operator {cond[1]}')
        if is_sql:
            ast.sons.append(AbstractSyntaxTreeSpider.parse_sql(grammar, cond[3]))
        return ast

    @staticmethod
    def parse_val_unit(grammar, val_unit, is_distinct=False):
        ast = AbstractSyntaxTreeSpider('val_unit')
        if val_unit[0] > 0:
            val_unit[1][1][0] = val_unit[0]
        val_unit = val_unit[1]
        ast.sons.append(AbstractSyntaxTreeSpider.parse_col_unit(grammar, val_unit[1], is_distinct))
        if val_unit[0] == 0:
            ast.constructor = grammar['val_unit']['Unary']
            return ast
        ast.sons.append(AbstractSyntaxTreeSpider.parse_col_unit(grammar, val_unit[2], is_distinct))
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
    def parse_col_unit(grammar, col_unit, is_distinct=False):
        ast = AbstractSyntaxTreeSpider('col_unit')
        is_distinct |= col_unit[2]
        if col_unit[0] == 0:
            ast.constructor = grammar['col_unit']['Distinct'] if is_distinct else grammar['col_unit']['None']
        elif col_unit[0] == 1:
            ast.constructor = grammar['col_unit']['Max']
        elif col_unit[0] == 2:
            ast.constructor = grammar['col_unit']['Min']
        elif col_unit[0] == 3:
            ast.constructor = grammar['col_unit']['CountDistinct'] if is_distinct else grammar['col_unit']['Count']
        elif col_unit[0] == 4:
            ast.constructor = grammar['col_unit']['Sum']
        elif col_unit[0] == 5:
            ast.constructor = grammar['col_unit']['Avg']
        else:
            raise ValueError(f'unknown aggregate function {col_unit[0]}')
        return ast

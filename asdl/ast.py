class AbstractSyntaxTree:
    def __init__(self, type, constructor):
        self.type = type
        self.constructor = constructor
        self.sons = []

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
        for sql_keyword in ['intersect', 'union', 'except']:
            if sql[sql_keyword]:
                ast = AbstractSyntaxTree('sql', grammar.constructors['sql'][sql_keyword.title()])
                ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql))
                ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql[sql_keyword]))
                return ast
        ast = AbstractSyntaxTree('sql', grammar.constructors['sql']['Single'])
        ast.sons.append(AbstractSyntaxTree.parse_sql_unit(grammar, sql))
        return ast

    @staticmethod
    def parse_sql_unit(grammar, sql_unit):
        pass

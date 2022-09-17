class Constructor:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def __eq__(self, constructor):
        return isinstance(constructor, Constructor) and self.name == constructor.name and self.fields == constructor.fields

    def __hash__(self):
        result = hash(self.name)
        for field in self.fields:
            result ^= hash(field)
        return result


class Grammar:
    def __init__(self, constructors):
        self.constructors = constructors

    @staticmethod
    def from_file(filepath):
        with open(filepath, 'r') as file:
            grammar_rules = file.read().split('\n')
        constructors = {}
        i = 0
        while i < len(grammar_rules):
            grammar_rule = grammar_rules[i].strip()
            type = grammar_rule[:grammar_rule.find('=')].strip()
            grammar_rule = grammar_rule[grammar_rule.find('=') + 1:].strip()
            constructors[type] = {}
            while 1:
                constructor = Constructor(
                    grammar_rule[:grammar_rule.find('(')],
                    grammar_rule[grammar_rule.find('(') + 1:grammar_rule.find(')')].split(', ')
                )
                constructors[type][constructor.name] = constructor
                i += 1
                if i >= len(grammar_rules):
                    break
                grammar_rule = grammar_rules[i].strip(' |')
                if grammar_rule == '':
                    i += 1
                    break
        return Grammar(constructors)

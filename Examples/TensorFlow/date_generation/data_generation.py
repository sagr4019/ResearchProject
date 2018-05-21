import random


class ProgramGen:
    def __init__(self):
        self.params = {
            "variables": ["v1", "v2", "v3", "v4"],
            "numbers": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "expressions": ["<", "<=", ">", ">=", "==", "!="],
            "operators": ["+", "-", "*", "/"]
        }
        self.tpl = {
            "while": ('while( {exprhelper} ){{\n    {code}\n}}\n'),
            "if": ('if( {exprhelper} ){{\n    {code}\n}}\n'),
            "declaration": ('{var} = {declhelper};\n')
        }
        self.helper = {
            "expr": ('{var} {expr} {varnr}'),
            "decl": ('{varnr} {operator} {varnr2}')
        }
        self.end = ('return {};')

    def generateHelper(self, _batchsize=100):  # creates 100 combinations of expr. and decl.
        declarations = []
        expressions = []
        varnr = self.params["variables"] + self.params["numbers"]
        operators = self.params["operators"]
        for i in range(_batchsize):
            rnd = int(round(random.uniform(0, 1)))
            if rnd == 0:  # extend declaration with operator and number/var
                declarations.append(self.helper["decl"].format(varnr=random.choice(varnr),
                                                               operator=random.choice(operators),
                                                               varnr2=random.choice(varnr)))
            else:
                declarations.append(self.helper["decl"].format(varnr=random.choice(varnr), operator='', varnr2='').strip())

        for i in range(_batchsize):
            expressions.append(self.helper["expr"].format(var=random.choice(self.params["variables"]),
                                                          expr=random.choice(self.params["expressions"]),
                                                          varnr=random.choice(varnr)))

        return expressions, declarations

    def createRndProgramm(self, _count=50, _loc=10):
        expression, declarations = self.generateHelper()
        programms = []
        for i in range(_count):
            lines = ""
            rLinesOfDeclaration = int(round(random.uniform(2, 6)))
            for j in range(rLinesOfDeclaration):
                lines += self.tpl["declaration"].format(var=random.choice(self.params["variables"]),
                                                        declhelper=random.choice(declarations))
            for j in range(_loc):
                element = random.choice(list(self.tpl.keys()))
                rnd = int(round(random.uniform(0, 1)))
                if element == "while" or element == "if":
                    if rnd == 0:
                        lines += self.tpl[element].format(exprhelper=random.choice(expression),
                                                          code=random.choice(self.params["variables"]) + " = " +
                                                          random.choice(declarations) + ";")
                    else:
                        lines += self.tpl[element].format(exprhelper=random.choice(expression),
                                                          code=(random.choice(self.params["variables"]) + " = " +
                                                                random.choice(declarations) + ";\n    " +
                                                                random.choice(self.params["variables"]) + " = " +
                                                                random.choice(declarations) + ";"))
                else:
                    lines += self.tpl[element].format(var=random.choice(self.params["variables"]),
                                                      declhelper=random.choice(declarations))
            programms.append(lines + self.end.format("true"))
        return programms


def main(args):
    tmp = ProgramGen()
    myProgram = tmp.createRndProgramm(25, 15)
    count = 1
    for item in myProgram:
        tmpfile = open("data/unchecked/" + str(count) + ".txt", 'w')
        tmpfile.write("%s\n" % item)
        count = count + 1
        # print item


if __name__ == '__main__':
    main("test")

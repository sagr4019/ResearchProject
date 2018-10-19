import random
import string
from random import randint
from pprint import pprint


IDENTIFIER_LENGTH = 1
INT_START_RANGE = -999999
INT_END_RANGE = 999999

MAX_DEPTH_EXPRESSION = 10
MAX_DEPTH_COMMAND = 10

depth_expression = 0  # global expression depth counter
depth_command = 0  # global command depth counter


class Expr:
    kind = None

    def __init__(self, kind):
        self.kind = kind


class TypeExpr(Expr):
    _value = None

    def __init__(self, kind, value):
        Expr.kind = kind
        self._value = value

    def get(self):
        return {'Kind': Expr.kind,
                'Value': self._value
                }


class OpExpr(Expr):
    _operator = None
    _operand = None
    _operand2 = None

    def __init__(self, kind, operator, operand, operand2):
        Expr.kind = kind
        self._operator = operator
        self._operand = operand
        self._operand2 = operand2

    def get(self):
        return {'Kind': Expr.kind,
                'Operator': self._operator,
                'Operand1': self._operand,
                'Operand2': self._operand2,
                }


class ExpressionGenerator:

    ast = {}

    def __init__(self):
        rnd = randint(0, 1)
        if rnd == 0:
            self.ast = self.int().get()
        else:
            self.ast = self.str().get()

    def get(self):
        return self.ast

    def int(self):
        self.ast = TypeExpr('Int', randint(INT_START_RANGE, INT_END_RANGE)).get()
        return self

    def str(self):
        self.ast = TypeExpr('Str', self._random_word()).get()
        return self

    def add(self, e, e2):
        self.ast = OpExpr('Add', '+', e.get(), e2.get()).get()
        return self

    def sub(self, e, e2):
        self.ast = OpExpr('Sub', '-', e.get(), e2.get()).get()
        return self

    def equal(self, e, e2):
        self.ast = OpExpr('Equal', '==', e.get(), e2.get()).get()
        return self

    def less(self, e, e2):
        self.ast = OpExpr('Less', '<', e.get(), e2.get()).get()
        return self

    def _random_word(self, n=IDENTIFIER_LENGTH):
        return ''.join(random.choice(string.ascii_letters) for _ in range(n))


def gen_expr(expr):
    global depth_expression
    depth_expression += 1
    if depth_expression >= MAX_DEPTH_EXPRESSION:
        return expr

    rnd = randint(0, 5)
    if rnd == 0:  # int
        if depth_expression == 1:  # set int expr
            expr.int()
        else:  # generate new int expression
            return ExpressionGenerator().int()
    elif rnd == 1:  # str
        if depth_expression == 1:  # set str expr
            expr.str()
        else:  # generate new str expression
            return ExpressionGenerator().str()
    elif rnd == 2:
        e = gen_expr(ExpressionGenerator())
        e2 = gen_expr(ExpressionGenerator())
        expr.add(e, e2)
    elif rnd == 3:
        e = gen_expr(ExpressionGenerator())
        e2 = gen_expr(ExpressionGenerator())
        expr.sub(e, e2)
    elif rnd == 4:
        e = gen_expr(ExpressionGenerator())
        e2 = gen_expr(ExpressionGenerator())
        expr.equal(e, e2)
    else:
        e = gen_expr(ExpressionGenerator())
        e2 = gen_expr(ExpressionGenerator())
        expr.less(e, e2)
    return expr


def generate_expression():
    depth_expression = 0  # set start depth
    return gen_expr(ExpressionGenerator()).get()


class Cmd:
    kind = None

    def __init__(self, kind):
        self.kind = kind


class IfCmd(Cmd):
    _condition = None
    _then = None
    _else = None

    def __init__(self, e, c, c2=None):
        Cmd.kind = 'If'
        self._condition = e
        self._then = c
        self._else = c2

    def get(self):
        return {'Kind': Cmd.kind,
                'Condition': self._condition,
                'Then': self._then,
                'Else': self._else
                }


class WhileCmd(Cmd):
    _condition = None
    _do = None

    def __init__(self, e, c):
        Cmd.kind = 'While'
        self._condition = e
        self._do = c

    def get(self):
        return {'Kind': Cmd.kind,
                'Condition': self._condition,
                'Do': self._do
                }


class OpCmd(Cmd):
    _operator = None
    _operand = None
    _operand2 = None

    def __init__(self, kind, operator, operand, operand2):
        Cmd.kind = kind
        self._operator = operator
        self._operand = operand
        self._operand2 = operand2

    def get(self):
        return {'Kind': Cmd.kind,
                'Operator': self._operator,
                'Operand1': self._operand,
                'Operand2': self._operand2,
                }


class CommandGenerator:

    ast = {}

    def __init__(self):
        # default cmd is an assignment of two expressions
        e = generate_expression()
        e2 = generate_expression()
        self.assign(e, e2)

    def get(self):
        return self.ast

    def assign(self, e, e2):
        self.ast = OpCmd('Assign', ':=', e, e2).get()
        return self

    def concat(self, c):
        self.ast = OpCmd('Concat', '; ', c.get(), self.ast).get()
        return self

    def ifcmd(self, e, c):
        self.ast = IfCmd(e, c.get(), self.ast).get()
        return self

    def whilecmd(self, e, c):
        self.ast = WhileCmd(e, c.get()).get()
        return self


def gen_cmd(cmd):
    global depth_command
    depth_command += 1
    if depth_command >= MAX_DEPTH_COMMAND:
        return cmd

    rnd = randint(0, 3)
    if rnd == 0:  # assignment
        if depth_command == 1:  # cmd is assignment by default
            True
        else:  # generate another assignment as cmd
            return CommandGenerator()
    elif rnd == 1:
        cmd2 = gen_cmd(CommandGenerator())
        cmd.concat(cmd2)
    elif rnd == 2:
        cmd2 = gen_cmd(CommandGenerator())
        cmd.ifcmd(generate_expression(), cmd2)
    else:
        cmd2 = gen_cmd(CommandGenerator())
        cmd.whilecmd(generate_expression(), cmd2)
    return cmd


def generate_command():
    depth_command = 0  # set start depth
    return gen_cmd(CommandGenerator()).get()


class Phrase:

    def generate(self):
        rnd = randint(0, 1)
        if rnd == 0:
            print('Generating Expression as phrase\n')
            return generate_expression()
        else:
            print('Generating Command as phrase\n')
            return generate_command()


def prettyprinter(ast):
    """Convert AST to human readable code with bracketing"""
    code = ''
    if 'Kind' in ast:
        if ast['Kind'] == 'If':
            code += 'if ('
            new_code = prettyprinter(ast['Condition'])
            code += new_code
            code += ') then {'
            new_code = prettyprinter(ast['Then'])
            code += new_code
            code += '} else {'
            new_code = prettyprinter(ast['Else'])
            code += new_code
            code += '}'
        elif ast['Kind'] == 'While':
            code += 'while ('
            new_code = prettyprinter(ast['Condition'])
            code += new_code
            code += ') do {'
            new_code = prettyprinter(ast['Do'])
            code += new_code
            code += '}'
        else:
            if 'Value' in ast:
                code += str(ast['Value'])
            else:
                code += '('
                new_code = prettyprinter(ast['Operand1'])
                code += new_code
                code += ast['Operator']
                new_code = prettyprinter(ast['Operand2'])
                code += new_code
                code += ')'
    return code


def main():
    ast = Phrase().generate()
    pprint(ast)
    print('')
    print(prettyprinter(ast))


if __name__ == "__main__":
    main()

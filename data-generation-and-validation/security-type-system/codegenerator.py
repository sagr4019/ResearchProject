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
    _left = None
    _right = None

    def __init__(self, kind, left, right):
        Expr.kind = kind
        self._left = left
        self._right = right

    def get(self):
        return {'Kind': Expr.kind,
                'Left': self._left,
                'Right': self._right,
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
        self.ast = TypeExpr('Var', self._random_word()).get()
        return self

    def add(self, e, e2):
        self.ast = OpExpr('Add', e.get(), e2.get()).get()
        return self

    def sub(self, e, e2):
        self.ast = OpExpr('Sub', e.get(), e2.get()).get()
        return self

    def equal(self, e, e2):
        self.ast = OpExpr('Equal', e.get(), e2.get()).get()
        return self

    def less(self, e, e2):
        self.ast = OpExpr('Less', e.get(), e2.get()).get()
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
    else:
        e = gen_expr(ExpressionGenerator())
        e2 = gen_expr(ExpressionGenerator())
        if rnd == 2:
            expr.add(e, e2)
        elif rnd == 3:
            expr.sub(e, e2)
        elif rnd == 4:
            expr.equal(e, e2)
        else:
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


class SomeCmd(Cmd):
    _left = None
    _right = None

    def __init__(self, kind, left, right):
        Cmd.kind = kind
        self._left = left
        self._right = right

    def get(self):
        return {'Kind': Cmd.kind,
                'Left': self._left,
                'Right': self._right
                }


class CommandGenerator:

    ast = {}

    def __init__(self):
        # default cmd is an assignment
        e = ExpressionGenerator().str().get()
        e2 = generate_expression()
        self.assign(e, e2)

    def get(self):
        return self.ast

    def assign(self, e, e2):
        self.ast = SomeCmd('Assign', e, e2).get()
        return self

    def concat(self, c):
        self.ast = SomeCmd('Concat', c.get(), self.ast).get()
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
    else:
        cmd2 = gen_cmd(CommandGenerator())
        if rnd == 1:
            cmd.concat(cmd2)
        elif rnd == 2:
            cmd.ifcmd(generate_expression(), cmd2)
        else:
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
            code += "if ({}) then {{{}}} else {{{}}}".format(
                prettyprinter(ast['Condition']),
                prettyprinter(ast['Then']),
                prettyprinter(ast['Else']))
        elif ast['Kind'] == 'While':
            code += "while ({}) do {{{}}}".format(
                prettyprinter(ast['Condition']),
                prettyprinter(ast['Do']))
        elif 'Value' in ast:
            code += str(ast['Value'])
        else:
            code += "({} {} {})".format(
                prettyprinter(ast['Left']),
                get_center(ast['Kind']),
                prettyprinter(ast['Right']))
    return code


def get_center(kind):
    if kind == 'Assign':
        return ':='
    elif kind == 'Concat':
        return '; '
    elif kind == 'Add':
        return '+'
    elif kind == 'Sub':
        return '-'
    elif kind == 'Equal':
        return '=='
    else:
        return '<'


def main():
    ast = Phrase().generate()
    pprint(ast)
    print('')
    print(prettyprinter(ast))


if __name__ == "__main__":
    main()

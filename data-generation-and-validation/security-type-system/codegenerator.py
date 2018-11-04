import random
import string
import sys
from random import randint
from pprint import pprint

sys.setrecursionlimit(5000)

INT_START_RANGE = -999999
INT_END_RANGE = 999999
IDENTIFIER_LENGTH = 1

MAX_DEPTH_EXPRESSION = 2
MAX_DEPTH_COMMAND = 5


TAB_SIZE = '    '

# ENABLE_SEED = False
ENABLE_SEED = True

vars_assigned = set()

if ENABLE_SEED:
    SEED = 9
    random.seed(SEED)
    print('SEED: {}'.format(SEED))


class IntExpr:

    def gen(self):
        """
        Return AST representation for integers.
        The value for the key 'Value' is a randomly generated integer.
        The value range is defined in the constants INT_START_RANGE and
        INT_END_RANGE.
        """
        return {'Kind': 'Int',
                'Value': randint(INT_START_RANGE, INT_END_RANGE)
                }, 1


class VarExpr:

    def gen(self, only_assigned):
        """
        Return AST representation for variables.
        The value for key 'Name' is a randomly generated string with the
        length as defined in the constant IDENTIFIER_LENGTH.
        """
        if only_assigned:
            global vars_assigned
            var = random.sample(vars_assigned, 1)[0]
        else:
            var = ''.join(random.choice(string.ascii_letters)
                          for _ in range(IDENTIFIER_LENGTH))
        return {'Kind': 'Var',
                'Name': var
                }, 1


class LiteralExpr:

    def gen(self):
        if randint(0, 1) == 0:
            return IntExpr().gen()
        else:
            return VarExpr().gen(True)


class AddExpr:

    def gen(self, depth, no_vars):
        depth_left, depth_right = get_rand_depth(depth - 1)

        left, depth_left = ExprGen().gen(depth_left, no_vars)
        right, depth_right = ExprGen().gen(depth_right, no_vars)
        depth_ret = max(depth_left, depth_right)

        return {'Kind': 'Add',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class SubExpr:

    def gen(self, depth, no_vars):
        depth_left, depth_right = get_rand_depth(depth - 1)

        left, depth_left = ExprGen().gen(depth_left, no_vars)
        right, depth_right = ExprGen().gen(depth_right, no_vars)
        depth_ret = max(depth_left, depth_right)

        return {'Kind': 'Sub',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class EqualExpr:

    def gen(self, depth, no_vars):
        depth_left, depth_right = get_rand_depth(depth - 1)

        left, depth_left = ExprGen().gen(depth_left, no_vars)
        right, depth_right = ExprGen().gen(depth_right, no_vars)
        depth_ret = max(depth_left, depth_right)

        return {'Kind': 'Equal',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class LessExpr:

    def gen(self, depth, no_vars):
        depth_left, depth_right = get_rand_depth(depth - 1)

        left, depth_left = ExprGen().gen(depth_left, no_vars)
        right, depth_right = ExprGen().gen(depth_right, no_vars)
        depth_ret = max(depth_left, depth_right)

        return {'Kind': 'Less',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class ExprGen:

    def gen(self, depth, no_vars=False):
        if depth == 0:
            if no_vars:
                return IntExpr().gen()
            else:
                return LiteralExpr().gen()

        rnd = randint(0, 3)
        if rnd == 0:
            return AddExpr().gen(depth, no_vars)
        elif rnd == 1:
            return SubExpr().gen(depth, no_vars)
        elif rnd == 2:
            return EqualExpr().gen(depth, no_vars)
        elif rnd == 3:
            return LessExpr().gen(depth, no_vars)


class ExpressionGenerator:

    def gen(self, no_vars=False):
        depth = randint(0, MAX_DEPTH_EXPRESSION)
        # print('Generating expression with depth {}'.format(depth))
        return ExprGen().gen(depth, no_vars)


class AssignCmd:

    def gen(self, depth, only_assigned=False, no_vars=False):
        global vars_assigned
        left, _ = VarExpr().gen(only_assigned)
        right, _ = ExpressionGenerator().gen(no_vars)
        vars_assigned.add(left['Name'])

        return {'Kind': 'Assign',
                'Left': left,
                'Right': right,
                }, 0


class SeqCmd:

    def gen(self, depth, pre_assign=False):
        if pre_assign:
            left, depth_left = AssignCmd().gen(depth, no_vars=True)
            right, depth_right = CmdGen().gen(depth - 1)
        else:
            depth_left, depth_right = get_rand_depth(depth - 1)
            left, depth_left = CmdGen().gen(depth_left)
            right, depth_right = CmdGen().gen(depth_right)
        depth_ret = max(depth_left, depth_right)

        return {'Kind': 'Seq',
                'Left': left,
                'Right': right
                }, depth_ret + 1


class WhileCmd:

    def gen(self, depth):
        cond, _ = ExpressionGenerator().gen()
        body, depth_body = CmdGen().gen(depth - 1)

        return {'Kind': 'While',
                'Condition': cond,
                'Body': body,
                }, depth_body + 1


class IfCmd:

    def gen(self, depth):
        cond, _ = ExpressionGenerator().gen()

        depth_then, depth_else = get_rand_depth(depth - 1)

        then, depth_then = CmdGen().gen(depth_then)
        _else, depth_else = CmdGen().gen(depth_else)
        depth_ret = max(depth_then, depth_else)

        return {'Kind': 'If',
                'Condition': cond,
                'Then': then,
                'Else': _else,
                }, depth_ret + 1


class CmdGen:

    def gen(self, depth, pre_assign=False):
        if pre_assign:
            return SeqCmd().gen(depth, pre_assign)
        if depth == 0:
            return AssignCmd().gen(depth)

        rnd = randint(0, 2)
        if rnd == 0:
            return WhileCmd().gen(depth)
        elif rnd == 1:
            return IfCmd().gen(depth)
        elif rnd == 2:
            return SeqCmd().gen(depth,)


class CommandGenerator:

    def gen(self):
        depth = randint(1, MAX_DEPTH_COMMAND)
        print('Generating command with depth {}'.format(depth))
        return CmdGen().gen(depth, pre_assign=True)


def get_rand_depth(depth):
    if randint(0, 1) == 0:
        return depth, randint(0, depth)
    else:
        return randint(0, depth), depth


def prettyprint_singleline(ast):
    """Return AST as human readable single-line string with bracketing"""
    code = ''
    if 'Kind' in ast:
        if ast['Kind'] == 'If':
            code += "if {} then {{{}}} else {{{}}}".format(
                prettyprint_singleline(ast['Condition']),
                prettyprint_singleline(ast['Then']),
                prettyprint_singleline(ast['Else']))
        elif ast['Kind'] == 'While':
            code += "while {} do {{{}}}".format(
                prettyprint_singleline(ast['Condition']),
                prettyprint_singleline(ast['Body']))
        elif ast['Kind'] == 'Int':
            code += str(ast['Value'])
        elif ast['Kind'] == 'Var':
            code += str(ast['Name'])
        else:
            code += "({} {} {})".format(
                prettyprint_singleline(ast['Left']),
                get_center(ast['Kind']),
                prettyprint_singleline(ast['Right']))
    return code


def prettyprint_multiline_indented(ast, level=0):
    """
    Return AST as human readable multi-line string with bracketing and
    indentation
    """
    code = ''
    if 'Kind' in ast:
        if ast['Kind'] == 'If':
            code += "{}if {} then {{\n{}\n{}}} else {{\n{}\n{}}}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Condition'], level),
                prettyprint_multiline_indented(ast['Then'], level + 1),
                get_tabs(level),
                prettyprint_multiline_indented(ast['Else'], level + 1),
                get_tabs(level))
        elif ast['Kind'] == 'While':
            code += "{}while {} do {{\n{}\n{}}}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Condition'], level),
                prettyprint_multiline_indented(ast['Body'], level + 1),
                get_tabs(level))
        elif ast['Kind'] == 'Assign':
            code += "{}{} {} {}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Seq':
            code += "{}{}\n{}".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Add':
            code += "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Sub':
            code += "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Less':
            code += "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Equal':
            code += "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_center(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Int':
            code += str(ast['Value'])
        elif ast['Kind'] == 'Var':
            code += str(ast['Name'])
        else:
            raise RuntimeError("Unknown kind {}".format(ast['Kind']))
    return code


def get_tabs(level):
    """Return tab string for the given level"""
    tabs = ''
    for i in range(level):
        tabs += TAB_SIZE
    return tabs


def get_center(kind):
    """Return the symbol(s) associated with each kind"""
    if kind == 'Assign':
        return ':='
    elif kind == 'Seq':
        return '; '
    elif kind == 'Add':
        return '+'
    elif kind == 'Sub':
        return '-'
    elif kind == 'Equal':
        return '=='
    elif kind == 'Less':
        return '<'
    else:
        raise RuntimeError("Unknown kind {}".format(kind))


def main():
    ast, depth = CommandGenerator().gen()
    pprint(ast)
    print('\n')
    # print(prettyprint_singleline(ast))
    # print('\n')
    print(prettyprint_multiline_indented(ast))


if __name__ == "__main__":
    main()

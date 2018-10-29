import random
import string
import sys
from random import randint
from pprint import pprint

sys.setrecursionlimit(5000)

INT_START_RANGE = -999999
INT_END_RANGE = 999999
IDENTIFIER_LENGTH = 1

MAX_EXPRESSIONS_PER_EXPRESSION = 5
MAX_COMMANDS_PER_COMMAND = 50

TAB_SIZE = '    '

ENABLE_SEED = True


if ENABLE_SEED:
    SEED = 8
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
                }


class VarExpr:

    def gen(self):
        """
        Return AST representation for variables.
        The value for key 'Name' is a randomly generated string with the
        length as defined in the constant IDENTIFIER_LENGTH.
        """
        return {'Kind': 'Var',
                'Name': ''.join(random.choice(string.ascii_letters)
                                for _ in range(IDENTIFIER_LENGTH))
                }


class AddExpr:

    def gen(self, left, right):
        return {'Kind': 'Add',
                'Left': left,
                'Right': right,
                }


class SubExpr:

    def gen(self, left, right):
        return {'Kind': 'Sub',
                'Left': left,
                'Right': right,
                }


class LessExpr:

    def gen(self, left, right):
        return {'Kind': 'Less',
                'Left': left,
                'Right': right,
                }


class EqualExpr:

    def gen(self, left, right):
        return {'Kind': 'Equal',
                'Left': left,
                'Right': right,
                }


class IfCmd:

    def gen(self, condition, then, _else):
        return {'Kind': 'If',
                'Condition': condition,
                'Then': then,
                'Else': _else
                }


class WhileCmd:

    def gen(self, condition, body):
        return {'Kind': 'While',
                'Condition': condition,
                'Body': body
                }


class AssignCmd:

    def gen(self, var, right):
        return {'Kind': 'Assign',
                'Left': var,
                'Right': right
                }


class SeqCmd:

    def gen(self, left, right):
        return {'Kind': 'Seq',
                'Left': left,
                'Right': right
                }


class ExpressionGenerator():

    def gen(self, expr=None, expr_count=0,
            expr_count_max=randint(1, MAX_EXPRESSIONS_PER_EXPRESSION)):
        """
        Return an expression. Even count of expressions within an expression is
        impossible according to the grammar used in the paper. In this case
        the next higher odd count of expressions within an expression is
        selected.
        """
        if expr_count >= expr_count_max:
            return expr, expr_count

        if expr_count == 0:
            if expr_count_max == 1:
                expr, count = self._gen_literal()
            else:
                expr, count = self._gen_simpl_expr()
            expr_count += count
        else:
            if (expr_count + 1) == expr_count_max:
                expr_next, count = self._gen_literal()
            else:
                expr_next, count = ExpressionGenerator().gen(None, 0,
                                                             expr_count_max -
                                                             expr_count - 1)
            rnd = randint(0, 3)
            if rnd == 0:
                if randint(0, 1) == 0:
                    expr = AddExpr().gen(expr, expr_next)
                else:
                    expr = AddExpr().gen(expr_next, expr)
            elif rnd == 1:
                if randint(0, 1) == 0:
                    expr = SubExpr().gen(expr, expr_next)
                else:
                    expr = SubExpr().gen(expr_next, expr)
            elif rnd == 2:
                if randint(0, 1) == 0:
                    expr = LessExpr().gen(expr, expr_next)
                else:
                    expr = LessExpr().gen(expr_next, expr)
            else:
                if randint(0, 1) == 0:
                    expr = EqualExpr().gen(expr, expr_next)
                else:
                    expr = EqualExpr().gen(expr_next, expr)
            expr_count += count + 1
        expr, count = self.gen(expr, expr_count, expr_count_max)
        return expr, count

    def _gen_simpl_expr(self):
        """
        Return a non-recursive expression along with the count of
        subexpressions, that is either a literal or an expression consisting of
        two literals.
        """
        rnd = randint(0, 5)
        if rnd == 0 or rnd == 1:
            return self._gen_literal()
        else:
            left, cl = self._gen_literal()
            right, cr = self._gen_literal()

            if rnd == 2:
                return AddExpr().gen(left, right), cl + cr + 1
            elif rnd == 3:
                return SubExpr().gen(left, right), cl + cr + 1
            elif rnd == 4:
                return LessExpr().gen(left, right), cl + cr + 1
            else:
                return EqualExpr().gen(left, right), cl + cr + 1

    def _gen_literal(self):
        if randint(0, 1) == 0:
            return IntExpr().gen(), 1
        else:
            return VarExpr().gen(), 1


class CommandGenerator():

    def gen(self, cmd=None, cmd_count=0,
            cmd_count_max=randint(1, MAX_COMMANDS_PER_COMMAND)):
        if cmd_count >= cmd_count_max:
            return cmd, cmd_count

        if cmd_count == 0:
            # default arguments are evaluated once when the function is defined
            # and not each time the function is called, which is a problem if
            # we call a function as default argument that should generate a
            # random int. So to get e. g. expressions with a random count of
            # subexpressions inside, we have to randomly generate the count
            # of subexpressions and pass it to gen() each time we call it
            expr, _ = ExpressionGenerator().gen(
                expr_count_max=randint(1, MAX_EXPRESSIONS_PER_EXPRESSION))
            cmd = AssignCmd().gen(VarExpr().gen(), expr)
            cmd_count += 1
        else:
            if (cmd_count + 1) == cmd_count_max:
                expr, _ = ExpressionGenerator().gen(
                    expr_count_max=randint(1, MAX_EXPRESSIONS_PER_EXPRESSION))
                cmd = WhileCmd().gen(expr, cmd)
                cmd_count += 1
            else:
                rnd = randint(0, 2)
                if rnd == 0:
                    expr, _ = ExpressionGenerator().gen(
                        expr_count_max=randint(1, MAX_EXPRESSIONS_PER_EXPRESSION))
                    cmd = WhileCmd().gen(expr, cmd)
                    cmd_count += 1
                elif rnd == 1:
                    expr, _ = ExpressionGenerator().gen(
                        expr_count_max=randint(1, MAX_EXPRESSIONS_PER_EXPRESSION))
                    cmd_next, count = CommandGenerator().gen(None, 0,
                                                             cmd_count_max -
                                                             cmd_count - 1)
                    if randint(0, 1) == 0:
                        cmd = IfCmd().gen(expr, cmd, cmd_next)
                    else:
                        cmd = IfCmd().gen(expr, cmd_next, cmd)
                    cmd_count += count + 1
                else:
                    cmd_next, count = CommandGenerator().gen(None, 0,
                                                             cmd_count_max -
                                                             cmd_count - 1)
                    if randint(0, 1) == 0:
                        cmd = SeqCmd().gen(cmd, cmd_next)
                    else:
                        cmd = SeqCmd().gen(cmd_next, cmd)
                    cmd_count += count + 1
        cmd, count = self.gen(cmd, cmd_count, cmd_count_max)
        return cmd, count


class PhraseGenerator:

    def gen(self):
        if randint(0, 1) == 0:
            ast, count = ExpressionGenerator().gen()
            return 'expression', count, ast
        else:
            ast, count = CommandGenerator().gen()
            return 'command', count, ast


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
    _type, count, ast = PhraseGenerator().gen()
    print('Generated {} with count {} (incl. sub {}s) as phrase\n'.format(
        _type, count, _type,))
    pprint(ast)
    print('\n')
    print(prettyprint_singleline(ast))
    print('\n')
    print(prettyprint_multiline_indented(ast))


if __name__ == "__main__":
    main()

import random
import string
import sys
from random import randint
from pprint import pprint

sys.setrecursionlimit(1500)


IDENTIFIER_LENGTH = 1
INT_START_RANGE = -999999
INT_END_RANGE = 999999

MAX_EXPRESSIONS_PER_EXPRESSION = 7
MAX_COMMANDS_PER_COMMAND = 15  # successfully tested: 1000

ENABLE_SEED = True


if ENABLE_SEED:
    SEED = 3
    random.seed(SEED)
    print('SEED: {}'.format(SEED))


class IntExpr:

    def gen(self):
        return {'Kind': 'Int',
                'Value': randint(INT_START_RANGE, INT_END_RANGE)
                }


class VarExpr:

    def gen(self):
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
        impossible. In this case the next higher odd count of expressions
        within an expression is selected.
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
            expr, _ = ExpressionGenerator().gen()
            cmd = AssignCmd().gen(VarExpr().gen(), expr)
            cmd_count += 1
        else:
            if (cmd_count + 1) == cmd_count_max:
                expr, _ = ExpressionGenerator().gen()
                cmd = WhileCmd().gen(expr, cmd)
                cmd_count += 1
            else:
                rnd = randint(0, 2)
                if rnd == 0:
                    expr, _ = ExpressionGenerator().gen()
                    cmd = WhileCmd().gen(expr, cmd)
                    cmd_count += 1
                elif rnd == 1:
                    expr, _ = ExpressionGenerator().gen()
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
            return 'expr', count, ast
        else:
            ast, count = CommandGenerator().gen()
            return 'cmd', count, ast


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
                prettyprinter(ast['Body']))
        elif 'Value' in ast:
            code += str(ast['Value'])
        elif 'Name' in ast:
            code += str(ast['Name'])
        else:
            code += "({} {} {})".format(
                prettyprinter(ast['Left']),
                get_center(ast['Kind']),
                prettyprinter(ast['Right']))
    return code


def get_center(kind):
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
    else:
        return '<'


def main():
    _type, count, ast = PhraseGenerator().gen()
    print('Generated {} with count {}\n'.format(_type, count))
    pprint(ast)
    print('')
    print(prettyprinter(ast))


if __name__ == "__main__":
    main()

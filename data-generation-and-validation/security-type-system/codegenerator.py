import random
import string
from random import randint
from pprint import pprint


class Expression:

    IDENTIFIER_LENGTH = 1

    def __init__(self, which=None):
        self.code = self.generate_literal(which)

    def generate_literal(self, which=None):
        if which is not None:
            if which == 'LiteralStr':
                c = self._random_word(self.IDENTIFIER_LENGTH)
            else:  # LiteralInt
                c = str(randint(-99, 99))
            self.ast = [{which: c}]
            return c

        rnd = randint(0, 1)
        if rnd <= 0:
            ast_key = 'LiteralStr'
            c = self._random_word(self.IDENTIFIER_LENGTH)
        else:
            ast_key = 'LiteralInt'
            c = str(randint(-99, 99))
        self.ast = [{ast_key: c}]
        return c

    def get(self):
        return {'code': self.code, 'ast': self.ast}

    def _random_word(self, n):
        return ''.join(random.choice(string.ascii_letters) for _ in range(n))

    def add(self, e):
        ast_key = 'AddExpr'
        self.code = self.code + ' + ' + e.get()['code']
        self.ast = add_to_ast(e.get()['ast'], self.ast, ast_key)
        return self.get()

    def sub(self, e):
        ast_key = 'SubExpr'
        self.code = self.code + ' - ' + e.get()['code']
        self.ast = add_to_ast(e.get()['ast'], self.ast, ast_key)
        return self.get()

    def less(self, e):
        ast_key = 'LessExpr'
        self.code = self.code + ' < ' + e.get()['code']
        self.ast = add_to_ast(e.get()['ast'], self.ast, ast_key)
        return self.get()

    def equal(self, e):
        ast_key = 'EqualExpr'
        self.code = self.code + ' == ' + e.get()['code']
        self.ast = add_to_ast(e.get()['ast'], self.ast, ast_key)
        return self.get()


class Command:

    def __init__(self):
        # default is an assignment of two expressions
        self.assign(Expression('LiteralStr'), Expression('LiteralInt'))

    def get(self):
        return {'code': self.code, 'ast': self.ast}

    def assign(self, e, e2):
        # ensure to assign literal only
        if list(e.get()['ast'][0].keys())[0] != 'LiteralStr':
            e = Expression('LiteralStr')
        if list(e2.get()['ast'][0].keys())[0] != 'LiteralInt' and \
                list(e2.get()['ast'][0].keys())[0] != 'LiteralStr':
            e2 = Expression()
        ast_key = 'AssignCMD'
        self.code = e.get()['code'] + ' := ' + e2.get()['code']
        self.ast = add_to_ast(e2.get()['ast'], e.get()['ast'], ast_key)
        return self.get()

    def concat(self, c):
        ast_key = 'ConcatCMD'
        self.code = self.code + '; ' + c.get()['code']
        self.ast = add_to_ast(c.get()['ast'], self.ast, ast_key)
        return self.get()

    def ifcmd(self, e, c):
        ast_key = 'IfCMD'
        self.code = 'if ' + e.get()['code'] \
            + ' then ' + self.code + ' else ' + c.get()['code']
        new_ast = [{'Condition': e.get()['code']},
                   {'Then': self.ast},
                   {'Else': c.get()['ast']}]
        self.ast = add_to_ast(new_ast, self.ast, ast_key)
        self.ast[0][list(self.ast[0].keys())[0]].pop(0)
        return self.get()

    def whilecmd(self, e):
        ast_key = 'WhileCMD'
        self.code = 'while ' + e.get()['code'] + ' do ' + self.code
        new_ast = [{'Condition': e.get()['code']}, {'Do': self.ast}]
        self.ast = add_to_ast(new_ast, self.ast, ast_key)
        self.ast[0][list(self.ast[0].keys())[0]].pop(0)
        return self.get()


def add_to_ast(ast_new, ast_to_add, key):
    ast_new.insert(0, ast_to_add)
    return [{key: ast_new}]


def get_rnd_expression(condition=False, literal=False):
    max_expr_sequence = 1
    if not literal:
        expr = Expression()
        for i in range(max_expr_sequence):
            e = Expression()
            if not condition:
                rnd = randint(0, 3)
            else:
                rnd = randint(2, 3)
            if rnd == 0:
                expr.add(e)
            elif rnd == 1:
                expr.sub(e)
            elif rnd == 2:
                if condition:
                    # ensure identifier left
                    if list(expr.get()['ast'][0].keys())[0] != 'LiteralStr':
                        expr = Expression('LiteralStr')
                expr.less(e)
            else:
                if condition:
                    # ensure identifier left
                    if list(expr.get()['ast'][0].keys())[0] != 'LiteralStr':
                        expr = Expression('LiteralStr')
                expr.equal(e)
        return expr
    return Expression()


def gen_rnd_cmd(max_commands_per_program=10):
    cmd = Command()
    for i in range(max_commands_per_program):
        rnd = randint(0, 3)
        if rnd == 0:
            expr = get_rnd_expression(False, True)
            expr2 = get_rnd_expression(False, True)
            cmd.assign(expr, expr2)
        elif rnd == 1:
            cmd.concat(Command())
        elif rnd == 2:
            cmd.ifcmd(get_rnd_expression(True), Command())
        else:
            cmd.whilecmd(get_rnd_expression(True))
    print(cmd.get()['code'])
    pprint(cmd.get()['ast'])
    print('\n\n')


class Phrase:

    def generate(self):
        rnd = randint(0, 1)
        if rnd == 0:
            print('Generating Expression as phrase\n')
            c = Expression()
        else:
            print('Generating Command as phrase\n')
            c = Command()
        print(c.get()['code'])
        pprint(c.get()['ast'])
        print('\n\n')


def main():
    print('Generating phrase (choosing between expression and command)')
    Phrase().generate()

    no_of_programs = 10
    print('Generating ' + str(no_of_programs) + ' programs...\n')
    for p in range(no_of_programs):
        gen_rnd_cmd()


if __name__ == "__main__":
    main()

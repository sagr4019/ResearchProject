import random
import string
from random import randint


class Expression:

    IDENTIFIER_LENGTH = 1

    def __init__(self):
        self.ast = [{'EXPR': ''}]
        rnd = randint(0, 1)
        if rnd <= 0:
            self.code = str(randint(-99, 99))
        else:
            self.code = self._random_word(self.IDENTIFIER_LENGTH)
        self.ast = add_to_ast(self.ast, {'Literal': [self.code]})

    def generate(self):
        rnd = randint(-30, 3)
        if rnd >= 0:
            e = Expression().generate()
            e2 = Expression().generate()
            if rnd == 0:
                ast_key = 'Add'
                self.code = self._add(e, e2)
            elif rnd == 1:
                ast_key = 'Sub'
                self.code = self._sub(e, e2)
            elif rnd == 2:
                ast_key = 'Less'
                self.code = self._less(e, e2)
            else:
                ast_key = 'Equal'
                self.code = self._equal(e, e2)
            self.ast = add_to_ast(self.ast, {ast_key: [e['ast'], e2['ast']]})
        return {'code': self.code, 'ast': self.ast}

    def _random_word(self, n):
        return ''.join(random.choice(string.ascii_letters) for _ in range(n))

    def _add(self, e, e2):
        return e['code'] + ' + ' + e2['code']

    def _sub(self, e, e2):
        return e['code'] + ' - ' + e2['code']

    def _less(self, e, e2):
        return e['code'] + ' < ' + e2['code']

    def _equal(self, e, e2):
        return e['code'] + ' == ' + e2['code']


class Command:

    def __init__(self):
        self.ast = [{'CMD': ''}]
        self.code = ''

    def generate(self):
        rnd = randint(0, 3)
        if rnd == 0:
            e = Expression().generate()
            e2 = Expression().generate()
            self.code = self._assign(e, e2)
            a = {'Assign': [e['ast'], e2['ast']]}
        elif rnd == 1:
            c = Command().generate()
            c2 = Command().generate()
            self.code = self._concat(c, c2)
            a = {'Concat': [c['ast'], c2['ast']]}
        elif rnd == 2:
            e = Expression().generate()
            c = Command().generate()
            c2 = Command().generate()
            self.code = self._if(e, c, c2)
            a = {'If': [{'Condition': e['ast']},
                        {'ThenBody': c['ast']},
                        {'ElseBody': c2['ast']}]}
        elif rnd == 3:
            e = Expression().generate()
            c = Command().generate()
            self.code = self._while(e, c)
            a = {'While': [{'Condition': e['ast']}, {'Body': c['ast']}]}
        self.ast = add_to_ast(self.ast, a)
        return {'code': self.code, 'ast': self.ast}

    def _assign(self, e, e2):
        return e['code'] + ' := ' + e2['code']

    def _concat(self, c, c2):
        return c['code'] + '; ' + c2['code']

    def _if(self, e, c, c2):
        return 'if ' + e['code'] +  \
            ' then ' + c['code'] + \
            ' else ' + c2['code']

    def _while(self, e, c):
        return 'while ' + e['code'] + ' do ' + c['code']


def add_to_ast(ast, dictionary):
    ast[-1][list(ast[-1].keys())[0]] = dictionary
    return ast


class Phrase:

    def generate(self):
        rnd = randint(0, 1)
        if rnd == 0:
            self.value = Expression().generate()
        else:
            self.value = Command().generate()
        return self.value


def main():
    p = Phrase().generate()
    print(p['code'])
    print(p['ast'])


if __name__ == "__main__":
    main()

import random
import string
import sys
import check_security
import os
import json
from random import randint

sys.setrecursionlimit(500000)

PROGRAMS_TO_GENERATE_VALID = 20
PROGRAMS_TO_GENERATE_INVALID = 20
ENABLE_PRINTING = True

INT_RANGE_START = -999999
INT_RANGE_END = 999999
MAX_LENGTH_IDENTIFIER = 1
MAX_DEPTH_EXPRESSION = 2
MAX_DEPTH_COMMAND = 3
RESERVED_KEYWORDS = ('if', 'then', 'else', 'while', 'do')
TAB_SIZE = 4

SEED = 123456789
random.seed(SEED)


class IntExpr:

    def gen(self):
        """
        Return AST representation for integers.
        The value for the key 'Value' is a randomly generated integer.
        The value range is defined in the constants INT_RANGE_START and
        INT_RANGE_END.
        """
        return {'Kind': 'Int',
                'Value': randint(INT_RANGE_START, INT_RANGE_END)
                }, 1


class VarExpr:

    def gen(self):
        """
        Return AST representation for variables.
        A variable is generated randomly with a random length with a maximum of
        MAX_LENGTH_IDENTIFIER, consisting of lowercase and/or uppercase letters.
        """
        ast = {'Kind': 'Var',
               'Name': self.gen_var()
               }
        return ast, 1

    def gen_var(self):
        var = ''.join(map(lambda x: random.choice(string.ascii_letters),
                          range(randint(1, MAX_LENGTH_IDENTIFIER))))
        while (var.lower() in RESERVED_KEYWORDS):
            var = self.gen_var()
        return var


class LiteralExpr:

    def gen(self):
        return frequency(((1, VarExpr()), (3, IntExpr()))).gen()


class AddExpr:

    def gen(self, depth):
        depth_left, depth_right = get_rand_depth(depth - 1)
        left, depth_left = ExprGen().gen(depth_left)
        right, depth_right = ExprGen().gen(depth_right)

        depth_ret = max(depth_left, depth_right)
        return {'Kind': 'Add',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class SubExpr:

    def gen(self, depth):
        depth_left, depth_right = get_rand_depth(depth - 1)
        left, depth_left = ExprGen().gen(depth_left)
        right, depth_right = ExprGen().gen(depth_right)

        depth_ret = max(depth_left, depth_right)
        return {'Kind': 'Sub',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class EqualExpr:

    def gen(self, depth):
        depth_left, depth_right = get_rand_depth(depth - 1)
        left, depth_left = ExprGen().gen(depth_left)
        right, depth_right = ExprGen().gen(depth_right)

        depth_ret = max(depth_left, depth_right)
        return {'Kind': 'Equal',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class LessExpr:

    def gen(self, depth):
        depth_left, depth_right = get_rand_depth(depth - 1)
        left, depth_left = ExprGen().gen(depth_left)
        right, depth_right = ExprGen().gen(depth_right)

        depth_ret = max(depth_left, depth_right)
        return {'Kind': 'Less',
                'Left': left,
                'Right': right,
                }, depth_ret + 1


class ExprGen:

    def gen(self, depth):
        if depth == 0:
            return LiteralExpr().gen()
        else:
            return one_of((AddExpr(), SubExpr(), EqualExpr(), LessExpr())).gen(depth)


class ExpressionGenerator:

    def gen(self):
        return ExprGen().gen(randint(0, MAX_DEPTH_EXPRESSION))


class DeclareCmd:

    def gen(self, label, var):
        return {'Kind': 'Declare',
                'Label': label,
                'Var': var
                }, 1


class AssignCmd:

    def gen(self, depth):
        left, _ = VarExpr().gen()
        right, _ = ExpressionGenerator().gen()

        return {'Kind': 'Assign',
                'Left': left,
                'Right': right,
                }, 0


def get_vars(ast, vars=None):
    """Return vars from assignments and conditions"""
    if vars is None:
        vars = []
    kind = ast.get("Kind")
    if kind == 'Var':
        if ast.get("Name") not in vars:
            vars.append(ast.get("Name"))
        return vars
    elif kind == 'If':
        return get_vars(ast.get("Condition"),
                        get_vars(ast.get("Else"),
                                 get_vars(ast.get("Then"),
                                          vars)))
    elif kind == 'While':
        return get_vars(ast.get("Condition"),
                        get_vars(ast.get("Body"),
                                 vars))
    elif kind == 'Assign':
        left = get_vars(ast.get("Left"))
        right = get_vars(ast.get("Right"))
        vars.append({
            'Left': left[0],
            'Right': right
        })
        return vars
    elif kind != 'Int':
        return get_vars(ast.get("Left"),
                        get_vars(ast.get("Right"),
                                 vars))
    else:
        return vars


class SeqCmd:

    def gen(self, depth):
        depth_left, depth_right = get_rand_depth(depth - 1)
        left, depth_left = CmdGen().gen(depth_left)
        right, depth_right = CmdGen().gen(depth_right)

        depth_ret = max(depth_left, depth_right)
        return {'Kind': 'Seq',
                'Left': left,
                'Right': right
                }, depth_ret + 1

    def gen_pre_seq(self, left, right, depth):
        return {'Kind': 'Seq',
                'Left': left,
                'Right': right
                }, depth + 1


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

    def gen(self, depth):
        if depth == 0:
            return AssignCmd().gen(depth)
        else:
            return one_of((WhileCmd(), IfCmd(), SeqCmd())).gen(depth)


class CommandGenerator:

    def gen(self, gen_valid):
        depth = randint(1, MAX_DEPTH_COMMAND)
        ast, depth = CmdGen().gen(depth)

        mixed = get_vars(ast)
        # assignments (indices) contain left and right keys
        assigns = list(filter(lambda i: 'Left' in mixed[i], range(len(mixed))))
        # vars (indices) from e. g. conditions
        vars = list(filter(lambda i: 'Left' not in mixed[i], range(len(mixed))))
        labels = {}
        if gen_valid:
            for i in assigns:
                ass = mixed[i]
                left_var = ass['Left']
                if left_var in labels:
                    left_label = labels[left_var]
                else:
                    # if one of the right vars already set in labels,
                    # get the label
                    left_label = self.get_label(ass['Right'], labels)
                    labels[left_var] = left_label

                for right_var in ass['Right']:
                    if right_var not in labels:
                        if left_label == 'H':
                            right_label = self.rand_label()
                        else:
                            right_label = 'L'
                        labels[right_var] = right_label
            for i in vars:
                var = mixed[i]
                if var not in labels:
                    labels[var] = self.rand_label()
        else:
            # get one assignment with at least one var right
            idx = list(filter(lambda i: len(mixed[i]['Right']) > 0, assigns))
            if len(idx) > 0:
                rnd = one_of(idx)
                left_var = mixed[rnd]['Left']
                labels[left_var] = 'L'

                rnd2 = randint(0, len(mixed[rnd]['Right']) - 1)
                right_var = mixed[rnd]['Right'][rnd2]
                labels[right_var] = 'H'

                # set also labels for other variables in assignments
                for i in assigns:
                    ass = mixed[i]
                    left_var = ass['Left']
                    if left_var not in labels:
                        labels[left_var] = self.rand_label()

                    for right_var in ass['Right']:
                        if right_var not in labels:
                            labels[right_var] = self.rand_label()

                # set labels for other variables
                for i in vars:
                    var = mixed[i]
                    if var not in labels:
                        labels[var] = self.rand_label()
            else:
                if ENABLE_PRINTING:
                    print('can\'t find any assignment with at least one right var '
                          'to set it invalid. Thus can\'t generate an invalid program. '
                          'Generating another program...')

                return CommandGenerator().gen(gen_valid)

        for var, label in labels.items():
            left, depth_left = DeclareCmd().gen(label, var)
            ast, depth = SeqCmd().gen_pre_seq(left, ast, depth_left + depth)

        sec_type = check_security.check_security(ast)
        return ast, depth, sec_type

    def rand_label(self):
        return random.choice(('H', 'L'))

    def get_label(self, vars, labels):
        for var in vars:
            if var in labels:
                return labels[var]
        return self.rand_label()


def get_rand_depth(depth):
    if randint(0, 1) == 0:
        return depth, randint(0, depth)
    else:
        return randint(0, depth), depth


def one_of(choices):
    rnd = randint(0, len(choices) - 1)
    return choices[rnd]


def prettyprint_singleline(ast):
    """Return AST as human readable single-line string with bracketing"""
    if 'Kind' in ast:
        if ast['Kind'] == 'If':
            code = "if {} then {{{}}} else {{{}}}".format(
                prettyprint_singleline(ast['Condition']),
                prettyprint_singleline(ast['Then']),
                prettyprint_singleline(ast['Else']))
        elif ast['Kind'] == 'While':
            code = "while {} do {{{}}}".format(
                prettyprint_singleline(ast['Condition']),
                prettyprint_singleline(ast['Body']))
        elif ast['Kind'] == 'Int':
            code = str(ast['Value'])
        elif ast['Kind'] == 'Var':
            code = str(ast['Name'])
        elif ast['Kind'] == 'Declare':
            code = "{} {}".format(ast['Label'], ast['Var'])
        else:
            code = "({} {} {})".format(
                prettyprint_singleline(ast['Left']),
                get_operator_symbol(ast['Kind']),
                prettyprint_singleline(ast['Right']))
    return code


def prettyprint_multiline_indented(ast, level=0):
    """
    Return AST as human readable multi-line string with bracketing and
    indentation
    """
    if 'Kind' in ast:
        if ast['Kind'] == 'If':
            code = "{}if {} then {{\n{}\n{}}} else {{\n{}\n{}}}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Condition'], level),
                prettyprint_multiline_indented(ast['Then'], level + 1),
                get_tabs(level),
                prettyprint_multiline_indented(ast['Else'], level + 1),
                get_tabs(level))
        elif ast['Kind'] == 'While':
            code = "{}while {} do {{\n{}\n{}}}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Condition'], level),
                prettyprint_multiline_indented(ast['Body'], level + 1),
                get_tabs(level))
        elif ast['Kind'] == 'Assign':
            code = "{}{} {} {}".format(
                get_tabs(level),
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Seq':
            code = "{}{}\n{}".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Add':
            code = "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Sub':
            code = "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Less':
            code = "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Equal':
            code = "({} {} {})".format(
                prettyprint_multiline_indented(ast['Left'], level),
                get_operator_symbol(ast['Kind']),
                prettyprint_multiline_indented(ast['Right'], level))
        elif ast['Kind'] == 'Int':
            code = str(ast['Value'])
        elif ast['Kind'] == 'Var':
            code = str(ast['Name'])
        elif ast['Kind'] == 'Declare':
            code = "{} {}".format(ast['Label'], ast['Var'])
        else:
            raise RuntimeError("Unknown kind {}".format(ast['Kind']))
    return code


def get_tabs(level):
    """Return tab string for the given level"""
    return ' ' * TAB_SIZE * level


def get_operator_symbol(kind):
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


def store(ast, dir, id):
    path_current = os.path.dirname(os.path.realpath(__file__))
    fname = '{} - {}.txt'.format(SEED, id)
    path = path_current + '/' + dir + '/' + fname
    with open(path, 'w') as out:
        out.write(json.dumps(ast))


def frequency(choices):
    sum_of_dist = sum(map(lambda x: x[0], choices))

    # build a distribution dictionary
    idx = 0
    no_of_values = 0
    dist = {}
    for i in range(sum_of_dist):
        if choices[idx][0] == no_of_values:
            idx += 1
            no_of_values = 0
        dist[i] = choices[idx][1]
        no_of_values += 1

    rnd = randint(0, sum_of_dist - 1)
    return dist[rnd]


def gen_program_valid(i):
    ast, _, sec_type = CommandGenerator().gen(True)
    print('Generated {}. valid program'.format(i + 1))
    if ENABLE_PRINTING:
        print('securitychecker outputs {}'.format('valid' if sec_type else 'invalid'))
        print(prettyprint_multiline_indented(ast))
        print('\n')
    dir_out = 'programs/valid'
    store(ast, dir_out, i + 1)


def gen_program_invalid(i):
    ast, _, sec_type = CommandGenerator().gen(False)
    print('Generated {}. invalid program'.format(i + 1))
    if ENABLE_PRINTING:
        print('securitychecker outputs {}'.format('valid' if sec_type else 'invalid'))
        print(prettyprint_multiline_indented(ast))
        print('\n')
    dir_out = 'programs/invalid'
    store(ast, dir_out, i + 1)


def main():
    list(map(gen_program_valid, range(PROGRAMS_TO_GENERATE_VALID)))
    list(map(gen_program_invalid, range(PROGRAMS_TO_GENERATE_INVALID)))


if __name__ == "__main__":
    main()

import random
import string
import sys
import check_security
import os
import json
from random import randint

sys.setrecursionlimit(500000)

INT_START_RANGE = -999999
INT_END_RANGE = 999999
IDENTIFIER_LENGTH = 1

MAX_DEPTH_EXPRESSION = 2
MAX_DEPTH_COMMAND = 15

PROGRAMS_TO_GENERATE_VALID = 2
PROGRAMS_TO_GENERATE_INVALID = 2


RESERVED_KEYWORDS = ['if', 'then', 'else', 'while', 'do']
TAB_SIZE = 4

ENABLE_SEED = True

all_vars_asts = []
ass_vars_l_r = []

if ENABLE_SEED:
    SEED = 123456789
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

    def gen(self):
        """
        Return AST representation for variables.
        A variable is generated randomly with a random length with a maximum of
        IDENTIFIER_LENGTH, consisting of lowercase and/or uppercase letters.
        """
        global all_vars_asts
        var = ''.join(random.choice(string.ascii_letters)
                      for _ in range(randint(1, IDENTIFIER_LENGTH)))
        while (var.lower() in RESERVED_KEYWORDS):
            var = ''.join(random.choice(string.ascii_letters)
                          for _ in range(randint(1, IDENTIFIER_LENGTH)))

        ast = {'Kind': 'Var',
               'Name': var
               }
        if ast not in all_vars_asts:
            all_vars_asts.append(ast)

        return ast, 1


class LiteralExpr:

    def gen(self):
        return frequency([[1, VarExpr()], [10, IntExpr()]]).gen()


def frequency(choices):
    maxint = 0
    for e in range(0, len(choices) - 1):
        maxint = max(choices[e][0], choices[e + 1][0])

    rnd = randint(1, maxint)
    for e in choices:
        if rnd <= e[0]:
            return e[1]


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
            return one_of([AddExpr(), SubExpr(), EqualExpr(), LessExpr()]).gen(depth)


class ExpressionGenerator:

    def gen(self):
        depth = randint(0, MAX_DEPTH_EXPRESSION)
        # print('Generating expression with depth {}'.format(depth))
        return ExprGen().gen(depth)


class DeclareCmd:

    def gen(self, label, var):
        return {'Kind': 'Declare',
                'Label': label,
                'Var': var
                }, 1


class AssignCmd:

    def gen(self, depth):
        global ass_vars_l_r
        left, _ = VarExpr().gen()
        right, _ = ExpressionGenerator().gen()

        # find all vars used on the right side that are not equal to the
        # left side
        right_vars = find_vars(ast=right, vars=[], left_var_name=left['Name'])
        if right_vars is not None:
            # search ass_vars_l_r for left var to figure out if it has already
            # been assigned and try to append new right vars to it's rightvars
            # list
            left_var_found = False
            for i in range(len(ass_vars_l_r)):
                if ass_vars_l_r[i]['Name'] == left['Name']:
                    left_var_found = True
                    for e in right_vars:
                        if e not in ass_vars_l_r[i]['RightVars']:
                            ass_vars_l_r[i]['RightVars'].append(e)

            if not left_var_found and len(right_vars) > 0:
                # left var has not yet been assigned, create a new list entry
                ass_vars_l_r.append({
                    'Name': left['Name'],
                    'RightVars': right_vars
                })

        return {'Kind': 'Assign',
                'Left': left,
                'Right': right,
                }, 0


def find_vars(ast, vars, left_var_name):
    """
    Return names of vars from ast for each var that has not the same name as
    the given argument left_var_name, which is the left side of an assignment
    """
    kind = ast.get("Kind")

    if kind == 'Var':
        if ast.get("Name") not in vars and ast.get("Name") != left_var_name:
            vars.append(ast.get("Name"))
        return vars
    elif kind == 'If':
        return find_vars(ast.get("Else"),
                         find_vars(ast.get("Then"),
                                   vars,
                                   left_var_name),
                         left_var_name)
    elif kind == 'While':
        return find_vars(ast.get("Body"),
                         vars,
                         left_var_name)
    elif kind != 'Int':
        return find_vars(ast.get("Left"),
                         find_vars(ast.get("Right"),
                                   vars,
                                   left_var_name),
                         left_var_name)
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
            return one_of([WhileCmd(), IfCmd(), SeqCmd()]).gen(depth)


class CommandGenerator:

    def gen(self, gen_valid):
        global all_vars_asts
        all_vars_asts = []
        depth = randint(1, MAX_DEPTH_COMMAND)
        ast, depth = CmdGen().gen(depth)

        environment = dict()
        if not gen_valid:
            if len(ass_vars_l_r) > 0:
                # if there are assignments which use vars on the right side
                # choose one assignment which should be marked as insecure
                # (left var L, at one right var H)
                no_of_insec_ass = 1
                # no_of_insec_ass = randint(1, len(ass_vars_l_r))
                assigns = random.sample(ass_vars_l_r, no_of_insec_ass)
                for e in assigns:
                    # choose one random var from the right side ( ... := ... x ...)
                    no_of_r_vars = 1
                    # no_of_r_vars = randint(1, len(e['RightVars']))
                    r_vars = random.sample(e['RightVars'], no_of_r_vars)
                    for ee in r_vars:
                        # set it's label as H
                        environment[ee] = 'H'

                    # set label for var from left as L, e. g. ( x := ...)
                    environment[e['Name']] = 'L'

        for e in all_vars_asts:
            if not e['Name'] in environment:
                label = random.choice(['H', 'L'])
                # label = 'L'
            else:
                label = environment[e['Name']]

            left, depth_left = DeclareCmd().gen(label, e['Name'])
            ast, depth = SeqCmd().gen_pre_seq(left, ast, depth_left + depth)

        sec_type = check_security.check_security(ast)

        if gen_valid and sec_type is None:
            return CommandGenerator().gen(gen_valid=gen_valid)
        elif not gen_valid and sec_type is not None:
            return CommandGenerator().gen(gen_valid=gen_valid)
        else:
            # print('Generated command with depth {}'.format(depth))
            return ast, depth, sec_type


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
    with open(path, 'a') as out:
        out.write(json.dumps(ast))


def main():
    for i in range(PROGRAMS_TO_GENERATE_VALID):
        ast, _, sec_type = CommandGenerator().gen(True)
        dir_out = 'programs/valid'
        # print('Generated {} program into {}'.format('valid' if sec_type else 'invalid',
        # dir_out))
        # print(prettyprint_multiline_indented(ast))
        store(ast, dir_out, i)
    for i in range(PROGRAMS_TO_GENERATE_INVALID):
        ast, _, sec_type = CommandGenerator().gen(False)
        dir_out = 'programs/invalid'
        # print('Generated {} program into {}'.format('valid' if sec_type else 'invalid',
        # dir_out))
        # print(prettyprint_multiline_indented(ast))
        store(ast, dir_out, i)


if __name__ == "__main__":
    main()

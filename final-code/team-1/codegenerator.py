import random
import string
import sys
import check_security
import os
import json
from random import randint
import pickle

sys.setrecursionlimit(500000)
PROGRAMS_TO_GENERATE_VALID = 1
PROGRAMS_TO_GENERATE_INVALID = 0
ENABLE_IMPLICIT_FLOW = False
STORE_PRETTYPRINTED_AST = True
STORE_PICKLE = True
PRINT_SECURITY_OUTPUT = False
PRINT_PATHS = True
INT_RANGE_START = -999999
INT_RANGE_END = 999999
MAX_LENGTH_IDENTIFIER = 1
MAX_DEPTH_EXPRESSION = 2
MAX_DEPTH_COMMAND = 3
TAB_SIZE = 4
SEED = 1234567890

RESERVED_KEYWORDS = ('if', 'then', 'else', 'while', 'do')
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
        var = ''.join(map(lambda x: random.choice(string.ascii_lowercase),
                          range(randint(1, MAX_LENGTH_IDENTIFIER))))
        while (var.lower() in RESERVED_KEYWORDS):
            var = self.gen_var()
        return var


class LiteralExpr:

    def gen(self):
        return frequency(((3, VarExpr()), (1, IntExpr()))).gen()


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
            return one_of((AddExpr(), SubExpr(),
                           EqualExpr(), LessExpr())).gen(depth)


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

    def gen(self, gen_valid, implicit=False):
        depth = randint(0, MAX_DEPTH_COMMAND)
        ast, depth = CmdGen().gen(depth)

        mixed = get_vars(ast)
        assigns = list(filter(lambda i: 'Left' in mixed[i], range(len(mixed))))
        vars = list(
            filter(lambda i: 'Left' not in mixed[i], range(len(mixed))))
        labels = {}
        if implicit:
            labels = self.get_implicit_labels(ast, labels, gen_valid)
            if labels is None:
                # unable to set program invalid  based on implicit flow
                # due to too few various variables (all conditions and left
                # assignments equal)
                return CommandGenerator().gen(gen_valid, implicit)
        labels = self.get_labels(ast, labels, mixed, assigns, vars, gen_valid)
        if labels is None:
            # unable to find one var on the right side of an assignment
            # to set invalid. Thus can't generate an invalid program.
            # Generate another one
            return CommandGenerator().gen(gen_valid, implicit)

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

    def get_implicit_labels(self, ast, labels, gen_valid):
        tmp = condition_assignments(ast)
        conds_and_assigns = []
        [conds_and_assigns.append(e) for e in tmp if isinstance(e, dict)]
        if not gen_valid:
            # One variable from a condition must be H
            # One assignment variable from this condition must be L
            _range = set(range(len(conds_and_assigns)))
            while _range:
                rnd = random.choice(list(_range))
                # remove the choosen index of the pair from the set to ensure
                # that they are not reused
                _range.remove(rnd)
                # choose a random pair of condition and assignment
                conds = conds_and_assigns[rnd]['Condition']
                assigned = conds_and_assigns[rnd]['Assigned']
                # choose a random condition var and assignment var
                var_cond = random.choice(list(conds))
                var_ass = random.choice(list(assigned))
                if var_cond == var_ass:
                    # cannot set different labels for the same var,
                    # try to choose another one
                    if len(list(conds)) == 1 and len(list(assigned)) == 1:
                        # var used in condition and assignment are the same
                        # and there are no other vars in both sets
                        # do another loop run and
                        continue
                    if len(conds) > 1:
                        conds.remove(var_cond)
                        var_cond = random.choice(list(conds))
                    else:
                        assigned.remove(var_ass)
                        var_ass = random.choice(list(assigned))
                labels[var_cond] = 'H'
                labels[var_ass] = 'L'
                _range = set()
            if len(labels) < 2:
                # unable to set program invalid  based on implicit flow
                # due to too few various variables
                return None
        else:
            for e in conds_and_assigns:
                conds = list(e['Condition'])  # all vars used in a condition
                high_in_condition = False

                for var in conds:
                    if var in labels:
                        label = labels[var]
                    else:
                        label = self.rand_label()
                        labels[var] = label
                    if label == 'H':
                        high_in_condition = True

                # all vars of the condition branches
                assigned = list(e['Assigned'])
                for ass in assigned:
                    if high_in_condition:
                        labels[ass] = 'H'
                    elif ass not in labels:
                        labels[ass] = self.rand_label()
        return labels

    def get_labels(self, ast, labels, mixed, assigns, vars, gen_valid):
        # assume that they are already labels set from implicit
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
            # get all assignment indices with at least one var on the right
            # side
            one_ass_invalid = False
            indices_ass = list(
                set(filter(lambda i: len(mixed[i]['Right']) > 0, assigns)))
            while indices_ass:
                rnd_ass_idx = random.choice(indices_ass)
                # remove index of assignment pair to ensure
                # that they are not reused
                indices_ass.remove(rnd_ass_idx)
                left_var = mixed[rnd_ass_idx]['Left']
                # incides of all vars on the right side
                r_vars_idx = list(set(range(len(mixed[rnd_ass_idx]['Right']))))
                while r_vars_idx:
                    rnd_r_var_idx = random.choice(r_vars_idx)
                    r_vars_idx.remove(rnd_r_var_idx)
                    right_var = mixed[rnd_ass_idx]['Right'][rnd_r_var_idx]
                    if right_var == left_var:
                        # cannot set different labels for the same var,
                        # try to choose another right var
                        continue
                    elif left_var in labels and labels[left_var] == 'H':
                        continue
                    elif right_var in labels and labels[right_var] == 'L':
                        continue
                    else:
                        labels[left_var] = 'L'
                        labels[right_var] = 'H'
                        one_ass_invalid = True
                        r_vars_idx = set()
                        # set also labels for other vars in assignments
                        for i in assigns:
                            ass = mixed[i]
                            left_var = ass['Left']
                            if left_var not in labels:
                                labels[left_var] = self.rand_label()

                            for right_var in ass['Right']:
                                if right_var not in labels:
                                    labels[right_var] = self.rand_label()

                        # set labels for other unset vars too
                        for i in vars:
                            var = mixed[i]
                            if var not in labels:
                                labels[var] = self.rand_label()

                if one_ass_invalid:
                    indices_ass = set()
                else:
                    continue
            if not one_ass_invalid:
                # unable to find one var on the right side of an assignment
                # to set invalid. Thus can't generate an invalid program.
                return None
        return labels


def condition_assignments(ast, vars=None):
    """Return vars from assignments and conditions"""
    if vars is None:
        vars = []
    kind = ast.get("Kind")

    if kind == 'Var':
        if len(vars) == 0 or not isinstance(vars[0], set):
            vars.insert(0, set())
        vars[0].add(ast.get("Name"))

    elif kind == 'If':
        condition = condition_assignments(ast.get("Condition"))
        if len(condition) > 0:
            condition = condition[0]

            _then = condition_assignments(ast.get("Then"))[0]
            if 'Assigned' in _then:
                _then = _then['Assigned']

            _else = condition_assignments(ast.get("Else"))[0]
            if 'Assigned' in _else:
                _else = _else['Assigned']

            assigned = set()
            assigned.update(_then)
            assigned.update(_else)

            vars.append({
                'Condition': condition,
                'Assigned': assigned
            })
        return condition_assignments(ast.get("Then"),
                                     condition_assignments(ast.get("Else"),
                                                           vars))
    elif kind == 'While':
        condition = condition_assignments(ast.get("Condition"))
        if len(condition) > 0:
            condition = condition[0]

            assigned = condition_assignments(ast.get("Body"))[0]
            if 'Assigned' in assigned:
                assigned = assigned['Assigned']

            vars.append({
                'Condition': condition,
                'Assigned': assigned
            })
        return condition_assignments(ast.get("Body"), vars)
    elif kind == 'Assign':
        return condition_assignments(ast.get("Left"), vars)
    elif kind != 'Int':
        return condition_assignments(ast.get("Left"),
                                     condition_assignments(ast.get("Right"),
                                                           vars))
    return vars


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


def store(ast, dir, id, to_json=True):
    path_current = os.path.dirname(os.path.realpath(__file__))
    fname = '{} - {}.txt'.format(SEED, id)
    path = os.path.join(path_current,dir)
    
    #print("1.PATH",path)
    if STORE_PICKLE:
        p_path = os.path.join(path_current,"pickle")
        p_path = os.path.join(p_path,dir)
        if not os.path.isdir(p_path):
            os.makedirs(p_path,0o777)
        p_path=os.path.join(p_path,fname)
        with open(p_path,"wb") as f:
            pickle.dump(ast,f)
    if STORE_PRETTYPRINTED_AST:
        if not os.path.isdir(path):
            os.makedirs(path,0o777)
        path=os.path.join(path,fname)
        with open(path, 'w') as out:
            if to_json:
                out.write(json.dumps(ast))
            else:
                out.write(ast)


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
    gen_valid = True
    implicit = ENABLE_IMPLICIT_FLOW
    gen_program(i, gen_valid, implicit)


def gen_program_invalid(i):
    gen_valid = False
    implicit = ENABLE_IMPLICIT_FLOW
    gen_program(i, gen_valid, implicit)


def gen_program(i, gen_valid, implicit):
    ast, _, sec_type = CommandGenerator().gen(gen_valid, implicit)
    t_str = 'implicit' if implicit else 'explicit'
    v_str = 'valid' if gen_valid else 'invalid'
    dir_out = os.path.join("programs",t_str,v_str)
    #dir_out = 'programs/{}/{}'.format(t_str, v_str)
    if PRINT_SECURITY_OUTPUT:
        print('securitychecker outputs {}'.format(
            'valid' if sec_type else 'invalid'))
        print(prettyprint_multiline_indented(ast))
        print('\n')
    store(ast, dir_out + os.sep +'ast', i + 1)
    if PRINT_PATHS:
        print('Generated {}/ast/{} - {}.txt'.format(dir_out, SEED, i + 1))
    if STORE_PRETTYPRINTED_AST:
        store(prettyprint_multiline_indented(ast),
              dir_out + os.sep +'ast-prettyprinted', i + 1, False)
        if PRINT_PATHS:
            print('Generated {}/ast-prettyprinted/{} - {}.txt'.format(dir_out,
                                                                      SEED,
                                                                      i + 1))


def main():
    print('please use generate_programs.py to generate programs.')


if __name__ == "__main__":
    main()

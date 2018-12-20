import codegenerator
import parsy


whitespace = parsy.regex(r'\s*')

lexeme = lambda p: p << whitespace

parens = lambda p: parsy.string("(") >> p << parsy.string(")")


# int ::= 0 | [1-9][0-9]*
int = parsy.string('0').map(int) | parsy.regex(r'[1-9][0-9]*').map(int)

# var ::= [a-zA-Z]+
var = parsy.regex(r'[a-zA-Z]+')

# lbl ::= L | H
label = parsy.string('L') | parsy.string('H')

# lit ::= int | var
lit = int.map(lambda x: {'Kind': 'Int', 'Value': x}) | var.map(lambda x : {'Kind' : 'Var', 'Name' : x})

@parsy.generate
def op():
    e1 = yield exp
    yield whitespace
    op = yield parsy.alt(*map(parsy.string,['+','-','==','<']))
    yield whitespace
    e2 = yield exp
    return {'Kind': kind(op), 'Left': e1, 'Right': e2}

def kind(op):
    if op == '+':
        return 'Add'
    elif op == '-':
        return 'Sub'
    elif op == '==':
        return 'Equal'
    elif op == '<':
        return 'Less'

# exp ::= lit | exp + exp' | exp - exp' | exp = exp' | exp < exp'
exp = lit | parens(op)

# dec ::= lbl var; dec | ""
@parsy.generate
def basicdec():
    l = yield label
    yield whitespace
    v = yield var
    return {'Kind': 'Declare', 'Var': v, 'Label': l}

@parsy.generate
def decs():
    d = yield basicdec
    yield parsy.string(';')
    yield whitespace
    ds = yield dec
    return {'Kind': 'Seq', 'Left': d, 'Right': ds}

dec = decs | basicdec

# | var := exp
@parsy.generate
def assign():
    v = yield var.map(lambda x : {'Kind' : 'Var', 'Name' : x})
    yield whitespace
    yield parsy.string(':=')
    yield whitespace
    e = yield exp
    return {'Kind': 'Assign', 'Left': v, 'Right': e}

# | while exp do cmd
@parsy.generate
def whileP():
    yield parsy.string('while')
    e = yield exp
    yield parsy.string('do')
    c = yield cmd
    return {'Kind': 'While', 'Condition': e, 'Body': c}

# | if exp then cmd else cmd'
@parsy.generate
def ifP():
    yield parsy.string('if')
    yield whitespace
    b = yield exp
    yield whitespace
    yield parsy.string('then')
    yield whitespace
    yield parsy.string('{')
    yield whitespace
    t = yield cmd
    yield whitespace
    yield parsy.string('}')
    yield whitespace
    yield parsy.string('else')
    yield whitespace
    yield parsy.string('{')
    yield whitespace
    e = yield cmd
    yield whitespace
    yield parsy.string('}')
    return {'Kind': 'If', 'Condition': b, 'Then': t, 'Else': e}

basecmd = assign | whileP | ifP

# cmd ::= cmd; cmd
# @parsy.generate
# def seq():
#     c1 = yield cmd
#     yield parsy.string(';')
#     yield whitespace
#     c2 = yield cmd
#     return {'Kind': 'Seq', 'Left': c1, 'Right': c2}

@parsy.generate
def cmds():
    c = yield basecmd
    yield parsy.string(';')
    yield whitespace
    cs = yield cmd
    return {'Kind': 'Seq', 'Left': c, 'Right': cs}

cmd = cmds | basecmd


# prg ::= dec cmd
@parsy.generate
def prog():
    ds = yield dec
    yield parsy.string(';')
    yield whitespace
    c = yield cmd
    return {'Kind': 'Seq', 'Left': ds, 'Right': c}

def testProg1():
    return """H x;
L y;
x := y"""

def testProg2():
    return """H x;
L y;
y := x"""

def testProg3():
    return """H x;
L y;
if (x == 10) then {
    x := y
} else {
    y := 0
}"""

def testProg4():
    return """H x;
if (1 < 2) then {
    x := y
} else {
    y := 0
}"""

def testProg5():
    return """H x;
L y;
if (x < 10) then {
    y := 0
} else {
    if (1 < 2) then {
        y := 0
    } else {
        x := y
    }
}"""

def testProg6():
    return """H x;
L y;
if (x < 10) then {
    y := 0
} else {
    if (1 < 2) then {
        y := 0
    } else {
        if (1 < 2) then {
            y := 0
        } else {
            if (1 < 2) then {
                y := 0
            } else {
                if (1 < 2) then {
                    y := 0
                } else {
                    if (1 < 2) then {
                        y := 0
                    } else {
                        x := y
                    }
                }
            }
        }
    }
}"""

def testProg7():
    return """H x;
L y;
if (x < 10) then {
    y := 0
} else {
    if (1 < 2) then {
        y := 0
    } else {
        if (1 < 2) then {
            y := 0
        } else {
            if (1 < 2) then {
                y := 0
            } else {
                if (1 < 2) then {
                    y := 0
                } else {
                    if (1 < 2) then {
                        y := 0
                    } else {
                        x := 1
                    }
                }
            }
        }
    }
}"""


def parse(program):
    return prog(program,0).value

def test(prog):
    print(prog)
    print(parse(prog))
    print(codegenerator.prettyprint_multiline_indented(parse(prog)))


def main():
    test(testProg1())
    test(testProg2())
    test(testProg3())
    test(testProg4())
    test(testProg5())
    test(testProg7())

if __name__ == '__main__':
    main()

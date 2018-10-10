import random

class Node(object):
    def __init__(self, type, subnodes):
        self.type = type
        self.subnodes = subnodes


Node("+", [Node("a", None), Node("+", [Node("1", None), Node("1", None)])]) #a +(1+1)
Node("-", [Node("b", None), Node("-", [Node("4", None), Node("5", None)])]) #b - (4-5)
Node("=", [Node("4", None), Node("=", [Node("4", None)])]) #4=4

Node("while", [Node("<", [Node("1", None), Node("50", None)]),Node("do", [Node("+",[Node("1",None),Node("2",None)])])])#while 1 < 50 do 1 + 1
Node("if", [Node("<", [Node("1", None), Node("2", None)]), Node(":=", [Node("a", None), Node("2", None)]), Node(":=", [Node("a", None), Node("3", None)])]) #if 1 < 2 then a := 2 else a := 3


def __repr__(self):
    return "type:" + str(self.type) + str(self.subnodes)


def gen_minus(a, b):
    return __repr__(Node("-", [a, b]))


def gen_plus(a, b):
    return __repr__(Node("+", [a, b]))


def gen_if(bed, then, els):
    return __repr__(Node("if", [bed, then, els]))


def gen_while(bed, do):
    return __repr__(Node("while", [bed, do]))


def gen_kleiner_als(a, b):
    return __repr__(Node("<", [a, b]))


def gen_gleich(a, b):
    return __repr__(Node("=", [a, b]))


def random_bed():
    r = random.randint(0, 2)
    a = random.randint(0, 1000)
    b = random.randint(0, 1000)
    if r == 1:
        return gen_kleiner_als(a, b)
    else:
        return gen_gleich(a, b)


def random_instruction():
    r = random.randint(0, 5)
    if r == 0:
        bed = random_bed()
        then = random_instruction()
        els = random_instruction()
        return gen_if(bed, then, els)

    if r == 1:
        bed = random_bed()
        do = random_instruction()
        return gen_while(bed, do)
    if r == 2:
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        return gen_minus(a, b)
    if r == 3:
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        return gen_plus(a, b)
    if r == 4:
        a = random.randint(0, 1000)
        b = random.randint(0, 1000)
        return gen_gleich(a, b)


result = []
for i in range(1):
    result.append(random_instruction())
    print(result)

str_result = []
array_length = len(result)

for x in range(array_length):
    str_result.append(result[x])
    print(str_result)

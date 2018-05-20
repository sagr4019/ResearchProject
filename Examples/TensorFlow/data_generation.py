from collections import defaultdict
import random

class ProgramGen:
    def __init__(self):
        self.params={
            "variables": ["v1","v2","v3","v4"],
            "numbers": ["0","1","2","3","4","5","6","7","8","9"],
            "expressions" : ["<","<=",">",">=","==","!="],
            "operators": ["+","-","*","/"]
        }
        self.tpl={
            "while": ('while( {exprhelper} ){{\n{code}\n}}\n'),
            "if": ('if( {exprhelper} ){{\n{code}\n}}\n'),
            "declaration": ('{var} = {declhelper};\n')
        }
        self.helper={
            "expr": ('{var} {expr} {varnr}'),
            "decl": ('{varnr} {operator} {varnr2}')
        }
        self.end=('return {};')

    def generateHelper(self,_batchsize=100):#creates 100 combinations of expr. and decl.
        declarations = []
        expressions = []
        varnr=self.params["variables"]+self.params["numbers"]
        operators=self.params["operators"]
        for i in range(_batchsize):
            rnd=int(round(random.uniform(0,1)))
            if rnd==0: #extend declaration with operator and number/var
                declarations.append(self.helper["decl"].format(varnr=random.choice(varnr),
                operator=random.choice(operators),
                varnr2=random.choice(varnr)))
            else:
                declarations.append(self.helper["decl"].format(varnr=random.choice(varnr),operator='',varnr2=''))

        for i in range(_batchsize):
            expressions.append(self.helper["expr"].format(var=random.choice(self.params["variables"]),
            expr=random.choice(self.params["expressions"]),
            varnr=random.choice(varnr)))

        return expressions,declarations

    def createRndProgramm(self,_count=50,_los=10,onlyDeclarations=False):
        expression , declarations = self.generateHelper()
        programms = []
        for i in range(_count):
            lines=""
            j=0
            while j <=_los:
                if not onlyDeclarations:
                    element = random.choice(list(self.tpl.keys()))
                else:
                    element = "declaration"
                if element == "while" or element == "if":
                    sub_los=int(round(random.uniform(0,(_los-j)))) #lines of statements for sub program
                    if sub_los > 0:
                        sub_programm_lines=self.createRndProgramm(1,sub_los,True)[0].split("\n")
                        sub_programm=""
                        for curr in range(len(sub_programm_lines)-1):
                            sub_programm+="    %s\n"%sub_programm_lines[curr]
                        lines+=self.tpl[element].format(exprhelper=random.choice(expression),
                        code=sub_programm)
                        j+=sub_los                
                else:
                    lines+=self.tpl[element].format(var=random.choice(self.params["variables"]),
                    declhelper=random.choice(declarations))
                j+=1
            lines+=self.end.format("true")
            programms.append(lines)
        return programms
                    
def main(args):
    tmp = ProgramGen()
    myProgram=tmp.createRndProgramm(3)
    datacnt=1
    for item in myProgram:
        tmpfile = open("data%d.txt"%datacnt,'w')
        tmpfile.write("%s\n" % item)
        datacnt+=1
    
if __name__ == '__main__':
    main("test")
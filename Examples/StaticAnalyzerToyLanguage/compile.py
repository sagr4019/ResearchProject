import io, re, sys

def compile(lines):
    result=""
    pwhile = re.compile("while\(([v0-9!=<>]*)\){")
    pif = re.compile("if\(([v0-9!=<>]*)\){")

    expressions = [[re.compile("v([0-9]*)=([0-9]*)"), lambda m: "setz " + m.group(1) + " " + m.group(2)]]
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)"), lambda m: "setv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("}"), lambda m: "end"])
    expressions.append([re.compile("returntrue"), lambda m: "rettrue"])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\+([0-9]*)"),
                        lambda m: "addzz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\+([0-9]*)"),
                        lambda m: "addvz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\+v([0-9]*)"),
                        lambda m: "addzv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\+v([0-9]*)"),
                        lambda m: "addvv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\-([0-9]*)"),
                        lambda m: "subzz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\-([0-9]*)"),
                        lambda m: "subvz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\-v([0-9]*)"),
                        lambda m: "subzv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\-v([0-9]*)"),
                        lambda m: "subvv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\*([0-9]*)"),
                        lambda m: "multzz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\*([0-9]*)"),
                        lambda m: "multvz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\*v([0-9]*)"),
                        lambda m: "multzv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\*v([0-9]*)"),
                        lambda m: "multvv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\/([0-9]*)"),
                        lambda m: "divzz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\/([0-9]*)"),
                        lambda m: "divvz " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=([0-9]*)\/v([0-9]*)"),
                        lambda m: "divzv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)=v([0-9]*)\/v([0-9]*)"),
                        lambda m: "divvv " + m.group(1) + " " + m.group(2) + " " + m.group(3)])
    expressions.append([re.compile("v([0-9]*)==([0-9]*)"), lambda m: "eqzz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)==v([0-9]*)"), lambda m: "eqvz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)==([0-9]*)"), lambda m: "eqzv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)==v([0-9]*)"), lambda m: "eqvv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)!=([0-9]*)"), lambda m: "neqzz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)!=v([0-9]*)"), lambda m: "neqvz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)!=([0-9]*)"), lambda m: "neqzv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)!=v([0-9]*)"), lambda m: "neqvv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<([0-9]*)"), lambda m: "ltzz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<v([0-9]*)"), lambda m: "ltvz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<([0-9]*)"), lambda m: "ltzv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<v([0-9]*)"), lambda m: "ltvv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>([0-9]*)"), lambda m: "gtzz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>v([0-9]*)"), lambda m: "gtvz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>([0-9]*)"), lambda m: "gtzv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>v([0-9]*)"), lambda m: "gtvv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<=([0-9]*)"), lambda m: "lezz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<=v([0-9]*)"), lambda m: "levz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<=([0-9]*)"), lambda m: "lezv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)<=v([0-9]*)"), lambda m: "levv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>=([0-9]*)"), lambda m: "gezz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>=v([0-9]*)"), lambda m: "gevz " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>=([0-9]*)"), lambda m: "gezv " + m.group(1) + " " + m.group(2)])
    expressions.append([re.compile("v([0-9]*)>=v([0-9]*)"), lambda m: "gevv " + m.group(1) + " " + m.group(2)])

    for line in lines:
        mwhile = pwhile.fullmatch(line)
        if mwhile:
            result += "while\n"
            line = mwhile.group(1)
        else:
            mif = pif.fullmatch(line)
            if mif:
                result += "if\n"
                line = mif.group(1)
        for expr in expressions:
            m = re.fullmatch(expr[0], line)
            if m:
                result += expr[1](m) + "\n"
                break
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compile.py INPUTFILE OUTPUTFILE")
        sys.exit(-1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    with io.open(inputfile) as f:
        code = f.read()

    code = code.replace(" ", "").replace(";", "")
    lines = code.split("\n")
    result = compile(lines)

    with io.open(outputfile, "w") as f:
        f.write(result)

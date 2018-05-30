import io, sys

def asm(lines):
    result=[]

    for line in lines:
        symbols=line.split(" ")

        if symbols[0] == "setz" and len(symbols) == 3:
            result.extend((255, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "setv" and len(symbols) == 3:
            result.extend((254, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "addzz" and len(symbols) == 4:
            result.extend((253, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "addvz" and len(symbols) == 4:
            result.extend((252, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "addzv" and len(symbols) == 4:
            result.extend((251, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "addvv" and len(symbols) == 4:
            result.extend((250, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "subzz" and len(symbols) == 4:
            result.extend((249, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "subvz" and len(symbols) == 4:
            result.extend((248, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "subzv" and len(symbols) == 4:
            result.extend((247, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "subvv" and len(symbols) == 4:
            result.extend((246, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "multzz" and len(symbols) == 4:
            result.extend((245, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "multvz" and len(symbols) == 4:
            result.extend((244, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "multzv" and len(symbols) == 4:
            result.extend((243, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "multvv" and len(symbols) == 4:
            result.extend((242, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "divzz" and len(symbols) == 4:
            result.extend((241, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "divvz" and len(symbols) == 4:
            result.extend((240, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "divzv" and len(symbols) == 4:
            result.extend((239, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "divvv" and len(symbols) == 4:
            result.extend((238, int(symbols[1]), int(symbols[2]), int(symbols[3])))
        elif symbols[0] == "while":
            result.append(237)
        elif symbols[0] == "if":
            result.append(236)
        elif symbols[0] == "end":
            result.append(235)
        elif symbols[0] == "rettrue":
            result.append(234)
        elif symbols[0] == "eqzz" and len(symbols) == 3:
            result.extend((233, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "eqvz" and len(symbols) == 3:
            result.extend((232, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "eqzv" and len(symbols) == 3:
            result.extend((231, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "eqvv" and len(symbols) == 3:
            result.extend((230, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "neqzz" and len(symbols) == 3:
            result.extend((229, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "neqvz" and len(symbols) == 3:
            result.extend((228, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "neqzv" and len(symbols) == 3:
            result.extend((227, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "neqvv" and len(symbols) == 3:
            result.extend((226, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "ltzz" and len(symbols) == 3:
            result.extend((225, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "ltvz" and len(symbols) == 3:
            result.extend((224, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "ltzv" and len(symbols) == 3:
            result.extend((223, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "ltvv" and len(symbols) == 3:
            result.extend((222, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gtzz" and len(symbols) == 3:
            result.extend((221, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gtvz" and len(symbols) == 3:
            result.extend((220, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gtzv" and len(symbols) == 3:
            result.extend((219, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gtvv" and len(symbols) == 3:
            result.extend((218, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "lezz" and len(symbols) == 3:
            result.extend((217, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "levz" and len(symbols) == 3:
            result.extend((216, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "lezv" and len(symbols) == 3:
            result.extend((215, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "levv" and len(symbols) == 3:
            result.extend((214, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gezz" and len(symbols) == 3:
            result.extend((213, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gevz" and len(symbols) == 3:
            result.extend((212, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gezv" and len(symbols) == 3:
            result.extend((211, int(symbols[1]), int(symbols[2])))
        elif symbols[0] == "gevv" and len(symbols) == 3:
            result.extend((210, int(symbols[1]), int(symbols[2])))

    return result

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: asm.py INPUTFILE OUTPUTFILE")
        sys.exit(-1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    with io.open(inputfile) as f:
        lines = f.read().split("\n")

    result = asm(lines)

    print(str(result))

    with io.open(outputfile, "wb") as f:
        f.write(bytes(result))
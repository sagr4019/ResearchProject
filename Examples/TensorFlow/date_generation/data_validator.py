import os
import shutil

source = 'data/unchecked/'
dstValid = "data/valid/"
dstNotValid = "data/not_valid/"

stdvars = ["v1", "v2", "v3", "v4"]


def isValidCode(path):
    vars = []
    if os.path.isfile(path) is True:
        file = open(path, "r")
        line = file.readline()
        while line:
            #print(line)
            for var in stdvars:
                if (var + " = " in line):
                    if (var not in vars):
                        vars.append(var)
                        if (var in line.split(" = ")[1]):
                                # var used on the right side, without being declared
                            return False
            for var in stdvars:
                if (var in line):
                    # print (var + " used")
                    if (var not in vars):
                        #print (var + " used but not declared")
                        return False
            line = file.readline()
        file.close()
        return True
    return "file not exists"


for root, dirs, filenames in os.walk(source):
    for f in filenames:
        path = os.path.join(source, f)
        validCode = isValidCode(path)
        if validCode is False:
            # print (dstNotValid)
            shutil.move(path, dstNotValid + f)
        elif validCode != "file not exists":
            shutil.move(path, dstValid + f)

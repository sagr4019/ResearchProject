import check_security

def assignInvalid():
    # Low x can't read High y
    # L x
    # H y
    # x := y
    codeExample = {"Kind":"Seq", "Left": {"Label":"L", "Var":"x","Kind":"Declare"}, "Right": {"Kind":"Seq", "Left": {"Label":"H", "Var":"y", "Kind": "Declare"}, "Right": {"Kind": "Assign", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"} }}}
    return check_security.check_security(codeExample)

def assignValid():
    # H x
    # L y
    # x = y
    codeExample = {"Kind":"Seq", "Left": {"Label":"H", "Var":"x","Kind":"Declare"}, "Right": {"Kind":"Seq", "Left": {"Label":"L", "Var":"y", "Kind": "Declare"}, "Right": {"Kind": "Assign", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"} }}}
    return check_security.check_security(codeExample)

def varInvalid():
    # Var x is not declared!
    # x
    codeExample = {"Kind": "Var", "Name": "x"}
    return check_security.check_security(codeExample)

def varValid():
    # H x
    # x
    codeExample = {"Kind":"Seq", "Left":{"Kind": "Declare", "Var": "x", "Label": "H"}, "Right": {"Kind": "Var", "Name": "x"}}
    return check_security.check_security(codeExample)

def compareValid_1():
    # result should be H! -> L will go up to H.
    # given declaration! (H x, L y) (to prevent High CMD from "Seq")
    # x == y
    environment = {"x":"H", "y": "L"}
    codeExample = {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}
    return check_security.check_rules(codeExample, environment)

def compareValid_2():
    # result should be H! -> L will go up to H.
    # given declaration! (L x, H y) (to prevent High CMD from "Seq")
    # x == y
    environment = {"x":"L", "y": "H"}
    codeExample = {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}
    return check_security.check_rules(codeExample, environment)

def compareValid_3():
    # result should be L!
    # given declaration! (L x, L y) (to prevent High CMD from "Seq")
    # x == y
    environment = {"x":"L", "y": "L"}
    codeExample = {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}
    return check_security.check_rules(codeExample, environment)

def compareValid_4():
    # result should be H!
    # given declaration! (H x, H y) (to prevent High CMD from "Seq")
    # x == y
    environment = {"x":"H", "y": "H"}
    codeExample = {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}
    return check_security.check_rules(codeExample, environment)

def main():

    # check var statement
    if varInvalid() == None:
        print("[OK] varInvalid is invalid")
    else:
        print("[ERR] varInvalid is valid")

    # check var statement
    if varValid() == None:
        print("[ERR] varValid is invalid")
    else:
        print("[OK] varValid is valid")

    # check invalid assignment
    if assignInvalid() == None:
        print("[OK] assignInvalid is invalid")
    else:
        print("[ERR] assignInvalid is valid")

    # check valid assignment
    if assignValid() == None:
        print("[ERR] assignValid is invalid")
    else:
        print("[OK] assignValid is valid")

    # check comparing
    if compareValid_1() == 'H':
        print("[OK] compareValid_1 is valid")
    else:
        print("[ERR] compareValid_1 is invalid")

    # check comparing
    if compareValid_2() == 'H':
        print("[OK] compareValid_2 is valid")
    else:
        print("[ERR] compareValid_2 is invalid")

    # check comparing
    if compareValid_3() == 'L':
        print("[OK] compareValid_3 is valid")
    else:
        print("[ERR] compareValid_3 is invalid")

    # check comparing
    if compareValid_4() == 'H':
        print("[OK] compareValid_4 is valid")
    else:
        print("[ERR] compareValid_4 is invalid")


if __name__ == "__main__":
    main()

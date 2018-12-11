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

def compareInvalid_1():
    # H can't be compared with L
    # H x
    # L y
    # x == y
    codeExample = {"Kind": "Seq", "Left": {"Kind": "Declare", "Var": "x", "Label": "H"}, "Right": { "Kind": "Seq", "Left": {"Kind": "Declare", "Var": "y", "Label": "L"}, "Right": {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}}}
    return check_security.check_security(codeExample)

def compareInvalid_2():
    # H can't be compared with L
    # L x
    # H y
    # x == y
    codeExample = {"Kind": "Seq", "Left": {"Kind": "Declare", "Var": "x", "Label": "L"}, "Right": { "Kind": "Seq", "Left": {"Kind": "Declare", "Var": "y", "Label": "H"}, "Right": {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}}}
    return check_security.check_security(codeExample)

def compareValid_1():
    # L x
    # L y
    # x == y
    codeExample = {"Kind": "Seq", "Left": {"Kind": "Declare", "Var": "x", "Label": "L"}, "Right": { "Kind": "Seq", "Left": {"Kind": "Declare", "Var": "y", "Label": "L"}, "Right": {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}}}
    return check_security.check_security(codeExample)

def compareValid_2():
    # H x
    # H y
    # x == y
    codeExample = {"Kind": "Seq", "Left": {"Kind": "Declare", "Var": "x", "Label": "H"}, "Right": { "Kind": "Seq", "Left": {"Kind": "Declare", "Var": "y", "Label": "H"}, "Right": {"Kind": "Equal", "Left": {"Kind": "Var", "Name": "x"}, "Right": {"Kind": "Var", "Name": "y"}}}}
    return check_security.check_security(codeExample)

def codeExampleInvalid_1():
    # Invalid Example with two invalid parts
    # Code Example for Seed "272306"
    #
    # H C;
    # H eQX;        <-- Change security label from H to L
    # L c;
    # L u;
    # L FW;
    # L fTkA;       <-- Change security label from L to T
    # while ((fTkA < 162642) - (FW + u)) do {
    #     c := (eQX - C)
    # }
    codeExample = {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'C'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'eQX'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'c'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'u'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'FW'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'fTkA'}, 'Right': {'Kind': 'While', 'Condition': {'Kind': 'Sub', 'Left': {'Kind': 'Less', 'Left': {'Kind': 'Var', 'Name': 'fTkA'}, 'Right': {'Kind': 'Int', 'Value': 162642}}, 'Right': {'Kind': 'Add', 'Left': {'Kind': 'Var', 'Name': 'FW'}, 'Right': {'Kind': 'Var', 'Name': 'u'}}}, 'Body': {'Kind': 'Assign', 'Left': {'Kind': 'Var', 'Name': 'c'}, 'Right': {'Kind': 'Sub', 'Left': {'Kind': 'Var', 'Name': 'eQX'}, 'Right': {'Kind': 'Var', 'Name': 'C'}}}}}}}}}}
    return check_security.check_security(codeExample)

def codeExampleInvalid_2():
    # Another example, obviously invalid
    # D is High and compared with an int (Low)!
    # L u;
    # H D;
    # L r;
    # L t;
    # L s;
    # L X;
    # if ((572624 == 286491) + -14247) then {
    #     D := 853109;
    #     s := ((-597500 == -882673) - (-772568 + -708854));
    #     t := 105894;
    #     r := (D == -139009)
    # } else {
    #     u := (611637 - 93416)
    # }
    codeExample = {'Left': {'Label': 'L', 'Var': 'u', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'H', 'Var': 'D', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'r', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 't', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 's', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'X', 'Kind': 'Declare'}, 'Right': {'Else': {'Left': {'Name': 'u', 'Kind': 'Var'}, 'Right': {'Left': {'Kind': 'Int', 'Value': 611637}, 'Right': {'Kind': 'Int', 'Value': 93416}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Condition': {'Left': {'Left': {'Kind': 'Int', 'Value': 572624}, 'Right': {'Kind': 'Int', 'Value': 286491}, 'Kind': 'Equal'}, 'Right': {'Kind': 'Int', 'Value': -14247}, 'Kind': 'Add'}, 'Kind': 'If', 'Then': {'Left': {'Left': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 853109}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 's', 'Kind': 'Var'}, 'Right': {'Left': {'Left': {'Kind': 'Int', 'Value': -597500}, 'Right': {'Kind': 'Int', 'Value': -882673}, 'Kind': 'Equal'}, 'Right': {'Left': {'Kind': 'Int', 'Value': -772568}, 'Right': {'Kind': 'Int', 'Value': -708854}, 'Kind': 'Add'}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Right': {'Left': {'Left': {'Name': 't', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 105894}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 'r', 'Kind': 'Var'}, 'Right': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': -139009}, 'Kind': 'Equal'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}
    return check_security.check_security(codeExample)

def codeExampleValid_1():
    # Code Example for Seed "272306"
    #
    # H C;
    # H eQX;
    # L c;
    # L u;
    # L FW;
    # L fTkA;
    # while ((fTkA < 162642) - (FW + u)) do {
    #     c := (eQX - C)
    # }
    codeExample = {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'C'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'eQX'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'c'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'u'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'FW'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'fTkA'}, 'Right': {'Kind': 'While', 'Condition': {'Kind': 'Sub', 'Left': {'Kind': 'Less', 'Left': {'Kind': 'Var', 'Name': 'fTkA'}, 'Right': {'Kind': 'Int', 'Value': 162642}}, 'Right': {'Kind': 'Add', 'Left': {'Kind': 'Var', 'Name': 'FW'}, 'Right': {'Kind': 'Var', 'Name': 'u'}}}, 'Body': {'Kind': 'Assign', 'Left': {'Kind': 'Var', 'Name': 'c'}, 'Right': {'Kind': 'Sub', 'Left': {'Kind': 'Var', 'Name': 'eQX'}, 'Right': {'Kind': 'Var', 'Name': 'C'}}}}}}}}}}
    return check_security.check_security(codeExample)


def codeExampleValid_2():
    # Change D from High to Low and r from Low to High -> High can read low
    # L u;
    # L D;
    # H r;
    # L t;
    # L s;
    # L X;
    # if ((572624 == 286491) + -14247) then {
    #     D := 853109;
    #     s := ((-597500 == -882673) - (-772568 + -708854));
    #     t := 105894;
    #     r := (D == -139009)
    # } else {
    #     u := (611637 - 93416)
    # }
    codeExample = {'Left': {'Label': 'L', 'Var': 'u', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'D', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'H', 'Var': 'r', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 't', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 's', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'X', 'Kind': 'Declare'}, 'Right': {'Else': {'Left': {'Name': 'u', 'Kind': 'Var'}, 'Right': {'Left': {'Kind': 'Int', 'Value': 611637}, 'Right': {'Kind': 'Int', 'Value': 93416}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Condition': {'Left': {'Left': {'Kind': 'Int', 'Value': 572624}, 'Right': {'Kind': 'Int', 'Value': 286491}, 'Kind': 'Equal'}, 'Right': {'Kind': 'Int', 'Value': -14247}, 'Kind': 'Add'}, 'Kind': 'If', 'Then': {'Left': {'Left': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 853109}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 's', 'Kind': 'Var'}, 'Right': {'Left': {'Left': {'Kind': 'Int', 'Value': -597500}, 'Right': {'Kind': 'Int', 'Value': -882673}, 'Kind': 'Equal'}, 'Right': {'Left': {'Kind': 'Int', 'Value': -772568}, 'Right': {'Kind': 'Int', 'Value': -708854}, 'Kind': 'Add'}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Right': {'Left': {'Left': {'Name': 't', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 105894}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 'r', 'Kind': 'Var'}, 'Right': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': -139009}, 'Kind': 'Equal'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}
    return check_security.check_security(codeExample)




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

    # check invalid comparing
    if compareInvalid_1() == None:
        print("[OK] compareInvalid_1 is invalid")
    else:
        print("[ERR] compareInvalid_1 is valid")

    # check invalid comparing
    if compareInvalid_2() == None:
        print("[OK] compareInvalid_2 is invalid")
    else:
        print("[ERR] compareInvalid_2 is valid")

    # check valid comparing
    if compareValid_1() == None:
        print("[ERR] compareValid_1 is invalid")
    else:
        print("[OK] compareValid_1 is valid")

    # check valid comparing
    if compareValid_2() == None:
        print("[ERR] compareValid_2 is invalid")
    else:
        print("[OK] compareValid_2 is valid")

    # check valid code example
    if codeExampleValid_1() == None:
        print("[ERR] codeExampleValid_1 is invalid")
    else:
        print("[OK] codeExampleValid_1 is valid")

    # check invalid code example
    if codeExampleInvalid_1() == None:
        print("[OK] codeExampleInvalid_1 is invalid")
    else:
        print("[ERR] codeExampleInvalid_1 is valid")

    # check invalid code example
    if codeExampleInvalid_2() == None:
        print("[OK] codeExampleInvalid_2 is invalid")
    else:
        print("[ERR] codeExampleInvalid_2 is valid")

    # check valid code example
    if codeExampleValid_2() == None:
        print("[ERR] codeExampleValid_2 is invalid")
    else:
        print("[OK] codeExampleValid_2 is valid")


if __name__ == "__main__":
    main()

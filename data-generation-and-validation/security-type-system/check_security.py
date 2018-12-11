def get_label_from_environment(identifier, environment):
    securityClass = None

    for key in environment.keys():
        if key == identifier:
            securityClass = environment[key]

    return securityClass


def convert_label_to_int(securityClass):
    if securityClass == "H":
        return 1
    else:
        return 0


def check_security(ast):
    """Wrapper function to call check_rules without an environment"""
    return check_rules(ast, {})


# check security rules from "secure type system"
def check_rules(node, environment):
    # get the type of the current node
    key = node.get("Kind")

    if key == "Int":
        # return "best fit" type "L"
        return "L"

    elif key == "Var":
        # return security class from environment
        return get_label_from_environment(node.get("Name"), environment)

    elif key == "Declare":
        # add or update entry in dict
        environment[node.get("Var")] = node.get("Label")
        # prevent "None"-Type Error by returning an inconsequenctial label "L" or "H"
        return "L"

    # arithmetic operation
    elif key == "Equal" or key == "Less" or key == "Add" or key == "Sub":
        secType1 = check_rules(node.get("Left"), environment)
        secType2 = check_rules(node.get("Right"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None:
            return None

        if secType1 != secType2:
            return None

        # valid - return bestfit
        return "L"

    elif key == "Assign":
        secType1 = check_rules(node.get("Left"), environment)
        secType2 = check_rules(node.get("Right"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None:
            return None

        # valid - return bestfit as cmd
        if convert_label_to_int(secType1) >= convert_label_to_int(secType2):
            return "H"

        # else -> not valid
        return None

    elif key == "While":
        secType1 = check_rules(node.get("Condition"), environment)
        secType2 = check_rules(node.get("Body"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None:
            return None

        # valid - return bestfit as cmd
        if convert_label_to_int(secType2) >= convert_label_to_int(secType1):
            return "H"

        # else -> not valid
        return None

    elif key == "If":
        secType1 = check_rules(node.get("Condition"), environment)
        secType2 = check_rules(node.get("Then"), environment)
        secType3 = check_rules(node.get("Else"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None or secType3 == None:
            return None

        # valid - return bestfit as cmd
        if convert_label_to_int(secType2) >= convert_label_to_int(secType1) and convert_label_to_int(secType3) >= convert_label_to_int(secType1):
            return "H"

        # else -> not valid
        return None

    # compose commands
    elif key == "Seq":
        secType1 = check_rules(node.get("Left"), environment)
        secType2 = check_rules(node.get("Right"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None:
            return None

        # valid - return bestfit as cmd
        return "H"

    else:
        # unknown kind - not valid
        return None


def main():

    # Valid Example
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

    environment1 = {}

    codeExample1 = {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'C'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'eQX'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'c'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'u'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'FW'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'fTkA'}, 'Right': {'Kind': 'While', 'Condition': {'Kind': 'Sub', 'Left': {'Kind': 'Less', 'Left': {'Kind': 'Var', 'Name': 'fTkA'}, 'Right': {'Kind': 'Int', 'Value': 162642}}, 'Right': {'Kind': 'Add', 'Left': {'Kind': 'Var', 'Name': 'FW'}, 'Right': {'Kind': 'Var', 'Name': 'u'}}}, 'Body': {'Kind': 'Assign', 'Left': {'Kind': 'Var', 'Name': 'c'}, 'Right': {'Kind': 'Sub', 'Left': {'Kind': 'Var', 'Name': 'eQX'}, 'Right': {'Kind': 'Var', 'Name': 'C'}}}}}}}}}}

    secType1 = check_rules(codeExample1, environment1)

    if secType1 == None:
        print("First Example is invalid")
    else:
        print("First Example is valid")

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

    environment2 = {}

    codeExample2 = {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'C'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'eQX'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'c'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'u'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'L', 'Var': 'FW'}, 'Right': {'Kind': 'Seq', 'Left': {'Kind': 'Declare', 'Label': 'H', 'Var': 'fTkA'}, 'Right': {'Kind': 'While', 'Condition': {'Kind': 'Sub', 'Left': {'Kind': 'Less', 'Left': {'Kind': 'Var', 'Name': 'fTkA'}, 'Right': {'Kind': 'Int', 'Value': 162642}}, 'Right': {'Kind': 'Add', 'Left': {'Kind': 'Var', 'Name': 'FW'}, 'Right': {'Kind': 'Var', 'Name': 'u'}}}, 'Body': {'Kind': 'Assign', 'Left': {'Kind': 'Var', 'Name': 'c'}, 'Right': {'Kind': 'Sub', 'Left': {'Kind': 'Var', 'Name': 'eQX'}, 'Right': {'Kind': 'Var', 'Name': 'C'}}}}}}}}}}

    secType2 = check_rules(codeExample2, environment2)

    if secType2 == None:
        print("Second Example is invalid")
    else:
        print("Second Example is valid")

    # third example, obviously invalid
    # L u;
    # H D;
    # L r;
    # L t;
    # L s;
    # L D;
    # if ((572624 == 286491) + -14247) then {
    #     D := 853109;
    #     s := ((-597500 == -882673) - (-772568 + -708854));
    #     t := 105894;
    #     r := (D == -139009)
    # } else {
    #     u := (611637 - 93416)
    # }
    codeExample3 = {'Left': {'Label': 'L', 'Var': 'u', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'H', 'Var': 'D', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'r', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 't', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 's', 'Kind': 'Declare'}, 'Right': {'Left': {'Label': 'L', 'Var': 'D', 'Kind': 'Declare'}, 'Right': {'Else': {'Left': {'Name': 'u', 'Kind': 'Var'}, 'Right': {'Left': {'Kind': 'Int', 'Value': 611637}, 'Right': {'Kind': 'Int', 'Value': 93416}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Condition': {'Left': {'Left': {'Kind': 'Int', 'Value': 572624}, 'Right': {'Kind': 'Int', 'Value': 286491}, 'Kind': 'Equal'}, 'Right': {'Kind': 'Int', 'Value': -14247}, 'Kind': 'Add'}, 'Kind': 'If', 'Then': {'Left': {'Left': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 853109}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 's', 'Kind': 'Var'}, 'Right': {'Left': {'Left': {'Kind': 'Int', 'Value': -597500}, 'Right': {'Kind': 'Int', 'Value': -882673}, 'Kind': 'Equal'}, 'Right': {'Left': {'Kind': 'Int', 'Value': -772568}, 'Right': {'Kind': 'Int', 'Value': -708854}, 'Kind': 'Add'}, 'Kind': 'Sub'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Right': {'Left': {'Left': {'Name': 't', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': 105894}, 'Kind': 'Assign'}, 'Right': {'Left': {'Name': 'r', 'Kind': 'Var'}, 'Right': {'Left': {'Name': 'D', 'Kind': 'Var'}, 'Right': {'Kind': 'Int', 'Value': -139009}, 'Kind': 'Equal'}, 'Kind': 'Assign'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}, 'Kind': 'Seq'}
    secType3 = check_rules(codeExample3, {})

    if secType3 == None:
        print("Third Example is invalid")
    else:
        print("Third Example is valid")


if __name__ == "__main__":
    main()

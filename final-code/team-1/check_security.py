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
        return environment.get(node.get("Name"), None);

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

        if secType1 == "H" or secType2 == "H":
            return "H"

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
    print("Usage:")
    print("import check_security")
    print("With environment use: 'check_rules(ast, environment)'")
    print("Otherwise use: 'check_security(ast)' or 'check_rules(ast, {})'")
    print()
    print("For examples, see 'examples_check_security.py'")

if __name__ == "__main__":
    main()

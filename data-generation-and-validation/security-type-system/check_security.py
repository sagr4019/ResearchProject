
CLASSES = {"N" : 0, "L" : 1, "H" : 2} #None (N), Low (L), High (H)

def get_class(cls): #converts a string of a security class into an int
    if cls in CLASSES.keys():
        return CLASSES[cls]
    else:
        return 0

#returns if the given node is valid towards its security class and the security class itself
def security(node):
    key = list(node.keys())[0] #get the type of the current node
    if key == "Identifier":
        return True, get_class(node["Identifier"]["SClass"])
    elif key == "LiteralInt":
        return True, 0
    elif key == "AddExpr" or key == "SubExpr" or key == "LessExpr" or key == "EqualExpr":
        _, class1 = security(node[key][0])
        _, class2 = security(node[key][1])
        return True, max(class1, class2)
    elif key == "AssignCMD":
        _, id_class = security(node[key][0])
        _, val_class = security(node[key][1])
        return (id_class >= val_class), max(id_class, val_class)
    elif key == "ConcatCMD":
        valid1, class1 = security(node[key][0])
        valid2, class2 = security(node[key][1])
        return (valid1 and valid2), max(class1, class2)
    elif key == "IfCMD":
        _, g_class = security(node[key][0])
        valid1, class1 = security(node[key][1])
        valid2, class2 = security(node[key][2])
        return (valid1 and valid2 and g_class >= class1 and g_class >= class2), max(g_class, class1, class2)
    elif key == "WhileCMD":
        _, g_class = security(node[key][0])
        cmd_valid, cmd_class = security(node[key][1])
        return (cmd_valid and g_class >= cmd_class), max(g_class, cmd_class)
    else:
        return True, 0


def main():
    # o := 1 + 1
    good = {"AssignCMD": [{'Identifier': {'Value': 'o', 'SClass': 'H'}},
                          {"AddExpr": [{"LiteralInt": "1"}, {"LiteralInt": "1"}]}]}
    print(security(good))
    # b : = 4 - a + 2
    good2 = {"AssignCMD": [{'Identifier': {'Value': 'b', 'SClass': 'H'}}, {
        "AddExpr": [{"SubExpr": [{"LiteralInt": "4"}, {"Identifier": {"Value": "a", "SClass": "H"}}]},
                    {"LiteralInt": "2"}]}]}
    print(security(good2))

    good3 = {"ConcatCMD": [good, good2]}
    print(security(good3))

    # if a < 4 then good() else good2()
    good4 = {"IfCMD": [{"LessExpr": [{"Identifier": {"Value": "a", "SClass": "H"}}, {"LiteralInt": "4"}]}, good, good2]}
    print(security(good4))

    # while x == 3 do good3()
    good4 = {"WhileCMD": [{"EqualExpr": [{"Identifier": {"Value": "x", "SClass": "H"}}, {"LiteralInt": "3"}]}, good3]}
    print(security(good4))


if __name__ == "__main__":
    main()
# global storage for identifiers
identifierStorage = []

def get_class(identifier): #converts a string of a security class into an int
    global identifierStorage

    securityClass = None

    for e in identifierStorage:
        if e["Identifier"] == identifier:
            securityClass = e["Security"]

    # debug - print identifier if not found
    #if securityClass == None:
    #    print(identifier)

    if securityClass == "H":
        return 1
    else:
        return 0

#returns if the given node is valid towards its security class and the security class itself
def security(node):
    global identifierStorage

    key = node.get("Kind") #get the type of the current node

    if key == "Concat":
        valid1, class1 = security(node.get("Left"))
        valid2, class2 = security(node.get("Right"))
        return (valid1 and valid2), max(class1, class2)
    elif key == "Assign":
        _, id_class = security(node.get("Left"))
        _, val_class = security(node.get("Right"))
        return (id_class >= val_class), max(id_class, val_class)
    elif key == "Var":
        return True, get_class(node.get("Value"))
    elif key == "While":
        _, g_class = security(node.get("Condition"))
        cmd_valid, cmd_class = security(node.get("Do"))
        return (cmd_valid and g_class >= cmd_class), max(g_class, cmd_class)
    elif key == "Int":
        return True, 0
    elif key == "If":
        _, g_class = security(node.get("Condition"))
        valid1, class1 = security(node.get("Then"))
        valid2, class2 = security(node.get("Else"))
        return (valid1 and valid2 and g_class >= class1 and g_class >= class2), max(g_class, class1, class2)
    elif key == "Equal" or key == "Less" or key == "Add" or key == "Sub":
        _, class1 = security(node.get("Left"))
        _, class2 = security(node.get("Right"))
        return True, max(class1, class2)
    else:
        return True, 0

def main():
    global identifierStorage

    # predefine identifierStorage
    identifierStorage = [{"Identifier": "G", "Security": "L"}, {"Identifier": "X", "Security": "L"}, {"Identifier": "n", "Security": "L"}, {"Identifier": "J", "Security": "L"}, {"Identifier": "R", "Security": "L"}, {"Identifier": "i", "Security": "L"}, {"Identifier": "f", "Security": "L"}, {"Identifier": "v", "Security": "L"}, {"Identifier": "K", "Security": "L"}]

    # (((G := X) ;  (n := (-16782 < (((J < ((R + -314341) + -776311)) == i) + f)))) ;  (v := K))
    newExample = {'Kind': 'Concat',
     'Left': {'Kind': 'Concat',
              'Left': {'Kind': 'Assign',
                       'Left': {'Kind': 'Var', 'Value': 'G'},
                       'Right': {'Kind': 'Var', 'Value': 'X'}},
              'Right': {'Kind': 'Assign',
                        'Left': {'Kind': 'Var', 'Value': 'n'},
                        'Right': {'Kind': 'Less',
                                  'Left': {'Kind': 'Int', 'Value': -16782},
                                  'Right': {'Kind': 'Add',
                                            'Left': {'Kind': 'Equal',
                                                     'Left': {'Kind': 'Less',
                                                              'Left': {'Kind': 'Var',
                                                                       'Value': 'J'},
                                                              'Right': {'Kind': 'Add',
                                                                        'Left': {'Kind': 'Add',
                                                                                 'Left': {'Kind': 'Var',
                                                                                          'Value': 'R'},
                                                                                 'Right': {'Kind': 'Int',
                                                                                           'Value': -314341}},
                                                                        'Right': {'Kind': 'Int',
                                                                                  'Value': -776311}}},
                                                     'Right': {'Kind': 'Var',
                                                               'Value': 'i'}},
                                            'Right': {'Kind': 'Var',
                                                      'Value': 'f'}}}}},
     'Right': {'Kind': 'Assign',
               'Left': {'Kind': 'Var', 'Value': 'v'},
               'Right': {'Kind': 'Var', 'Value': 'K'}}}
    print(security(newExample))

    # rewrite identifierStorage
    identifierStorage = [{"Identifier": "U", "Security": "L"}, {"Identifier": "Q", "Security": "L"}, {"Identifier": "Z", "Security": "L"}, {"Identifier": "N", "Security": "L"}, {"Identifier": "V", "Security": "L"}, {"Identifier": "v", "Security": "L"}, {"Identifier": "H", "Security": "L"}, {"Identifier": "d", "Security": "L"}, {"Identifier": "q", "Security": "L"}]

    # (while (-20806) do {(if (-314201) then {(U := 638624)} else {(Q := 762253)} ;  (Z := -831119))} ;  (N := ((v < (((d == (431958 + V)) < H) - -73817)) == q)))
    testExample = {"Kind": "Concat",
     "Left": {"Condition": {"Kind": "Int", "Value": -20806},
              "Do": {"Kind": "Concat",
                     "Left": {"Condition": {"Kind": "Int", "Value": -314201},
                              "Else": {"Kind": "Assign",
                                       "Left": {"Kind": "Var", "Value": "Q"},
                                       "Right": {"Kind": "Int", "Value": 762253}},
                              "Kind": "If",
                              "Then": {"Kind": "Assign",
                                       "Left": {"Kind": "Var", "Value": "U"},
                                       "Right": {"Kind": "Int", "Value": 638624}}},
                     "Right": {"Kind": "Assign",
                               "Left": {"Kind": "Var", "Value": "Z"},
                               "Right": {"Kind": "Int", "Value": -831119}}},
              "Kind": "While"},
     "Right": {"Kind": "Assign",
               "Left": {"Kind": "Var", "Value": "N"},
               "Right": {"Kind": "Equal",
                         "Left": {"Kind": "Less",
                                  "Left": {"Kind": "Var", "Value": "v"},
                                  "Right": {"Kind": "Sub",
                                            "Left": {"Kind": "Less",
                                                     "Left": {"Kind": "Equal",
                                                              "Left": {"Kind": "Var",
                                                                       "Value": "d"},
                                                              "Right": {"Kind": "Add",
                                                                        "Left": {"Kind": "Int",
                                                                                 "Value": 431958},
                                                                        "Right": {"Kind": "Var",
                                                                                  "Value": "V"}}},
                                                     "Right": {"Kind": "Var",
                                                               "Value": "H"}},
                                            "Right": {"Kind": "Int",
                                                      "Value": -73817}}},
                         "Right": {"Kind": "Var", "Value": "q"}}}}
    print(security(testExample))

if __name__ == "__main__":
    main()

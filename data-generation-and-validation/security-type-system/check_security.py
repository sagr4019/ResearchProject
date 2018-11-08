def get_class(identifier, identifierStorage):  # converts a string of a security class into an int
    securityClass = None

    for e in identifierStorage:
        if e["Identifier"] == identifier:
            securityClass = e["Security"]

    # debug - print identifier if not found
    # if securityClass == None:
    #    print(identifier)

    if securityClass == "H":
        return 1
    else:
        return 0

# returns if the given node is valid towards its security class and the security class itself


def security(node, identifierStorage):
    key = node.get("Kind")  # get the type of the current node

    if key == "Seq":
        valid1, class1 = security(node.get("Left"), identifierStorage)
        valid2, class2 = security(node.get("Right"), identifierStorage)
        return (valid1 and valid2), max(class1, class2)
    elif key == "Assign":
        _, id_class = security(node.get("Left"), identifierStorage)
        _, val_class = security(node.get("Right"), identifierStorage)
        return (id_class >= val_class), max(id_class, val_class)
    elif key == "Var":
        return True, get_class(node.get("Name"), identifierStorage)
    elif key == "While":
        _, g_class = security(node.get("Condition"), identifierStorage)
        cmd_valid, cmd_class = security(node.get("Body"), identifierStorage)
        return (cmd_valid and g_class >= cmd_class), max(g_class, cmd_class)
    elif key == "Int":
        return True, 0
    elif key == "Null":
        return True, 0
    elif key == "If":
        _, g_class = security(node.get("Condition"), identifierStorage)
        valid1, class1 = security(node.get("Then"), identifierStorage)
        valid2, class2 = security(node.get("Else"), identifierStorage)
        return (valid1 and valid2 and g_class >= class1 and g_class >= class2), max(g_class, class1, class2)
    elif key == "Equal" or key == "Less" or key == "Add" or key == "Sub":
        _, class1 = security(node.get("Left"), identifierStorage)
        _, class2 = security(node.get("Right"), identifierStorage)
        return True, max(class1, class2)
    else:
        return True, 0


def main():

    # Code Example:
    #
    # vni := Null;
    # Mwq := Null;
    # MIz := Null;
    # tlZ := Null;
    # fnv := Null;
    # scB := Null;
    # gLV := Null;
    # cTl := Null;
    # zbJ := Null;
    # bVw := Null;
    # Tld := Null;
    # wtE := Null;
    # vtM := Null;
    # Akj := Null;
    # mIR := Null;
    # lXy := Null;
    # pyI := Null;
    # if ((-220292 - pyI) == (-144045 + lXy)) then {
    #     while ((-652173 + -393283) < mIR) do {
    #         if Akj then {
    #             vtM := (wtE + (Tld == bVw))
    #         } else {
    #             zbJ := (cTl == -750395)
    #         };
    #         while (gLV == scB) do {
    #             fnv := ((tlZ == 314507) == (510220 - -830218))
    #         };
    #         MIz := 553064
    #     }
    # } else {
    #     Mwq := (681213 < vni)
    # }

    # pre-define identifierStorage
    identifierStorage = [{'Identifier': 'pyI', 'Security': 'L'},
                         {'Identifier': 'lXy', 'Security': 'L'},
                         {'Identifier': 'mIR', 'Security': 'L'},
                         {'Identifier': 'Akj', 'Security': 'L'},
                         {'Identifier': 'vtM', 'Security': 'L'},
                         {'Identifier': 'wtE', 'Security': 'L'},
                         {'Identifier': 'Tld', 'Security': 'L'},
                         {'Identifier': 'bVw', 'Security': 'L'},
                         {'Identifier': 'zbJ', 'Security': 'L'},
                         {'Identifier': 'cTl', 'Security': 'L'},
                         {'Identifier': 'gLV', 'Security': 'L'},
                         {'Identifier': 'scB', 'Security': 'L'},
                         {'Identifier': 'fnv', 'Security': 'L'},
                         {'Identifier': 'tlZ', 'Security': 'L'},
                         {'Identifier': 'MIz', 'Security': 'L'},
                         {'Identifier': 'Mwq', 'Security': 'L'},
                         {'Identifier': 'vni', 'Security': 'L'}]
    newExample = {'Kind': 'Seq',
                  'Left': {'Kind': 'Assign',
                           'Left': {'Kind': 'Var', 'Name': 'vni'},
                           'Right': {'Kind': 'Null', 'Value': 'Null'}},
                  'Right': {'Kind': 'Seq',
                            'Left': {'Kind': 'Assign',
                                     'Left': {'Kind': 'Var', 'Name': 'Mwq'},
                                     'Right': {'Kind': 'Null', 'Value': 'Null'}},
                            'Right': {'Kind': 'Seq',
                                      'Left': {'Kind': 'Assign',
                                               'Left': {'Kind': 'Var', 'Name': 'MIz'},
                                               'Right': {'Kind': 'Null', 'Value': 'Null'}},
                                      'Right': {'Kind': 'Seq',
                                                'Left': {'Kind': 'Assign',
                                                         'Left': {'Kind': 'Var', 'Name': 'tlZ'},
                                                         'Right': {'Kind': 'Null',
                                                                   'Value': 'Null'}},
                                                'Right': {'Kind': 'Seq',
                                                          'Left': {'Kind': 'Assign',
                                                                   'Left': {'Kind': 'Var',
                                                                            'Name': 'fnv'},
                                                                   'Right': {'Kind': 'Null',
                                                                             'Value': 'Null'}},
                                                          'Right': {'Kind': 'Seq',
                                                                    'Left': {'Kind': 'Assign',
                                                                             'Left': {'Kind': 'Var',
                                                                                      'Name': 'scB'},
                                                                             'Right': {'Kind': 'Null',
                                                                                       'Value': 'Null'}},
                                                                    'Right': {'Kind': 'Seq',
                                                                              'Left': {'Kind': 'Assign',
                                                                                       'Left': {'Kind': 'Var',
                                                                                                'Name': 'gLV'},
                                                                                       'Right': {'Kind': 'Null',
                                                                                                 'Value': 'Null'}},
                                                                              'Right': {'Kind': 'Seq',
                                                                                        'Left': {'Kind': 'Assign',
                                                                                                 'Left': {'Kind': 'Var',
                                                                                                          'Name': 'cTl'},
                                                                                                 'Right': {'Kind': 'Null',
                                                                                                           'Value': 'Null'}},
                                                                                        'Right': {'Kind': 'Seq',
                                                                                                  'Left': {'Kind': 'Assign',
                                                                                                           'Left': {'Kind': 'Var',
                                                                                                                    'Name': 'zbJ'},
                                                                                                           'Right': {'Kind': 'Null',
                                                                                                                     'Value': 'Null'}},
                                                                                                  'Right': {'Kind': 'Seq',
                                                                                                            'Left': {'Kind': 'Assign',
                                                                                                                     'Left': {'Kind': 'Var',
                                                                                                                              'Name': 'bVw'},
                                                                                                                     'Right': {'Kind': 'Null',
                                                                                                                               'Value': 'Null'}},
                                                                                                            'Right': {'Kind': 'Seq',
                                                                                                                      'Left': {'Kind': 'Assign',
                                                                                                                               'Left': {'Kind': 'Var',
                                                                                                                                        'Name': 'Tld'},
                                                                                                                               'Right': {'Kind': 'Null',
                                                                                                                                         'Value': 'Null'}},
                                                                                                                      'Right': {'Kind': 'Seq',
                                                                                                                                'Left': {'Kind': 'Assign',
                                                                                                                                         'Left': {'Kind': 'Var',
                                                                                                                                                  'Name': 'wtE'},
                                                                                                                                         'Right': {'Kind': 'Null',
                                                                                                                                                   'Value': 'Null'}},
                                                                                                                                'Right': {'Kind': 'Seq',
                                                                                                                                          'Left': {'Kind': 'Assign',
                                                                                                                                                   'Left': {'Kind': 'Var',
                                                                                                                                                            'Name': 'vtM'},
                                                                                                                                                   'Right': {'Kind': 'Null',
                                                                                                                                                             'Value': 'Null'}},
                                                                                                                                          'Right': {'Kind': 'Seq',
                                                                                                                                                    'Left': {'Kind': 'Assign',
                                                                                                                                                             'Left': {'Kind': 'Var',
                                                                                                                                                                      'Name': 'Akj'},
                                                                                                                                                             'Right': {'Kind': 'Null',
                                                                                                                                                                       'Value': 'Null'}},
                                                                                                                                                    'Right': {'Kind': 'Seq',
                                                                                                                                                              'Left': {'Kind': 'Assign',
                                                                                                                                                                       'Left': {'Kind': 'Var',
                                                                                                                                                                                'Name': 'mIR'},
                                                                                                                                                                       'Right': {'Kind': 'Null',
                                                                                                                                                                                 'Value': 'Null'}},
                                                                                                                                                              'Right': {'Kind': 'Seq',
                                                                                                                                                                        'Left': {'Kind': 'Assign',
                                                                                                                                                                                 'Left': {'Kind': 'Var',
                                                                                                                                                                                          'Name': 'lXy'},
                                                                                                                                                                                 'Right': {'Kind': 'Null',
                                                                                                                                                                                           'Value': 'Null'}},
                                                                                                                                                                        'Right': {'Kind': 'Seq',
                                                                                                                                                                                  'Left': {'Kind': 'Assign',
                                                                                                                                                                                           'Left': {'Kind': 'Var',
                                                                                                                                                                                                    'Name': 'pyI'},
                                                                                                                                                                                           'Right': {'Kind': 'Null',
                                                                                                                                                                                                     'Value': 'Null'}},
                                                                                                                                                                                  'Right': {'Condition': {'Kind': 'Equal',
                                                                                                                                                                                                          'Left': {'Kind': 'Sub',
                                                                                                                                                                                                                   'Left': {'Kind': 'Int',
                                                                                                                                                                                                                            'Value': -220292},
                                                                                                                                                                                                                   'Right': {'Kind': 'Var',
                                                                                                                                                                                                                             'Name': 'pyI'}},
                                                                                                                                                                                                          'Right': {'Kind': 'Add',
                                                                                                                                                                                                                    'Left': {'Kind': 'Int',
                                                                                                                                                                                                                             'Value': -144045},
                                                                                                                                                                                                                    'Right': {'Kind': 'Var',
                                                                                                                                                                                                                              'Name': 'lXy'}}},
                                                                                                                                                                                            'Else': {'Kind': 'Assign',
                                                                                                                                                                                                     'Left': {'Kind': 'Var',
                                                                                                                                                                                                              'Name': 'Mwq'},
                                                                                                                                                                                                     'Right': {'Kind': 'Less',
                                                                                                                                                                                                               'Left': {'Kind': 'Int',
                                                                                                                                                                                                                        'Value': 681213},
                                                                                                                                                                                                               'Right': {'Kind': 'Var',
                                                                                                                                                                                                                         'Name': 'vni'}}},
                                                                                                                                                                                            'Kind': 'If',
                                                                                                                                                                                            'Then': {'Body': {'Kind': 'Seq',
                                                                                                                                                                                                              'Left': {'Kind': 'Seq',
                                                                                                                                                                                                                       'Left': {'Condition': {'Kind': 'Var',
                                                                                                                                                                                                                                              'Name': 'Akj'},
                                                                                                                                                                                                                                'Else': {'Kind': 'Assign',
                                                                                                                                                                                                                                         'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                  'Name': 'zbJ'},
                                                                                                                                                                                                                                         'Right': {'Kind': 'Equal',
                                                                                                                                                                                                                                                   'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                            'Name': 'cTl'},
                                                                                                                                                                                                                                                   'Right': {'Kind': 'Int',
                                                                                                                                                                                                                                                             'Value': -750395}}},
                                                                                                                                                                                                                                'Kind': 'If',
                                                                                                                                                                                                                                'Then': {'Kind': 'Assign',
                                                                                                                                                                                                                                         'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                  'Name': 'vtM'},
                                                                                                                                                                                                                                         'Right': {'Kind': 'Add',
                                                                                                                                                                                                                                                   'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                            'Name': 'wtE'},
                                                                                                                                                                                                                                                   'Right': {'Kind': 'Equal',
                                                                                                                                                                                                                                                             'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                                      'Name': 'Tld'},
                                                                                                                                                                                                                                                             'Right': {'Kind': 'Var',
                                                                                                                                                                                                                                                                       'Name': 'bVw'}}}}},
                                                                                                                                                                                                                       'Right': {'Body': {'Kind': 'Assign',
                                                                                                                                                                                                                                          'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                   'Name': 'fnv'},
                                                                                                                                                                                                                                          'Right': {'Kind': 'Equal',
                                                                                                                                                                                                                                                    'Left': {'Kind': 'Equal',
                                                                                                                                                                                                                                                             'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                                      'Name': 'tlZ'},
                                                                                                                                                                                                                                                             'Right': {'Kind': 'Int',
                                                                                                                                                                                                                                                                       'Value': 314507}},
                                                                                                                                                                                                                                                    'Right': {'Kind': 'Sub',
                                                                                                                                                                                                                                                              'Left': {'Kind': 'Int',
                                                                                                                                                                                                                                                                       'Value': 510220},
                                                                                                                                                                                                                                                              'Right': {'Kind': 'Int',
                                                                                                                                                                                                                                                                        'Value': -830218}}}},
                                                                                                                                                                                                                                 'Condition': {'Kind': 'Equal',
                                                                                                                                                                                                                                               'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                                        'Name': 'gLV'},
                                                                                                                                                                                                                                               'Right': {'Kind': 'Var',
                                                                                                                                                                                                                                                         'Name': 'scB'}},
                                                                                                                                                                                                                                 'Kind': 'While'}},
                                                                                                                                                                                                              'Right': {'Kind': 'Assign',
                                                                                                                                                                                                                        'Left': {'Kind': 'Var',
                                                                                                                                                                                                                                 'Name': 'MIz'},
                                                                                                                                                                                                                        'Right': {'Kind': 'Int',
                                                                                                                                                                                                                                  'Value': 553064}}},
                                                                                                                                                                                                     'Condition': {'Kind': 'Less',
                                                                                                                                                                                                                   'Left': {'Kind': 'Add',
                                                                                                                                                                                                                            'Left': {'Kind': 'Int',
                                                                                                                                                                                                                                     'Value': -652173},
                                                                                                                                                                                                                            'Right': {'Kind': 'Int',
                                                                                                                                                                                                                                      'Value': -393283}},
                                                                                                                                                                                                                   'Right': {'Kind': 'Var',
                                                                                                                                                                                                                             'Name': 'mIR'}},
                                                                                                                                                                                                     'Kind': 'While'}}}}}}}}}}}}}}}}}}}

    print(security(newExample, identifierStorage))

    # rewrite identifierStorage
    # identifierStorage = [{"Identifier": "U", "Security": "L"}, {"Identifier": "Q", "Security": "L"}, {"Identifier": "Z", "Security": "L"}, {"Identifier": "N", "Security": "L"}, {"Identifier": "V", "Security": "L"}, {"Identifier": "v", "Security": "L"}, {"Identifier": "H", "Security": "L"}, {"Identifier": "d", "Security": "L"}, {"Identifier": "q", "Security": "L"}]

    # (while (-20806) do {(if (-314201) then {(U := 638624)} else {(Q := 762253)} ;  (Z := -831119))} ;  (N := ((v < (((d == (431958 + V)) < H) - -73817)) == q)))
    # testExample = {"Kind": "Concat",
    #                "Left": {"Condition": {"Kind": "Int", "Value": -20806},
    #                         "Do": {"Kind": "Concat",
    #                                "Left": {"Condition": {"Kind": "Int", "Value": -314201},
    #                                         "Else": {"Kind": "Assign",
    #                                                  "Left": {"Kind": "Var", "Value": "Q"},
    #                                                  "Right": {"Kind": "Int", "Value": 762253}},
    #                                         "Kind": "If",
    #                                         "Then": {"Kind": "Assign",
    #                                                  "Left": {"Kind": "Var", "Value": "U"},
    #                                                  "Right": {"Kind": "Int", "Value": 638624}}},
    #                                "Right": {"Kind": "Assign",
    #                                          "Left": {"Kind": "Var", "Value": "Z"},
    #                                          "Right": {"Kind": "Int", "Value": -831119}}},
    #                         "Kind": "While"},
    #                "Right": {"Kind": "Assign",
    #                          "Left": {"Kind": "Var", "Value": "N"},
    #                          "Right": {"Kind": "Equal",
    #                                    "Left": {"Kind": "Less",
    #                                             "Left": {"Kind": "Var", "Value": "v"},
    #                                             "Right": {"Kind": "Sub",
    #                                                       "Left": {"Kind": "Less",
    #                                                                "Left": {"Kind": "Equal",
    #                                                                         "Left": {"Kind": "Var",
    #                                                                                  "Value": "d"},
    #                                                                         "Right": {"Kind": "Add",
    #                                                                                   "Left": {"Kind": "Int",
    #                                                                                            "Value": 431958},
    #                                                                                   "Right": {"Kind": "Var",
    #                                                                                             "Value": "V"}}},
    #                                                                "Right": {"Kind": "Var",
    #                                                                          "Value": "H"}},
    #                                                       "Right": {"Kind": "Int",
    #                                                                 "Value": -73817}}},
    #                                    "Right": {"Kind": "Var", "Value": "q"}}}}
    # print(security(testExample, identifierStorage))

if __name__ == "__main__":
    main()

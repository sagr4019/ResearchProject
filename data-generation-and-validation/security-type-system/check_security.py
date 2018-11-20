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


    # @Salvos: I don't think that this is correct, but to work with my code i had to introduce the key Declare...
    elif key == "Declare":
        return get_label_from_environment(node.get("Var"), environment)


    # arithmetic operation
    elif key == "Equal" or key == "Less" or key == "Add" or key == "Sub":
        secType1 = check_rules(node.get("Left"), environment)
        secType2 = check_rules(node.get("Right"), environment)

        # check if none-types exists -> not valid
        if secType1 == None or secType2 == None:
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
        if convert_label_to_int(secType2) >= convert_label_to_int(secType1):
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

    # Code Example:
    #
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

    # pre-define environment
    environment = {'pyI': 'L',
                     'lXy': 'L',
                     'mIR': 'L',
                     'Akj': 'L',
                     'vtM': 'L',
                     'wtE': 'L',
                     'Tld': 'L',
                     'bVw': 'L',
                     'zbJ': 'L',
                     'cTl': 'L',
                     'gLV': 'L',
                     'scB': 'L',
                     'fnv': 'L',
                     'tlZ': 'L',
                     'MIz': 'L',
                     'Mwq': 'L',
                     'vni': 'L'}

    codeExample = {'Kind': 'Seq',
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

    secType = check_rules(codeExample, environment)

    if secType == None:
        print("Invalid")
    else:
        print("Valid")

if __name__ == "__main__":
    main()

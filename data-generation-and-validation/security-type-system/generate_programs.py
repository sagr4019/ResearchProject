import codegenerator as c

# number of valid programs to generate
PROGRAMS_TO_GENERATE_VALID = 5

# number of invalid programs to generate
PROGRAMS_TO_GENERATE_INVALID = 5

# True to generate implicit programs or
# False to generate explicit programs
c.ENABLE_IMPLICIT_FLOW = True

# True if prettyprinted AST should also be stored
c.STORE_PRETTYPRINTED_AST = True

# True for printing paths in console, e. g.
c.PRINT_PATHS = True


def main():
    list(map(c.gen_program_valid, range(PROGRAMS_TO_GENERATE_VALID)))
    print('')
    list(map(c.gen_program_invalid, range(PROGRAMS_TO_GENERATE_INVALID)))


if __name__ == "__main__":
    main()

import argparse
import sys
sys.path.append('../../data-generation-and-validation/security-type-system')
import codegenerator
import codeparser
import models
import main as m
import keras
import tokenizer

NO_PROGRAMS = 10000
MAX_TOKEN_LENGTH = 50
IMPLICIT = True

def test_programs(count, valid, implicit, validator):
    no_wrong_classified = 0
    for i in range(count):
        tokens = []
        while (len(tokens) <= 0 or len(tokens) > MAX_TOKEN_LENGTH):
            ast, _, _ = codegenerator.CommandGenerator().gen(valid, implicit)
            tokens = tokenizer.Tokenizer().tokenize(ast)
        x = m.token_to_vec(tokens, MAX_TOKEN_LENGTH)
        y = validator.predict(x.reshape((1, MAX_TOKEN_LENGTH)))

        res_valid = round(y[0][1] * 100, 2)
        res_invalid = round(y[0][0] * 100, 2)
        if (valid and y[0][1] < y[0][0]) or (not valid and y[0][1] > y[0][0]):
            no_wrong_classified += 1
            print('\n\n{}. program NOT correctly classified'.format(
                i))
            print('Number of tokens: {}'.format(len(tokens)))
            validStr = str(res_valid)
            invalidStr = str(res_invalid)
            print("Valid:  ", formatOutput(validStr, invalidStr), "%")
            print("Invalid:", formatOutput(invalidStr, validStr), "%")
            print(codegenerator.prettyprint_multiline_indented(ast))
    return no_wrong_classified

def main():
    print('\nTesting {} {} programs'.format(NO_PROGRAMS,  'implicit' if IMPLICIT else 'explicit'))
    print('Max token length: {}'.format(MAX_TOKEN_LENGTH))

    print("Loading model...")
    path_model = 'models/weights_indirect_flow_iteration2.hdf5'
    validator = models.LSTMValidator(MAX_TOKEN_LENGTH, len(m.TOKEN2VEC) + 1, "adam")
    validator.load_weights(path_model)

    no_wrong_classified = 0
    no_wrong_classified += test_programs(NO_PROGRAMS // 2, True, IMPLICIT, validator)
    no_wrong_classified += test_programs(NO_PROGRAMS // 2, False, IMPLICIT, validator)

    print('\n\n{} of {} wrong classified'.format(
        no_wrong_classified, NO_PROGRAMS))


def formatOutput(str, refStr):
    return ' ' * (max(len(str), len(refStr)) - len(str)) + str


if __name__ == "__main__":
    main()

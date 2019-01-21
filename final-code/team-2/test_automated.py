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
VALID = True
IMPLICIT = True
# threshold value of incorrect classification
THRESHOLD_PERCENTAGE = 50


def main():
    print('\nTesting {} {} {} programs'.format(NO_PROGRAMS,
                                               'implicit' if IMPLICIT else 'explicit',
                                               'valid' if VALID else 'invalid'))
    print('Max token length: {}'.format(MAX_TOKEN_LENGTH))
    print('Threshold percentage of incorrect classification: {}'.format(
        THRESHOLD_PERCENTAGE))

    print("Loading model...")
    path_model = 'models/weights_indirect_flow_iteration2.hdf5'
    validator = models.LSTMValidator(
        MAX_TOKEN_LENGTH, len(m.TOKEN2VEC) + 1, "adam")
    validator.load_weights(path_model)

    no_tested = 0
    no_wrong_classified = 0
    while no_tested < NO_PROGRAMS:
        ast, _, _ = codegenerator.CommandGenerator().gen(VALID, IMPLICIT)
        tokens = tokenizer.Tokenizer().tokenize(ast)
        if len(tokens) <= MAX_TOKEN_LENGTH:
            no_tested += 1
            x = m.token_to_vec(tokens, MAX_TOKEN_LENGTH)
            y = validator.predict(x.reshape((1, MAX_TOKEN_LENGTH)))

            res_valid = round(y[0][1] * 100, 2)
            res_invalid = round(y[0][0] * 100, 2)
            if (not VALID and res_invalid < THRESHOLD_PERCENTAGE) or (VALID and res_valid < THRESHOLD_PERCENTAGE):
                no_wrong_classified += 1
                print('\n\n{}. program NOT correctly classified'.format(
                    no_tested))
                print('Number of tokens: {}'.format(len(tokens)))
                validStr = str(res_valid)
                invalidStr = str(res_invalid)
                print("Valid:  ", formatOutput(validStr, invalidStr), "%")
                print("Invalid:", formatOutput(invalidStr, validStr), "%")
                print(codegenerator.prettyprint_multiline_indented(ast))
    print('\n\n{} of {} wrong classified'.format(
        no_wrong_classified, no_tested))


def formatOutput(str, refStr):
    return ' ' * (max(len(str), len(refStr)) - len(str)) + str


if __name__ == "__main__":
    main()

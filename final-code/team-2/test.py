import argparse
import sys
sys.path.append('../../data-generation-and-validation/security-type-system')
import codegenerator
import codeparser
import models
import main as m
import keras
import tokenizer

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--model", required=True, help="Trained weight file")
    argparser.add_argument("--length", required=True, type=int, help="Maximum length of tokenized programs")
    args = argparser.parse_args()

    print("Loading model...")

    validator = models.LSTMValidator(args.length, len(m.TOKEN2VEC)+1, "adam")
    validator.load_weights(args.model)

    '''print("Generating program...")
    valid = True

    tokens = []
    ast = None
    while(len(tokens) <= 0 or len(tokens) > args.length):
        ast, _, _ = codegenerator.CommandGenerator().gen(valid)
        tokens = tokenizer.Tokenizer().tokenize(ast)
    print(codegenerator.prettyprint_multiline_indented(ast))'''

    print("Converting program...")

    prog = open('programs/invalid/if-stack2.txt', 'r').read()
    ast = codeparser.parse(prog)

    print(codegenerator.prettyprint_multiline_indented(ast))

    tokens = tokenizer.Tokenizer().tokenize(ast)
    print("Number of tokens: " + str(len(tokens)))

    x = m.token_to_vec(tokens, args.length)

    print("Testing program...")

    y = validator.predict(x.reshape((1, args.length)))

    print("Valid:", round(y[0][1] * 100, 2), "%")
    print("Invalid", round(y[0][0] * 100, 2), "%")

if __name__ == "__main__":
    main()

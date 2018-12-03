import argparse
import sys
sys.path.append('../../data-generation-and-validation/security-type-system')
import codegenerator
import models
import main as m
import keras
import tokenizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Trained weight file")
    parser.add_argument("--length", required=True, type=int, help="Maximum length of tokenized programs")
    args = parser.parse_args()

    print("Loading model...")

    validator = models.LSTMValidator(args.length, len(m.TOKEN2VEC)+1, keras.models.optimizers.Adam())
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

    ast = {"Kind" : "Seq",
           "Left" : {"Kind": "Declare", "Label": "H", "Var": "x"},
           "Right" : {
               "Kind" : "Seq",
               "Left" : {"Kind": "Declare", "Label": "H", "Var": "y"},
               "Right" : {
                   "Kind" : "Seq",
                   "Left" : {
                       "Kind": "Assign",
                       "Left": {"Kind": "Var", "Name": "x"},
                       "Right" : {"Kind": "Int", "Value": "5"},
                   },
                   "Right" : {
                       "Kind" : "If",
                       "Condition" : {"Kind" : "Less", "Left" : {"Kind": "Var", "Name": "x"}, "Right" : {"Kind": "Int", "Value": "10"}},
                       "Then" : {
                           "Kind": "Assign",
                           "Left": {"Kind": "Var", "Name": "y"},
                           "Right" : {"Kind": "Var", "Name": "x"},
                        },
                       "Else" : {
                           "Kind": "Assign",
                           "Left": {"Kind": "Var", "Name": "y"},
                           "Right" : {"Kind": "Int", "Value": "0"},
                        }
                   }
               }
           }
           }

    print(codegenerator.prettyprint_multiline_indented(ast))

    tokens = tokenizer.Tokenizer().tokenize(ast)

    x = m.token_to_vec(tokens, args.length)

    print(x)

    print("Testing program...")

    y = validator.predict(x.reshape((1, args.length)))

    print(y)

if __name__ == "__main__":
    main()
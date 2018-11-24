import json
import os
import glob
import errno
from Tokenizer import Tokenizer


def load_programs(ttype):
    """
    Load and return programs (asts) by type (valid/invalid) as a list of dicts
    with keys 'ast' and 'tokens'
    """
    asts_and_tokens = []
    dir_programs = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        "../../data-generation-and-validation/security-type-system/programs"))
    dir = dir_programs + '/' + ttype
    files = glob.glob(dir + '/*')
    for name in files:
            try:
                with open(name) as f:
                    ast = json.loads(f.read())
                    tokens = Tokenizer().parse(ast)
                    asts_and_tokens.append({
                        'ast': ast,
                        'tokens': tokens
                    })
            except IOError as exc:
                if exc.errno != errno.EISDIR:  # ignore if dir
                    raise
    return asts_and_tokens


def main():
    valid_asts_and_tokens = load_programs('valid')
    print(valid_asts_and_tokens[0]['ast'])
    print('\n')
    print(valid_asts_and_tokens[0]['tokens'])
    print('\n')
    invalid_asts_and_tokens = load_programs('invalid')
    print(invalid_asts_and_tokens[0]['ast'])
    print('\n')
    print(invalid_asts_and_tokens[0]['tokens'])


if __name__ == "__main__":
    main()

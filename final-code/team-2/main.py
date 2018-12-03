import json
import os
import glob
import errno
from tokenizer import Tokenizer
import numpy as np
import keras
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
import models

TOKEN2VEC = {
    'L': 1, 'H': 2, ';': 3, ':=': 4, 'int': 5, '(': 6, ')': 7, 'if': 8, 'then': 9, 'else': 10, 'while': 11, 'do': 12,
    '{': 13, '}': 14, '==': 15, '<': 16, '+': 17, '-': 18, 'a': 18, 'b': 19, 'c': 20, 'd': 21, 'e': 22, 'f': 23,
    'g': 24, 'h': 25, 'i': 26, 'j': 27, 'k': 28, 'l': 29, 'm': 30, 'n': 31, 'o': 32, 'p': 33, 'q': 34, 'r': 35, 's': 36,
    't': 37, 'u': 38, 'v': 39, 'w': 40, 'x': 41, 'y': 42, 'z': 43, 'A': 44, 'B': 45, 'C': 46, 'D': 47, 'E': 48, 'F': 49,
    'G': 50, 'I': 51, 'J': 52, 'K': 53, 'M': 54, 'N': 55, 'O': 56, 'P': 57, 'Q': 58, 'R': 59, 'S': 60, 'T': 61, 'U': 62,
    'V': 63, 'W': 64, 'X': 65, 'Y': 66, 'Z': 67
}


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
                    tokens = Tokenizer().tokenize(ast)
                    asts_and_tokens.append({
                        'ast': ast,
                        'tokens': tokens
                    })
            except IOError as exc:
                if exc.errno != errno.EISDIR:  # ignore if dir
                    raise
    return asts_and_tokens


def token_to_vec(tokens, length):
    result = np.zeros(length)
    for i in range(len(tokens)):
        if i < length:
            if tokens[i] in TOKEN2VEC:
                result[i] = TOKEN2VEC[tokens[i]]
            else:
                print("Warning: Unknown token ", tokens[i])
        else:
            print("Warning: Length exceeds maximum length")
            break
    return result


def main():
    epochs = 100
    batch_size = 64
    max_length = 100
    test_ratio = 0.1

    print("Loading programs")
    valid = load_programs("valid")
    invalid = load_programs("invalid")

    print("Filtering too large programs...")

    valid_valid = [] #valid programs not exceeding max_length
    for i in range(len(valid)):
        if len(valid[i]["tokens"]) <= max_length:
            valid_valid.append(valid[i])
    valid = valid_valid

    valid_invalid = [] #invalid programs not exceeding max_length
    for i in range(len(invalid)):
        if len(invalid[i]["tokens"]) <= max_length:
            valid_invalid.append(invalid[i])
    invalid = valid_invalid

    print("Valid count: ", len(valid))
    print("Invalid count: ", len(invalid))

    #equalize number of samples
    if len(valid) > len(invalid):
        valid = valid[:len(invalid)]
    elif len(invalid) > len(valid):
        invalid = invalid[:len(valid)]

    x_valid = np.zeros((len(valid), max_length))
    x_invalid = np.zeros((len(invalid), max_length))

    print("Converting valid...")

    for i in range(len(valid)):
        x_valid[i] = token_to_vec(valid[i]["tokens"], max_length)

    y_valid = np.ones(len(valid))

    print("Converting invalid...")

    for i in range(len(invalid)):
        x_invalid[i] = token_to_vec(invalid[i]["tokens"], max_length)

    y_invalid = np.zeros(len(invalid))

    print("Splitting data...")

    test_count = int(len(x_valid) * test_ratio)

    x = np.concatenate((x_valid[:-test_count], x_invalid[:-test_count]))
    y = np.concatenate((y_valid[:-test_count], y_invalid[:-test_count]))

    test_x = np.concatenate((x_valid[-test_count:], x_invalid[-test_count:]))
    test_y = np.concatenate((y_valid[-test_count:], y_invalid[-test_count:]))

    y = to_categorical(y, 2)
    test_y = to_categorical(test_y, 2)

    print("Creating model...")

    optimizer = keras.optimizers.Adam()
    validator = models.LSTMValidator(max_length, len(TOKEN2VEC) + 1, optimizer)

    print("Training...")

    filepath = "models\lstm1-{epoch:02d}--{val_acc:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]

    validator.fit(x, y, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=callbacks_list, validation_data=(test_x, test_y))


if __name__ == "__main__":
    main()

import sys, io
import keras
from preprocess_data_seq_embed import string_to_sequence
from train_seq_embed import sequences_to_onehot
from keras.models import load_model

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: check.py MODEL_FILE PROGRAM")
        sys.exit(-1)

    max_length = 128
    symbol_count = 19

    print("Setting up network...")

    model = load_model(sys.argv[1])

    print("Preparing program...")

    symbols = ["v1", "v2", "v3", "v4", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ";", "while", "if", "(", ")", "{", "}", "return", "true", " ", "=", "<", ">", "!", "+", "*", "-", "/"]

    symbols_to_index = {}
    index = 1
    for i in range(len(symbols)):  # create a dictionary with an index(number) for each symbol
        s = symbols[i]
        if s >= "0" and s < "9":
            symbols_to_index[s] = index
        elif s in ["<", ">", "+", "*", "-", "/"]:
            symbols_to_index[s] = index
        else:
            symbols_to_index[s] = index
            index += 1

    with open(sys.argv[2]) as f:
        program=f.read()

    program = program.replace("\n", "")
    program = string_to_sequence(program, symbols, symbols_to_index, [" "])

    if len(program) < max_length:
        program = program + ([0] * (max_length - len(program)))
    elif len(program) > max_length:
        print("Warning program size exceeding max_length!")
        program = program[:max_length]

    programs = sequences_to_onehot([program], max_length, symbol_count)

    print("Checking program...")

    result = model.predict(programs)

    print(result)
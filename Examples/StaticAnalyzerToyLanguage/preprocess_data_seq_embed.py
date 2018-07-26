import sys, io, os
import numpy as np

#load all files from the two specified directories
def load_data_from_dirs(valid_dir, not_valid_dir):
    valid = []
    for file in os.listdir(valid_dir):
        with io.open(os.path.join(valid_dir, file)) as f:
            valid.append(f.read())
    not_valid = []
    for file in os.listdir(not_valid_dir):
        with io.open(os.path.join(not_valid_dir, file)) as f:
            not_valid.append(f.read())
    return valid, not_valid

#converts a string into a sequence of symbol / word indices
def string_to_sequence(str, symbols, symbols_to_index, ignore_symbols):
    result=[]
    while(str != ""):
        for s in symbols:
            if str[:len(s)] == s:
                i=symbols_to_index[s]
                if not s in ignore_symbols: #ignore spaces
                    result.append(i)
                str=str[len(s):]
    return result


if __name__ == "__main__":

    symbols = ["v1", "v2", "v3", "v4", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ";", "while", "if", "(", ")", "{", "}", "return", "true", " ", "=", "<", ">", "!" ,"+", "*", "-", "/"]

    max_length = 128

    symbols_to_index = {}
    index=1
    for i in range(len(symbols)): #create a dictionary with an index(number) for each symbol
        s = symbols[i]
        if s >= "0" and s < "9":
            symbols_to_index[s] = index
        elif s in ["<", ">","+", "*", "-", "/"]:
            symbols_to_index[s] = index
        else:
            symbols_to_index[s] = index
            index+=1

    if len(sys.argv) < 4:
        print("Usage preprocess_data.py VALID_DIR NOT_VALID_DIR OUTPUTFILE")
        sys.exit(-1)

    print("Loading data...")

    valid, not_valid = load_data_from_dirs(sys.argv[1], sys.argv[2]) #load samples from disk

    print("Converting data...")

    for i in range(len(valid)):
        valid[i] = valid[i].replace("\n", "")
        valid[i] = string_to_sequence(valid[i], symbols, symbols_to_index, [" "])
        if len(valid[i]) < max_length: #pad data to max length
            valid[i] = valid[i] + ([0] * (max_length - len(valid[i])))
        elif len(valid[i]) > max_length:
            print("Warning: Data sequence length exceeds maximum length!")
            valid[i] = valid[i][:max_length]

    for i in range(len(not_valid)):
        not_valid[i] = not_valid[i].replace("\n", "")
        not_valid[i] = string_to_sequence(not_valid[i], symbols, symbols_to_index, [" "])
        if len(not_valid[i]) < max_length: #pad data to max length
            not_valid[i] = not_valid[i] + ([0] * (max_length - len(not_valid[i])))
        elif len(not_valid[i]) > max_length:
            print("Warning: Data sequence length exceeds maximum length!")
            not_valid[i] = not_valid[i][:max_length]

    print("Generating labels...")

    valid_y = []
    for i in range(len(valid)):
        valid_y.append(1)

    not_valid_y = []
    for i in range(len(not_valid)):
        not_valid_y.append(0)

    print("Saving data...")

    np.savez(sys.argv[3], x_valid=np.array(valid), x_not_valid=np.array(not_valid), y_not_valid=np.array(not_valid_y), y_valid=np.array(valid_y), max_length=np.array([max_length]))

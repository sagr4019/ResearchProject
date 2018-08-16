import os, io, sys
import compile, asm
import numpy as np
from lib import load_data_from_dirs, transform_arrays, pad_array

def process_string(str, max_length):
    str = str.replace(" ", "").replace("\n", "")
    result = [ord(c) for c in str]
    if len(result) < max_length:
        result = pad_array(result, max_length - len(result), 0)
    elif len(result) > max_length:
        print("Warning: Sample size greater then max length!")
        result=result[max_length:]
    return result

#remove whitespaces and semicolons and split on newlines
def process_strings(array, max_length):
    for i in range(len(array)):
        array[i] = process_string(array[i], max_length)

#compiles string to byte code array
def compile_string(str, max_length):
    return process_string(str, max_length)

if __name__ == "__main__":

    max_length = 500

    if len(sys.argv) < 4:
        print("Usage preprocess_data.py VALID_DIR NOT_VALID_DIR OUTPUTFILE")
        sys.exit(-1)

    print("Loading data...")

    valid, not_valid = load_data_from_dirs(sys.argv[1], sys.argv[2]) #load samples from disk

    print("Processing strings...")

    #preprocess strings
    process_strings(valid, max_length)
    process_strings(not_valid, max_length)

    print(valid)

    print("Transforming arrays...")

    #merge arrays into one, create label array
    x_valid, x_not_valid, y_valid, y_not_valid = transform_arrays(valid, not_valid)

    print("Saving data...")

    #save data to disk
    np.savez(sys.argv[3], x_valid=np.array(x_valid), x_not_valid=np.array(x_not_valid), y_not_valid=np.array(y_not_valid), y_valid=np.array(y_valid), max_length=np.array([max_length]))

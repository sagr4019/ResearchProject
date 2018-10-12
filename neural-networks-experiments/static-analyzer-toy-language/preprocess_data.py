import os, io, sys
import compile, asm
import numpy as np

from lib import load_data_from_dirs, transform_arrays, pad_array

def process_string(str):
    return str.replace(" ", "").replace(";", "").split("\n")

#remove whitespaces and semicolons and split on newlines
def process_strings(array):
    for i in range(len(array)):
        array[i] = process_string(array[i])

#compile the source code of the array into bytecode
def compile_array(array, max_length):
    for i in range(len(array)):
        code = asm.asm(compile.compile(array[i]).split("\n"))
        if (len(code) < max_length):  # pad to max_length
            code = pad_array(code, max_length - len(code), 0)
        elif len(code) > max_length:
            print("Warning: data sample size exceeds max length!")
            code = code[:max_length]
        array[i] = code

#compiles string to byte code array
def compile_string(str, max_length):
    str = process_string(str)
    result = asm.asm(compile.compile(str).split("\n"))
    if len(result) < max_length:
        result = pad_array(result, max_length - len(result), 0)
    return result

if __name__ == "__main__":

    max_length = 200

    if len(sys.argv) < 4:
        print("Usage preprocess_data.py VALID_DIR NOT_VALID_DIR OUTPUTFILE")
        sys.exit(-1)

    print("Loading data...")

    valid, not_valid = load_data_from_dirs(sys.argv[1], sys.argv[2]) #load samples from disk

    print("Processing strings...")

    #preprocess strings
    process_strings(valid)
    process_strings(not_valid)

    print("Compiling code...")

    #compile source code to byte code
    compile_array(valid, max_length)
    compile_array(not_valid, max_length)

    print("Transforming arrays...")

    #merge arrays into one, create label array
    x_valid, x_not_valid, y_valid, y_not_valid = transform_arrays(valid, not_valid)

    print("Saving data...")

    #save data to disk
    np.savez(sys.argv[3], x_valid=np.array(x_valid), x_not_valid=np.array(x_not_valid), y_not_valid=np.array(y_not_valid), y_valid=np.array(y_valid), max_length=np.array([max_length]))

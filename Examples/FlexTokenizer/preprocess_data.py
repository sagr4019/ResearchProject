import subprocess
import os, io, sys
import numpy as np

THISPATH = os.path.dirname(os.path.realpath(__file__))

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

def process_tokenizer(array):

    # create subprocess for the tokenizer
    proc = subprocess.Popen([THISPATH+"/tokenizer"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    #proc.wait()

    temp = ""
    # pipe code to the tokenizer
    for i in range(len(array)):
        temp = temp + " "+ array[i]
        #proc.stdin.write(array[i])

    output = proc.communicate(input=bytes(temp, 'UTF-8'))[0].decode("utf-8")

    proc.kill()

    # read output, remove the last char ('') and split by linebreak
    output = output[:-1].split("\n")

    # convert strings to integer
    for i in range(len(output)):
        output[i] = int(output[i])

    return output


#merge both arrays into one, provide labels (0 = invalid, 1 = valid)
def transform_arrays(valid, not_valid):
    y_valid=[]
    y_not_valid=[]
    for v in valid:
        y_valid.append(1)
    for nv in not_valid:
        y_not_valid.append(0)
    return valid, not_valid, y_valid, y_not_valid


if __name__ == "__main__":

    max_length = 200

    if len(sys.argv) < 4:
        print("Usage preprocess_data.py VALID_DIR NOT_VALID_DIR OUTPUTFILE")
        sys.exit(-1)

    print("Loading data...")

    valid, not_valid = load_data_from_dirs(sys.argv[1], sys.argv[2]) #load samples from disk


    valid = process_tokenizer(valid)
    not_valid = process_tokenizer(not_valid)

    print("Transforming arrays...")

    #merge arrays into one, create label array
    x_valid, x_not_valid, y_valid, y_not_valid = transform_arrays(valid, not_valid)

    print("Saving data...")

    #save data to disk
    np.savez(sys.argv[3], x_valid=np.array(x_valid), x_not_valid=np.array(x_not_valid), y_not_valid=np.array(y_not_valid), y_valid=np.array(y_valid), max_length=np.array([max_length]))

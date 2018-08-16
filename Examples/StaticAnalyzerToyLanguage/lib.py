import io, os
import numpy

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

#merge both arrays into one, provide labels (0 = invalid, 1 = valid)
def transform_arrays(valid, not_valid):
    y_valid=[]
    y_not_valid=[]
    for v in valid:
        y_valid.append(1)
    for nv in not_valid:
        y_not_valid.append(0)
    return valid, not_valid, y_valid, y_not_valid

def pad_array(array, length, value):
    return array + (length * [value])

#split dataset into test and training data
def split_dataset(x, y, factor):
    data_len = len(x)

    test_len = int(data_len / factor)

    train_x, test_x = (x[:data_len - test_len], x[data_len - test_len:])
    train_y, test_y = (y[:data_len - test_len], y[data_len - test_len:])
    return train_x, test_x, train_y, test_y

#randomly distiribute data
def shuffle(x, y):
    randomize = numpy.arange(len(x))
    numpy.random.shuffle(randomize)

    result_x = []
    result_y = []

    for i in range(len(randomize)):
        result_x.append(x[randomize[i]])
        result_y.append(y[randomize[i]])

    return numpy.array(result_x), numpy.array(result_y)
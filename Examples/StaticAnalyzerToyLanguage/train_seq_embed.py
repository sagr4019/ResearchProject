import sys
import keras
from keras.layers import Dense, LSTM, Activation
import numpy as np
from keras.utils import to_categorical

valid_sample = "v1 = 2;\nv2 = v1;\nwhile( v2 == 2){\nv2 = 5;}\nreturn true;\n"
invalid_sample = "v1 = 2;\nv2 = v3;\nwhile( v2 == 2){\nv2 = 5;}\nreturn true;\n"

def split_dataset(x, y, factor):
    data_len = len(x)

    test_len = int(data_len / factor)

    train_x, test_x = (x[:data_len - test_len], x[data_len - test_len:])
    train_y, test_y = (y[:data_len - test_len], y[data_len - test_len:])
    return train_x, test_x, train_y, test_y

def shuffle(x, y):
    randomize = np.arange(len(x))
    np.random.shuffle(randomize)

    result_x = []
    result_y = []

    for i in range(len(randomize)):
        result_x.append(x[randomize[i]])
        result_y.append(y[randomize[i]])

    return np.array(result_x), np.array(result_y)

# converts training and test data into one hot vectors
def sequences_to_onehot(array, max_length, symbol_count):
    result = np.zeros((len(array), max_length, symbol_count))
    for i in range(len(array)):
        for j in range(max_length):
            result[i][j][array[i][j]] = 1
    return result



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: train.py DATA_FILE")
        sys.exit(-1)

    max_length = 600
    symbol_count = 32
    num_hidden = 128
    batch_size = 64
    epochs = 100

    print("Loading data...")

    data =  np.load(sys.argv[1]) #load training data from file

    train_x_valid = data["x_valid"]
    train_x_not_valid = data["x_not_valid"]
    train_y_valid = data["y_valid"]
    train_y_not_valid = data["y_not_valid"]

    #split data, make sure test data contains all types of samples (valid and not valid ones)
    train_x_valid, test_x_valid, train_y_valid, test_y_valid = split_dataset(train_x_valid, train_y_valid, 5)
    train_x_not_valid, test_x_not_valid, train_y_not_valid, test_y_not_valid = split_dataset(train_x_not_valid, train_y_not_valid, 5)

    train_x = np.concatenate((train_x_valid, train_x_not_valid))
    train_y = np.concatenate((train_y_valid, train_y_not_valid))
    test_x = np.concatenate((test_x_valid, test_x_not_valid))
    test_y = np.concatenate((test_y_valid, test_y_not_valid))


    train_x, train_y = shuffle(train_x, train_y)
    test_x, test_y = shuffle(test_x, test_y)

    #convert y to one-hot encoding
    train_y = to_categorical(train_y, 2)
    test_y = to_categorical(test_y, 2)

    train_x = sequences_to_onehot(train_x, max_length, symbol_count)
    test_x = sequences_to_onehot(test_x, max_length, symbol_count)
    #train_x = np.expand_dims(train_x, axis=2)
    #test_x = np.expand_dims(test_x, axis=2)

    print("Setting up network...")

    model = keras.Sequential()
    model.add(keras.layers.LSTM(num_hidden, input_shape=(max_length, symbol_count)))
    #model.add(keras.layers.LSTM(num_hidden))
    model.add(keras.layers.Dense(2))
    model.add(keras.layers.Activation('softmax'))

    optimizer = keras.optimizers.RMSprop(0.1)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['categorical_accuracy'])

    model.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(test_x, test_y))

    score = model.evaluate(test_x, test_y, verbose=0)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

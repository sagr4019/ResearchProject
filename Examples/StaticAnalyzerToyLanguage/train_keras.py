import numpy, sys
import preprocess_data
import keras
import keras.layers as layers
import keras.callbacks
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
    randomize = numpy.arange(len(x))
    numpy.random.shuffle(randomize)

    result_x = []
    result_y = []

    for i in range(len(randomize)):
        result_x.append(x[randomize[i]])
        result_y.append(y[randomize[i]])

    return numpy.array(result_x), numpy.array(result_y)



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: train.py DATA_FILE")
        sys.exit(-1)

    max_length = 200
    num_hidden = 128
    batch_size = 64
    epochs = 200

    valid_sample = numpy.array(preprocess_data.compile_string(valid_sample, max_length))
    invalid_sample = numpy.array(preprocess_data.compile_string(invalid_sample, max_length))
    valid_sample = numpy.expand_dims(valid_sample, axis=0)
    invalid_sample = numpy.expand_dims(invalid_sample, axis=0)
    valid_sample = numpy.expand_dims(valid_sample, axis=2)
    invalid_sample = numpy.expand_dims(invalid_sample, axis=2)
    valid_sample.astype("float32")
    invalid_sample.astype("float32")


    print("Loading data...")

    data =  numpy.load(sys.argv[1]) #load training data from file

    train_x_valid = data["x_valid"]
    train_x_not_valid = data["x_not_valid"]
    train_y_valid = data["y_valid"]
    train_y_not_valid = data["y_not_valid"]

    #split data, make sure test data contains all types of samples (valid and not valid ones)
    train_x_valid, test_x_valid, train_y_valid, test_y_valid = split_dataset(train_x_valid, train_y_valid, 5)
    train_x_not_valid, test_x_not_valid, train_y_not_valid, test_y_not_valid = split_dataset(train_x_not_valid, train_y_not_valid, 5)

    train_x = numpy.concatenate((train_x_valid, train_x_not_valid))
    train_y = numpy.concatenate((train_y_valid, train_y_not_valid))
    test_x = numpy.concatenate((test_x_valid, test_x_not_valid))
    test_y = numpy.concatenate((test_y_valid, test_y_not_valid))


    train_x, train_y = shuffle(train_x, train_y)
    test_x, test_y = shuffle(test_x, test_y)

    #convert y to one-hot encoding
    #train_y = to_categorical(train_y, 2)
    #test_y = to_categorical(test_y, 2)

    train_x = train_x.astype("float32")
    test_x = test_x.astype("float32")

    #train_x /= 255
    #test_x /= 255

    train_x = numpy.expand_dims(train_x, axis=2)
    test_x = numpy.expand_dims(test_x, axis=2)

    #print(test_x[0].reshape((200)))

    print("Setting up network...")

    model = keras.models.Sequential()
    #model.add(keras.layers.Embedding(input_dim=256, output_dim=64, input_length=max_length))
    model.add(keras.layers.LSTM(num_hidden, batch_input_shape=(1,1,1), stateful=True))
    #model.add(keras.layers.LSTM(num_hidden, return_sequences=True))
    #model.add(keras.layers.LSTM(num_hidden))
    model.add(keras.layers.Dense(1))
    model.add(keras.layers.Activation('sigmoid'))

    #model.add(layers.Conv1D(32, 3, activation="relu", input_shape=(max_length,1)))
    #model.add(layers.Conv1D(64, 3, activation="relu"))
    #model.add(layers.Flatten())
    #model.add(layers.Dense(128, activation="relu"))
    #model.add(layers.Dense(2, activation="softmax"))

    optimizer = keras.optimizers.RMSprop(0.1)
    model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])

    print("Training...")

    class ResetStatesCallback(keras.callbacks.Callback):
        def __init__(self):
            self.counter = 0

        def on_batch_begin(self, batch, logs={}):
            if self.counter % max_length == 0:
                self.model.reset_states()
            self.counter += 1


    x = numpy.expand_dims(numpy.expand_dims(train_x.flatten(), axis=1), axis=1)
    y = numpy.expand_dims(numpy.array([[v] * max_length for v in train_y.flatten()]).flatten(), axis=1)

    model.fit(x, y, batch_size=1, epochs=epochs, verbose=1, callbacks=[ResetStatesCallback()])

    #score = model.evaluate(test_x, test_y, verbose=0)

    #print('Test loss:', score[0])
    #print('Test accuracy:', score[1])

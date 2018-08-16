import numpy, sys
import preprocess_data
import keras
import keras.layers as layers
import keras.callbacks
from keras.utils import to_categorical
from lib import split_dataset, shuffle

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: train.py DATA_FILE")
        sys.exit(-1)

    max_length = 200
    num_hidden = 128
    batch_size = 64
    epochs = 200


    print("Loading data...")

    data =  numpy.load(sys.argv[1]) #load training data from file

    train_x_valid = data["x_valid"]
    train_x_not_valid = data["x_not_valid"]
    train_y_valid = data["y_valid"]
    train_y_not_valid = data["y_not_valid"]
    max_length = data["max_length"][0]

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

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K #tensorflow?

batch_size = 128 # training data splitting -> influences training time / accuracy
num_classes = 10 # output categories
epochs = 12 # number of training cycles

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# preprocessing of data

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols) # convert data into input shape
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols) # convert data into input shape
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices | example: 8 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# create model

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape)) # Convolutional layer
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2))) # pooling -> reduce data size
model.add(Dropout(0.25)) # prevent overfitting
model.add(Flatten()) # ?
model.add(Dense(128, activation='relu')) # ?
model.add(Dropout(0.5)) #prevent overfitting
model.add(Dense(num_classes, activation='softmax')) # express categorization in probabilities

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test)) # execute training

score = model.evaluate(x_test, y_test, verbose=0) # evaluate training / model

# print results
print('Test loss:', score[0])
print('Test accuracy:', score[1])
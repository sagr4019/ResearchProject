import keras
from keras.layers import Dense, LSTM, Embedding

class LSTMValidator(keras.Sequential):
    EMBEDDING_FEATURES=32
    LSTM_UNITS=256
    def __init__(self, max_length, max_index, optimizer):
        super().__init__()
        self.max_length = max_length
        self.max_index = max_index
        self.optimizer = optimizer

        self.add(Embedding(max_index, LSTMValidator.EMBEDDING_FEATURES, input_length=max_length))
        self.add(LSTM(LSTMValidator.LSTM_UNITS, input_shape=(max_length, LSTMValidator.EMBEDDING_FEATURES)))
        self.add(Dense(2, activation="softmax"))

        self.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
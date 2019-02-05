import main as module_main
import numpy as np
from keras.utils import to_categorical
from keras.layers import Input, Embedding, LSTM, TimeDistributed, Dense
from keras import Model
import h5py

def main():
    epochs = 1
    batch_size = 64
    max_length = 50
    embedding_size = 32
    lstm_cells = 50


    print("Loading programs")
    valid = module_main.load_programs("implicit", "valid")
    invalid = module_main.load_programs("implicit", "invalid")

    print("Valid count: ", len(valid))
    print("Invalid count: ", len(invalid))

    print("Filtering too large programs...")

    valid_valid = [] #valid programs not exceeding max_length
    for i in range(len(valid)):
        if len(valid[i]["tokens"]) <= max_length:
            valid_valid.append(valid[i])
    valid = valid_valid

    valid_invalid = [] #invalid programs not exceeding max_length
    for i in range(len(invalid)):
        if len(invalid[i]["tokens"]) <= max_length:
            valid_invalid.append(invalid[i])
    invalid = valid_invalid

    print("Valid count: ", len(valid))
    print("Invalid count: ", len(invalid))

    #equalize number of samples
    if len(valid) > len(invalid):
        valid = valid[:len(invalid)]
    elif len(invalid) > len(valid):
        invalid = invalid[:len(valid)]

    x_valid = np.zeros((len(valid), max_length))
    x_invalid = np.zeros((len(invalid), max_length))

    print("Converting valid...")

    for i in range(len(valid)):
        x_valid[i] = module_main.token_to_vec(valid[i]["tokens"], max_length)

    y_valid = np.ones(len(valid))

    print("Converting invalid...")

    for i in range(len(invalid)):
        x_invalid[i] = module_main.token_to_vec(invalid[i]["tokens"], max_length)

    y_invalid = np.zeros(len(invalid))

    x = np.concatenate((x_valid, x_invalid))
    y = np.concatenate((y_valid, y_invalid))

    y = to_categorical(y, 2)

    print("preparing for lstm_vis...")

    x_flatten = x.flatten()
    hf = h5py.File("train.hdf5", "w")
    hf.create_dataset('words', data=x_flatten)
    hf.close()

    # Reshape y:
    '''print(y.shape)
    y_tiled = np.tile(y, (max_length, 1))
    print(y_tiled.shape)
    y_tiled = y_tiled.reshape(len(y), max_length, 1)'''

    # max_doc_length vectors of size embedding_size
    myInput = Input(shape=(max_length,), name='input')
    embed = Embedding(output_dim=embedding_size, input_dim=len(module_main.TOKEN2VEC)+1, input_length=max_length)(myInput)
    lstm_out = LSTM(lstm_cells)(embed)
    predictions = Dense(2, activation='softmax')(lstm_out)#TimeDistributed(Dense(2, activation='softmax'))(lstm_out)
    model = Model(inputs=myInput, outputs=predictions)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit({'input': x}, y, epochs=epochs, batch_size=batch_size)

    model.layers.pop()
    model.summary()
    # Save the states via predict
    inp = model.input
    out = model.layers[-1].output
    model_RetreiveStates = Model(inp, out)
    states_model = model_RetreiveStates.predict(x, batch_size=batch_size)
    print(states_model.shape)

    # Flatten first and second dimension for LSTMVis
    states_model_flatten = states_model.reshape(len(x) * max_length, 1)

    hf = h5py.File("states.hdf5", "w")
    hf.create_dataset('states1', data=states_model_flatten)
    hf.close()

if __name__ == "__main__":
    main()
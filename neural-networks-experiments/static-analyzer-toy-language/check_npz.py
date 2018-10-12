import sys, io
import keras
import numpy as np
from train_seq_embed import sequences_to_onehot
from keras.models import load_model

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: check.py MODEL-FILE NPZ-File")
        sys.exit(-1)

    max_length = 128
    symbol_count = 19

    print("Setting up network...")

    model = load_model(sys.argv[1])

    print("Loading data...")

    data = np.load(sys.argv[2])  # load training data from file

    x_valid = data["x_valid"]
    x_not_valid = data["x_not_valid"]

    x_valid = sequences_to_onehot(x_valid, max_length, symbol_count)
    x_not_valid = sequences_to_onehot(x_not_valid, max_length, symbol_count)

    print("Checking valid data...")

    results = model.predict(x_valid)

    valid_r=0
    valid_w=0
    for r in results:
        if(r[0] < r[1]):
            valid_r+=1
        else:
            valid_w+=1

    print("Checking invalid data...")

    results = model.predict(x_not_valid)

    invalid_r = 0
    invalid_w = 0
    for r in results:
        if (r[0] > r[1]):
            invalid_r += 1
        else:
            invalid_w += 1

    print(valid_r, "/", len(x_valid), "valid correct predicted")
    print(valid_w, "/", len(x_valid), "valid incorrect predicted")
    print(invalid_r, "/", len(x_not_valid), "invalid correct predicted")
    print(invalid_w, "/", len(x_not_valid), "invalid incorrect predicted")


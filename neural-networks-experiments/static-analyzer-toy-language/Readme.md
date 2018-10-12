# Usage

There three different type of data encodings used, byte code, ascii arrays and sequence embedding. For each type of encoding a preprocess script is used to preprocess the data into a usable format.

## Setup

- Python 3 (64 Bit) needs to be installed
- `pip install numpy` (Numpy)
- `pip install tensorflow` (Tensorflow)
- `pip install keras` (Keras)

## Byte code

The script preprocess_data.py is used to convert the training samples into byte code. The script receivers as parameter two directories which contain the valid and non valid samples and an output file name that will contain the encoded data. The output file can be fed to the script train.py or train_keras.py on the data.  
Example:
```
python preprocess_data.py /Path/to/valid/samples /Path/to/invalid/samples data.npz
python train_keras.py data.npz
```

## Ascii arrays

The script preprocess_data_string.py is used to convert the training samples into ascii arrays. The script receivers as parameter two directories which contain the valid and non valid samples and an output file name that will contain the encoded data. The output file can be fed to the script train.py or train_keras.py to train on the data.
Example:
```
python preprocess_data_string.py /Path/to/valid/samples /Path/to/invalid/samples data.npz
python train_keras.py data.npz
```

## Sequence embedding

The script preprocess_data_seq_embed.py is used to convert the training samples into sequences. The script receivers as parameter two directories which contain the valid and non valid samples and an output file name that will contain the encoded data. The output file can be fed to the script train_seq_embed.  
Example:
```
python preprocess_data_seq_embed.py /Path/to/valid/samples /Path/to/invalid/samples data.npz
python train_seq_embed.py data.npz 
```

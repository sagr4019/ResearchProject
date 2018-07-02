import numpy, sys
import tensorflow as tf
from tensorflow.contrib import rnn
import preprocess_data

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

    max_length = 500
    num_hidden = 512
    batch_size = 64

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
    max_length = data["max_length"][0]

    print(train_x_valid)

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
    train_y = tf.one_hot(train_y, 2)
    test_y = tf.one_hot(test_y, 2)

    train_x = train_x.astype("float32")
    test_x = test_x.astype("float32")

    train_x /= 255
    test_x /= 255

    train_x = numpy.expand_dims(train_x, axis=2)
    test_x = numpy.expand_dims(test_x, axis=2)

    #dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y)) #create dataset from training data

    print("Setting up network...")

    #input and output layers
    x = tf.placeholder(tf.float32, [None, max_length, 1])
    y = tf.placeholder(tf.float32, [None, 2])

    #lstm layer
    #cell = tf.nn.rnn_cell.LSTMCell(num_hidden, state_is_tuple=True)
    cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(num_hidden), rnn.BasicLSTMCell(num_hidden)])
    val, state = tf.nn.dynamic_rnn(cell, x, dtype=tf.float32)

    val = tf.transpose(val, [1, 0, 2])
    last = tf.gather(val, int(val.get_shape()[0]) - 1)

    weight = tf.Variable(tf.truncated_normal([num_hidden, int(y.get_shape()[1])]))
    bias = tf.Variable(tf.constant(0.1, shape=[y.get_shape()[1]]))

    prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)
    cross_entropy = -tf.reduce_sum(y * tf.log(tf.clip_by_value(prediction, 1e-10, 1.0)))

    #prediction = tf.matmul(last, weight) + bias
    #cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))

    optimizer = tf.train.RMSPropOptimizer(0.1)
    minimize = optimizer.minimize(cross_entropy)

    mistakes = tf.not_equal(tf.argmax(y, 1), tf.argmax(prediction, 1))
    error = tf.reduce_mean(tf.cast(mistakes, tf.float32))

    print("Initialising variables...")

    init_op = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init_op)

    print("Starting training...")

    test_y = sess.run(test_y) #converting tensor to numpy array
    train_y = sess.run(train_y)

    no_of_batches = int(len(train_x) / batch_size)
    epoch = 25
    for i in range(epoch):
        print("Training epoch " + str(i))
        ptr = 0
        for j in range(no_of_batches):
            print("Training batch " + str(j) + " of " + str(no_of_batches))
            inp, out = train_x[ptr:ptr + batch_size], train_y[ptr:ptr + batch_size]
            ptr += batch_size
            sess.run(minimize, feed_dict={x: inp, y: out})
        print("Evaluating...")
        incorrect = sess.run(error, feed_dict={x: test_x, y: test_y})
        print('Epoch {:2d} error {:3.4f}%'.format(i + 1, 100 * incorrect))
    print(sess.run(prediction, {x : valid_sample}))
    print(sess.run(prediction, {x: invalid_sample}))
    sess.close()

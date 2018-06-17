# Getting started with TensorFlow
## Prerequisite
Download latest python: [here](https://www.python.org/downloads/)

## Download and install TensorFlow
To install TensorFlow, start a terminal. Then issue the appropriate pip3 install command in that terminal. To install the CPU-only version of TensorFlow, enter the following command:

`pip3 install --upgrade tensorflow`

To install the GPU version of TensorFlow, enter the following command:

`pip3 install --upgrade tensorflow-gpu`

## Testing installation
You can test your installation by running a terminal and start the python shell.

`python`

Enter the following short program inside the python interactive shell:

```python
import tensorflow as tf

hello = tf.constant('Hello, TensorFlow!')

sess = tf.Session()

print(sess.run(hello))
```

If the system outputs "Hello, TensorFlow!", then you are ready to begin writing TensorFlow programs:



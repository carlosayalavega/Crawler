import tensorflow as tf
import numpy as np
from logistic_model import logistic_model 
from read_dataset import *

# Load and shuffle dataset
dataset = read_dataset('../data/trainset.csv')
np.random.shuffle(dataset)


# Separate 60% Training set / 40% Test Set
train_test_ratio = 0.6
trainset_size    = int(np.round(dataset.shape[0] * train_test_ratio))
testset_size     = dataset.shape[0] - trainset_size

train_dataset = dataset[0:trainset_size,:]
test_dataset  = dataset[trainset_size:,:]
train_X, train_Y = separate_labels(train_dataset)
test_X , test_Y  = separate_labels(test_dataset)

# Network parameters
input_units   = train_X.shape[1]
hiddent_units = 30
output_units  = 1

# Learning parameters
num_iterations = 1000
learning_rate  = 0.03

model = logistic_model(input_units, hiddent_units, output_units)

# Build TensorFlow training graph
model.build_graph(learning_rate)

# Train model via gradient descent.
session = tf.Session()
session.run(tf.global_variables_initializer())

for i in range(num_iterations):
    session.run(model.grad_descent, feed_dict={model.X: train_X, model.Y: train_Y})

train_accuracy = session.run(model.accuracy, feed_dict={model.X: train_X, model.Y: train_Y})
test_accuracy  = session.run(model.accuracy, feed_dict={model.X: test_X, model.Y: test_Y})

test_predict = session.run(model.predict, feed_dict={model.X: test_X, model.Y: test_Y})
print("Training Set accuracy:" , str.format('{0:.3f}', train_accuracy*100), "%")
print("Test Set accuracy:" , str.format('{0:.3f}', test_accuracy*100), "%")

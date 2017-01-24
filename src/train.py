# import tensorflow as tf

# hello = tf.constant('Hello, TensorFlow!')
# sess = tf.Session()
# print(sess.run(hello))
# a = tf.constant(10)
# b = tf.constant(32)
# print(sess.run(a + b))















# import gym
import numpy as np
import random
import tensorflow as tf
# import matplotlib.pyplot as plt

# %matplotlib inline


# env = gym.make('FrozenLake-v0')

fdata = open('data/keeper/input/g1_13.txt').readlines()
x_data = np.array([eval(x) for x in fdata])

fdata = open('data/keeper/output/g1_13.txt').readlines()
y_data = np.array([eval(y) for y in fdata])


tf.reset_default_graph()

x = tf.placeholder(tf.float32, [None, 14])


#These lines establish the feed-forward part of the network used to choose actions
# x_data = tf.placeholder(shape=[1,14], dtype=tf.int32)
# y_data = tf.placeholder(shape=[1,6], dtype=tf.int32)
# W = tf.Variable(tf.random_uniform([14,2],0,0.01))
# Qout = tf.matmul(x_data, W)
# predict = tf.argmax(Qout,1)


W = tf.Variable(tf.zeros([14, 1]))
b = tf.Variable(tf.zeros([1, 6]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.float32, [None, 6])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# W = tf.Variable(tf.random_uniform([1, 14], 0, 1, dtype=tf.float32))
# b = tf.Variable(tf.zeros([1,14]))
# y = W * x_data + b

# loss = tf.reduce_mean(tf.square(y - y_))
# optimizer = tf.train.GradientDescentOptimizer(0.5)
# train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

# Launch the graph.
sess = tf.Session()
sess.run(init)

# Fit the line.
for step in range(8):
    sess.run(train_step, feed_dict={x: x_data, y_: y_data})
    if step % 7 == 0:
        print('step: {}\nW: {}\nb: {}'.format(step, sess.run(W), sess.run(b)))




fdata = open('data/keeper/input/g1_10.txt').readlines()
x_data = np.array([eval(x) for x in fdata])

fdata = open('data/keeper/output/g1_10.txt').readlines()
y_data = np.array([eval(y) for y in fdata])


correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: x_data, y_: y_data}))

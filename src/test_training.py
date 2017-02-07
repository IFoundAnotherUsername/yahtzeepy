from gym.envs.registration import register, make
import os
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
import gym
#import matplotlib.pyplot as plt

register(
    id='Yahtzee-v0',
    entry_point='yahtzee:YahtzeeEnv',
    tags={'wrapper_config.TimeLimit.max_episode_steps': 100}
)

env = make('Yahtzee-v0')

tf.reset_default_graph()

inputs1 = tf.placeholder(shape=[1, 5], dtype=tf.float32)
W = tf.Variable(tf.random_uniform([5, 32], 0, 0.01))
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1, 32],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)


saver = tf.train.Saver()

with tf.Session() as sess:
    # Restore variables from disk.
    saver.restore(sess, "./1_yahtzee-model")
    state = env.reset()
    scores = []
    while True:
        a = sess.run(predict, feed_dict={inputs1: [state]})
        #print("State:", state, "Action:", a)
        state, reward, done, info = env.step(a[0])

        env.render()
        print('Action: ', a, "Reward:", reward)

        if done:
            #env.render()
            #print('Action: ', a, "Reward:", reward)
            scores.append(env.total_score())
            state = env.reset()
            done = False
            if len(scores) == 1:
                break
    for s in scores:
        print(s)
    print("Avg.:", float(sum(scores))/len(scores), "Max:", max(scores), "Min:", min(scores))


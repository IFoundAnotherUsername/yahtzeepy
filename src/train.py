from gym.envs.registration import register, make

import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
import gym
#import matplotlib.pyplot as plt

#from qlearn import QLearn
#qlearner = QLearn(range(32), epsilon=0.1, alpha=0.2, gamma=0.9)

register(
    id='Yahtzee-v0',
    entry_point='yahtzee:YahtzeeEnv',
    tags={'wrapper_config.TimeLimit.max_episode_steps': 100}
)

env = make('Yahtzee-v0')

tf.reset_default_graph()

inputs1 = tf.placeholder(shape=[1, 5], dtype=tf.float32)
W = tf.Variable(tf.random_uniform([5, 32], 0, 0.01))
Qout = tf.matmul(inputs1, W)
predict = tf.argmax(Qout, 1)

nextQ = tf.placeholder(shape=[1, 32], dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.AdamOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)


init = tf.global_variables_initializer()

# Set learning parameters
y = .99
e = 0.1
g = 0.1
num_episodes = 1000
#create lists to contain total rewards and steps per episode
jList = []
rList = []

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        #Reset environment and get first new observation
        s = env.reset()
        rAll = 0
        d = False
        j = 0
        #The Q-Network
        while j < 99:
            j += 1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            a, allQ = sess.run([predict, Qout], feed_dict={inputs1: [s]})
            if np.random.rand(1) < e:
                a[0] = env.action_space.sample()
            #Get new state and reward from environment
            s1, r, d, _ = env.step(a[0])
            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout, feed_dict={inputs1: [s1]})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0, a[0]] += e * (r + y * maxQ1 - targetQ[0, a[0]])
            #oldval = targetQ[0, a[0]]
            #targetQ[0, a[0]] = oldval + y * (r + g * maxQ1 - oldval)
            #Train our network using target and predicted Q values
            _, W1 = sess.run([updateModel, W], feed_dict={inputs1: [s], nextQ: targetQ})
            rAll += r
            s = s1
            if d:
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        jList.append(j)
        rList.append(rAll)

    print(saver.save(sess, '1_yahtzee-model'))

print ("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")

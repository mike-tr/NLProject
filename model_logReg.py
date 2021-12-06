from mazeToInput import generate_xSamples_on_maze, empty_spot, generate_xSamples_random, maze_to_1D
from maze import Maze
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.compat.v1 as tf
import math
#import tensorflow as tf
tf.disable_v2_behavior()

EPSILONE = 0.001


class logrModel:
    def __init__(self, features, num_classes) -> None:
        self.features = features
        self.num_classes = num_classes
        self.learning_rate = tf.placeholder(tf.float32, shape=[])
        self.x = tf.placeholder(tf.float32, [None, self.features])
        self.y_ = tf.placeholder(tf.float32, [None, self.num_classes])
        W = tf.Variable(tf.zeros([self.features, self.num_classes]), name='W')
        b = tf.Variable(tf.zeros([self.num_classes]), name='b')

        self.pred = tf.nn.softmax(tf.matmul(self.x, W) + b)

        self.cross_entropy = tf.reduce_mean(-tf.reduce_sum(self.y_ *
                                                           tf.log(self.pred + EPSILONE), reduction_indices=[1]))
        correct_prediction = tf.equal(
            tf.argmax(self.pred, 1), tf.argmax(self.y_, 1))
        self.accuracyN = tf.reduce_mean(
            tf.cast(correct_prediction, tf.float32))
        self.update = tf.train.GradientDescentOptimizer(
            learning_rate=self.learning_rate).minimize(self.cross_entropy)

        self.actual_pred = tf.argmax(self.pred, 1)
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def load(self, modelName):
        try:
            saver = tf.train.Saver()
            saver.restore(self.sess, modelName)
        except:
            print("no such model")
            pass

    def save(self, modelName):
        saver = tf.train.Saver()
        saver.save(self.sess, modelName)

    def predict_class(self, X):
        return self.sess.run(self.actual_pred, feed_dict={self.x: X})

    def accuracy(self, X, Y):
        return self.sess.run(self.accuracyN, feed_dict={self.x: X, self.y_: Y})

    def loss(self, X, Y):
        return self.sess.run(self.cross_entropy, feed_dict={self.x: X, self.y_: Y})

    def train(self, train_x, train_y, num_iterations, batch_size, update_num, learning_rate, modelName=None):
        if modelName == None:
            print("err")
            return
        train_size = len(train_x)
        current = 0
        for i in range(0, num_iterations):
            current = 0
            perm = np.random.permutation(range(train_size))
            while current < train_size:
                batch = perm[current:current+batch_size]
                current += batch_size
                # print(train_x[batch[range(5)]])
                self.sess.run(self.update, feed_dict={
                    self.x: train_x[batch], self.y_: train_y[batch], self.learning_rate: learning_rate})
            if i % update_num == 0:
                print('Iteration:', i, ' b:',
                      ' accuracity_train:', self.accuracy(train_x, train_y),
                      " loss :", self.loss(train_x, train_y))
                print("saved as", modelName + "_train")
                self.save(modelName + "_train")


def train_reg():
    train_x, train_y = generate_xSamples_random(11, 11, 15001)
    # print(data_x[0])

    features = train_x[0].shape[0]
    predictions = train_y[0].shape[0]

    modelname = 'rlogmodel'

    model = logrModel(features, predictions)

    print("preload accuracy", model.accuracy(train_x, train_y))
    print("error", model.loss(train_x, train_y))
    model.load(modelname)
    print("loaded accuracy", model.accuracy(train_x, train_y))
    print("error", model.loss(train_x, train_y))

    bad_trainings = 0
    for i in range(10):
        model.train(train_x, train_y, 2501, 250, 250,
                    0.01, modelname)
        model.save(modelname)

        train_x, train_y = generate_xSamples_random(11, 11, 15001)
        loss = model.loss(train_x, train_y)
        while(math.isnan(loss)):
            print("some error has accured")
            bad_trainings += 1
            if bad_trainings > 5:
                print("failed to generate good data! might be problem with model")
                exit(0)
            train_x, train_y = generate_xSamples_random(11, 11, 15001)
            loss = model.loss(train_x, train_y)

        bad_trainings = 0
        print("after train num", i, " accuracy",
              model.accuracy(train_x, train_y))
        print("error", model.loss(train_x, train_y))

    print(model.sess.run(model.wu))

from mazeToInput import generate_xSamples_on_maze, empty_spot, generate_xSamples_random, maze_to_1D, maze_state_to_input
from maze import Maze
import matplotlib.pyplot as plt
import numpy as np
from player import Direction
import tensorflow.compat.v1 as tf
from game import Game, input_loop_human
from model_logReg import logrModel
#import tensorflow as tf

tf.disable_v2_behavior()

train_x, train_y = generate_xSamples_random(31, 31, 1000)
print(train_x.shape)
# print(data_x[0])

# print(train_x[0:20, -5:])

features = train_x[0].shape[0]
predictions = train_y[0].shape[0]

modelname = 'rlogmodel'

model = logrModel(features, predictions)

#print("preload accuracy", model.accuracy(train_x, train_y))
model.load(modelname)

print("loaded accuracy", model.accuracy(train_x, train_y))

# model.train(train_x, train_y, 100001, 200, 2500)
model.save(modelname)


def run_comp():
    game = Game(640, 640)
    state = maze_state_to_input(
        game.m, game.player.posNormalized(), game.food_pos)
    # print(state.shape)
    # print()
    # print(model.predict_class(train_x[0:25]), train_y[0:25])

    def input_loop():
        key = model.predict_class(state)
        print("Direction comp", Direction.to_string(key))
        key2 = input_loop_human()
        if key2 == Direction.NONE:
            return key
        print("human controlling :", Direction.to_string(key2))
        return key2

    game.start(input_loop)
    exit()

#model.train(train_x, train_y, 40001, 200, 1000)


# run_comp()

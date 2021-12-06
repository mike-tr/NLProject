from math import log
import math
from maze import Maze
import numpy as np
from pathFinder import find_path


def maze_state_to_input(maze: Maze, pos_player, pos_food):
    data = maze_to_1D(maze)
    # data = input_add_pos(data, pos_food, maze.width, maze.height)
    data = input_add_pos(data, pos_player, maze.width, maze.height)
    return np.array([data])


def maze_to_1D(maze: Maze):
    # print(np.array(maze.maze))
    # fm = np.array(maze.maze)[1:-1, 1:-1]
    fm = np.array(maze.getWallsOnly())
    # print(fm)
    # print(maze.maze)
    # std = 0.5 * (fm.shape[0] + fm.shape[0]) / 2
    # print(fm.shape, 29, std)
    return (fm.flatten() * 2) - 1


def input_add_pos(X, pos, width, height):
    n = (width - 2)*(height - 2)
    avg = 1/n
    std = (1/n)*(1-1/n)
    std = math.sqrt(std)

    return add_pos_std_avg(X, pos, width, height, avg, std)


def add_pos_std_avg(X, pos, width, height, avg, std):
    arr = np.zeros([width - 2, height - 2])
    arr[pos[0]-1][pos[1]-1] = 1
    arr = (arr - avg) / std
    arr = arr.flatten()

    return np.append(X, arr)


def empty_spot(width, height):
    x = np.random.randint(0, np.floor((width) / 2)) * 2 + 1
    y = np.random.randint(0, np.floor((height) / 2)) * 2 + 1
    return x, y


def generate_xSamples_random(width, height, num_samples):
    maze = Maze(width, height)
    maze.rebuildMaze()
    datax, datay = generate_xSamples_on_maze(maze, 1000)
    if len(datax) <= 0:
        return generate_xSamples_random(width, height, num_samples)

    while len(datax) < num_samples:
        #print(len(datax), num_samples)
        maze = Maze(width, height)
        maze.rebuildMaze()
        X, Y = generate_xSamples_on_maze(maze, 1000)
        if len(X) <= 0:
            continue
        datax = np.concatenate((datax, X))
        datay = np.concatenate((datay, Y))
        # datax += X
        # datay += Y

    dic = [0, 0, 0, 0]
    for i in range(len(datax)):
        for j in range(4):
            if datay[i][j] == 1:
                dic[j] += 1
    print(len(datax), len(datay))
    print(dic)
    return np.array(datax), np.array(datay)


def getRandom(X, Y, indices, samples):
    perm = np.random.permutation(indices)
    return X[perm][0:samples], Y[perm][0:samples]


def generate_xSamples_on_maze(maze: Maze, num_samples):
    # denote the input is the above, and desired output would be to follow the path.
    datax = []
    datay = []

    width = maze.width
    height = maze.height
    inp = maze_to_1D(maze)

    #print(width, height)
    n = (width - 2)*(height - 2)
    # print(n)
    avg = 1/n
    #print(avg, 1/81)
    std = (1/n)*(1-1/n)
    std = math.sqrt(std)
    while(len(datax) < num_samples * 2):
        # food_pos = empty_spot(maze.width, maze.height)
        food_pos = (maze.width - 2, maze.height - 2)
        current_pos = empty_spot(maze.width, maze.height)
        path = find_path(maze, current_pos, food_pos)
        # print(current_pos, end)
        # print(path)

        # hX = input_add_pos(inp, food_pos, width, height)
        while(len(path) > 1):
            next_pos = path[1]
            #X = input_add_pos(inp, current_pos, width, height)
            X = add_pos_std_avg(inp, current_pos, width, height, avg, std)
            datax.append(X)

            dir_vec = direction_to_vector(current_pos, next_pos)
            # print(current_pos, next_pos, dir_vec)
            path.pop(0)
            current_pos = next_pos
            datay.append(dir_vec)
    # print(datax[1])

    perm = np.random.permutation(range(len(datax)))
    datax = np.array(datax)[perm][::2]
    datay = np.array(datay)[perm][::2]
    dic = [0, 0, 0, 0]
    inddic = [[], [], [], []]
    for i in range(len(datax)):
        for j in range(4):
            if datay[i][j] == 1:
                dic[j] += 1
                inddic[j].append(i)
    # print(dic)

    val = dic[0]
    for i in range(1, 4):
        if val > dic[i]:
            val = dic[i]
    if val <= 0:
        print("failed to generate data!")
        return [], None

    X, Y = getRandom(datax, datay, inddic[0], val)
    for i in range(1, 4):
        X2, Y2 = getRandom(datax, datay, inddic[i], val)
        X = np.concatenate((X, X2))
        Y = np.concatenate((Y, Y2))

    # max_index_row = np.argmax(datay, axis=1)
    # print(max_index_row[:10])

    return X, Y
    # return [1,2,3,4], [11,12,13,14]


def direction_to_vector(start, end):
    x_dir = end[0] - start[0]
    y_dir = end[1] - start[1]
    if x_dir == -1:
        # return [l,r,t,d]
        return [1, 0, 0, 0]
    if x_dir == 1:
        return [0, 1, 0, 0]
    if y_dir == 1:
        return [0, 0, 1, 0]
    if y_dir == -1:
        return [0, 0, 0, 1]


# def positionEncoder(n : float, dimention):
#     # idea of encoder from here https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
#     # basically i want to encode player position and food position with a good way
#     # tho maybe in this case we as the size of maze is always the same we can simply devide by the size of the word

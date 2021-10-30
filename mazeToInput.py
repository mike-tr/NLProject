from math import log
from maze import Maze
import numpy as np
from pathFinder import find_path


def mazeToInput(maze : Maze, pos_player, pos_food):
    data = np.array(maze.maze).flatten()
    data = np.append(data, [pos_player[0] / maze.width, pos_player[1] / maze.height, pos_food[0] / maze.width, pos_food[1] / maze.height])
    return data

def maze_to_1D(maze: Maze):
    return np.array(maze.maze).flatten()

def input_add_pos(X, pos, width, height):
     return np.append(X, [pos[0] / width, pos[1] / height])

def empty_spot(width, height):
    x  = np.random.randint(0, np.floor((width) / 2)) * 2 + 1
    y  = np.random.randint(0, np.floor((height) / 2)) * 2 + 1
    return x,y

def generate_xSamples_random(width, height, num_samples):
    datax = []
    datay = []
    
    while len(datax) < num_samples:
        maze = Maze(width,height)
        maze.buildMaze()
        X, Y = generate_xSamples_on_maze(maze, 200)
        datax += X
        datay += Y
    return datax, datay
    

def generate_xSamples_on_maze(maze : Maze, num_samples):
    # denote the input is the above, and desired output would be to follow the path.
    datax = []
    datay = []

    width = maze.width
    height = maze.height
    inp = maze_to_1D(maze)
    while(len(datax) < num_samples):
        end = empty_spot(maze.width, maze.height)
        current_pos = empty_spot(maze.width, maze.height)
        path = find_path(maze, current_pos, end)
        #print(current_pos, end)
        #print(path)
        
        hX = input_add_pos(inp, end, width, height)
        while(len(path) > 1):
            next_pos = path[1]
            X = input_add_pos(hX, current_pos, width, height)
            datax.append(X)

            dir_vec = direction_to_vector(current_pos, next_pos)
            print(current_pos, next_pos, dir_vec)
            path.pop(0)
            current_pos = next_pos
            datay.append(dir_vec)
    #print(datax[1])
    return datax, datay

            

def direction_to_vector(start, end):
    x_dir = end[0] - start[0]
    y_dir = end[1] - start[1]
    if x_dir == -1:
        # return [l,r,t,d]
        return [1,0,0,0]
    if x_dir == 1:
        return [0,1,0,0]
    if y_dir == 1:
        return [0,0,1,0]
    if y_dir == -1:
        return [0,0,0,1]
    
    

# def positionEncoder(n : float, dimention):
#     # idea of encoder from here https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
#     # basically i want to encode player position and food position with a good way
#     # tho maybe in this case we as the size of maze is always the same we can simply devide by the size of the word
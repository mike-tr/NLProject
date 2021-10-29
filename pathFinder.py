import numpy as np
from maze import Maze
import queue

def find_path(maze : Maze, start, end):
    # start : (x0,y0) , End : (x1,y1)
    q = queue.Queue()
    if maze.getVal(start) == 1 or maze.getVal(end) == 1:
        print("nope")
        return
    
    seen = set()
    seen.add(start)
    q.put(start)
    parent_map = {}

    parent_map[start] = -1

    while not q.empty() :
        # current : (x,y)
        current = q.get()
        if current == end:
            return path(parent_map, end)
        #print(current)
        for n in neibours(maze, current[0], current[1]):
            if n in seen:
                continue
            else:
                seen.add(n)
                parent_map[n] = current
                q.put(n)


def path(parent_map, end):
    p = [end]
    current = parent_map[end]
    while current != -1:
        p.insert(0, current)
        current = parent_map[current]    
    return p
    


    

def neibours(maze: Maze, x, y):
    ni = []
    for i in range(-1, 2, 2):
        if x + i > 1 or x + i < maze.width - 1:
            pos = (x+i, y)
            if maze.getVal(pos) == 0:
                ni.append(pos)
        if y + i > 1 or y + i < maze.width - 1:
            pos = (x, y+i)
            if maze.getVal(pos) == 0:
                ni.append(pos)
    return ni
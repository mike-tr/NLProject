from math import fabs, log
import numpy as np
import random

from union import Union


class MCell(Union):
    def __init__(self,x,y, wall) -> None:
        Union.__init__(self)
        self.x = x
        self.y = y
        self.wall = wall

class Maze:
    def __init__(self, width, height) -> None:
        self.maze = []
        self.empty = []
        self.width = width
        self.height = height

        self.cells : dict[any,MCell] = {}
        self.walls = []
        self.perm = []
        self.iter = 0
        for y in range(height):
            ar = []
            for x in range(width):
                if x == 0 or x == width-1 or y == 0 or y == height - 1:
                    ar.append(1)
                else:
                    ar.append(0)
                    self.empty.append((x,y))
            self.maze.append(ar)
        self.floor = (width - 1)*(height-1)
    
    
    def getRandomEmpty(self):
        return self.empty[random.randint(0, len(self.empty) - 1)]
    
    def setVal(self,x,y,v):
        self.maze[y][x] = v

    def makeMaze(self): 
        # Randomized Kruskal's algorithm
        self.walls = []
        self.cells : dict[any,MCell] = {}

        s = 0
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                cell = MCell(x,y, True)
                if x % 2 == 0 and y % 2 == 0:
                    # walls.append((x,y))
                    self.setVal(x,y,1)
                    cell.m = 1
                elif  x % 2 == 0 or y % 2 == 0:
                    self.walls.append((x,y))
                    self.setVal(x,y,1)
                else:
                    cell.wall = False
                s+=1
                self.cells[(x,y)] = cell
                

        self.perm = np.random.permutation(range(len(self.walls)))
        # print(perm)
        #for i in range(len(self.perm)):
            #self.addWall()

    def addWall(self):
        if self.iter >= len(self.perm):
            return -1

        wall = self.walls[self.perm[self.iter]]
        ni = neibours(self, wall[0], wall[1])
        # print(wall, ni)
        connected = True
        f = -1
        for n in ni:
            ccell = self.cells[n]
            if ccell.wall:
                continue
            if f == -1:
                f = ccell.get_group()
            elif ccell.get_group() != f:
                # print(f, self.cells[n].get_group(), n)
                connected = False
                break

        if not connected:
            wc = self.cells[wall]
            for n in ni:
                ncell = self.cells[n]
                if ncell.wall:
                    continue
                wc.add_child(ncell)

            wc.wall = False
            self.setVal(wall[0], wall[1], 0)
            self.iter += 1
            return wall
        self.iter += 1
        return -1
       
        
def neibours(maze : Maze, x, y):
    ni = set()
    for i in range(-1,2,2):
        if x + i < maze.width - 1 and x + i > 0:
            ni.add((x+i,y))
        if y + i < maze.height - 1 and y + i > 0:
            ni.add((x,y+i))
    return ni
    
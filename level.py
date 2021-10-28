import pygame

class Wall(object):
    def __init__(self, level, x, y, width, height):
        level.walls.append(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255,255,255)

class Block(object):
    def __init__(self, x, y, width, height, r,b,g):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (r,g,b)

class Level:
    def __init__(self) -> None:
        self.walls : list[Wall] = []
        self.path = []
    
    def reset(self):
        self.walls : list[Wall] = []

    def addWall(self, x, y):
        Wall(self,x,y,16,16)

    def add_path(self, path):
        self.path = []
        for pos in path:
            self.addBlock(pos[0] * 16, pos[1] * 16)

    def addBlock(self, x, y):
        self.path.append(Block(x,y,16,16,200,0,0))

    def draw(self, screen):
        for pnode in self.path:
            pygame.draw.rect(screen, pnode.color, pnode.rect)
        for wall in self.walls:
            wall : Wall
            pygame.draw.rect(screen, wall.color, wall.rect)

import pygame

class Wall(object):
    def __init__(self, level, x, y, width, height):
        level.walls.append(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255,255,255)

class Level:
    def __init__(self) -> None:
        self.walls : list[Wall] = []
    
    def reset(self):
        self.walls : list[Wall] = []

    def addWall(self, x, y):
        Wall(self,x,y,16,16)

    def draw(self, screen):
        for wall in self.walls:
            wall : Wall
            pygame.draw.rect(screen, wall.color, wall.rect)
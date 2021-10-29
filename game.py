import pygame
from level import Level
from maze import Maze

class Game:
    def __init__(self, width, length) -> None:
        pygame.init()
        self.window = pygame.display.set_mode((width, length))
        self.run = True
        self.draw = None
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def init(self, draw):
        self.draw = draw
        self.loop()
    
    def loop(self):
        while self.run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.run = self.draw(self.window) and self.run
            pygame.display.flip()
        pygame.quit()
        exit()

# class AbstactCar:
#     def __init__(self) -> None:
#         pass


# class Player(object):
    
#     def __init__(self, level : Level):
#         self.rect = pygame.Rect(32, 32, 32, 16)
#         self.level = level

#     def move(self, dx, dy):
        
#         # Move each axis separately. Note that this checks for collisions both times.
#         if dx != 0:
#             self.move_single_axis(dx, 0)
#         if dy != 0:
#             self.move_single_axis(0, dy)
    
#     def move_single_axis(self, dx, dy):
        
#         # Move the rect
#         self.rect.x += dx
#         self.rect.y += dy

#         # If you collide with a wall, move out based on velocity
#         for wall in self.level.walls:
#             if self.rect.colliderect(wall.rect):
#                 if dx > 0: # Moving right; Hit the left side of the wall
                    
#                     self.rect.right = wall.rect.left
#                 if dx < 0: # Moving left; Hit the right side of the wall
#                     self.rect.left = wall.rect.right
#                 if dy > 0: # Moving down; Hit the top side of the wall
#                     self.rect.bottom = wall.rect.top
#                 if dy < 0: # Moving up; Hit the bottom side of the wall
#                     self.rect.top = wall.rect.bottom

# generate level object

# create maze class of size 31x31
m = Maze(31,31)
level = Level(m.width * 16, m.height * 16, (255,255,224), (222,184,135))
# m.initMaze()5

# build a maze
m.buildMaze()

# just a function that places white cubes for drawing
def rebuildLevel(level : Level):
    level.reset()
    x = y = 0
    for y in range(m.height):
        for x in range(m.width):
            if m.maze[y][x] == 1:
                level.addWall(x * 16,y * 16)

# draw maze on the level
rebuildLevel(level)
# draw path on the level
level.add_path([(1,1),(1,2),(1,3),(1,4)])

# end_rect = pygame.Rect(200, 200, 16, 16)

# create window
game = Game(800,640)
# player = Player(level) # Create the player

# draw loop
def loop(screen : pygame.Surface):
    screen.fill((0, 0, 0))
    level.draw(screen)
    return True

# actually start drawing
game.init(loop)


exit()
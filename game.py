import pygame
from level import Level
from maze import Maze
from player import Player
from pathFinder import find_path
from mazeToInput import generate_xSamples_on_maze, empty_spot, generate_xSamples_random

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


# generate level object

# create maze class of size 31x31
m = Maze(31,31)
level = Level(m.width * 16, m.height * 16, (255,255,224), (222,184,135))
m.initMaze()
#m.reset()
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

# end_rect = pygame.Rect(200, 200, 16, 16)

# create window
game = Game(800,640)
# player = Player(level) # Create the player
player_pos = empty_spot(m.width, m.height)
player = Player(level,player_pos[0],player_pos[1],16,16)

food_pos = empty_spot(m.width, m.height)
food_rect = pygame.Rect(food_pos[0] * 16 + 1, food_pos[1] * 16 + 1, 14, 14)

#gemerate_xSamples_on_maze(m, 5)
generate_xSamples_random(31,31,100)

# draw loop
def loop(screen : pygame.Surface):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)
    # m.addWall()
    # rebuildLevel(level)
    screen.fill((0, 0, 0))
    level.draw(screen)
    pygame.draw.rect(screen, (0, 255, 0), food_rect)
    pygame.draw.rect(screen, (70, 130, 180), player.rect)

    # print(mazeToInput(m, player.posNormalized(), food_pos))
    # print(m.maze)

    #print(find_path(m, player.posNormalized(), food_pos))
    level.add_path(find_path(m, player.posNormalized(), food_pos))

    if player.rect.colliderect(food_rect):
        print("you win!")
        return False

    return True

# actually start drawing
game.init(loop)


exit()
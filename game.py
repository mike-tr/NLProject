import pygame
from level import Level
from maze import Maze
from player import Player
from pathFinder import find_path

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
player = Player(level,1,1,16,16)
end_rect = pygame.Rect(29 * 16 + 1, 29 * 16 + 1, 14, 14)

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
    pygame.draw.rect(screen, (0, 255, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)


    level.add_path(find_path(m, player.pos(), (29,29)))

    if player.rect.colliderect(end_rect):
        print("you win!")
        return False

    return True

# actually start drawing
game.init(loop)


exit()
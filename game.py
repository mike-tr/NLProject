import pygame
from level import Level

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


class Player(object):
    
    def __init__(self, level : Level):
        self.rect = pygame.Rect(32, 32, 32, 16)
        self.level = level

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.rect = pygame.transform.rotate( self.rect, 10 ) 
            #self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in self.level.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

word = [
"WWWWWWWWWWWWWWWWWWWW",
"W                  W",
"W         WWWWWW   W",
"W   WWWW       W   W",
"W   W        WWWW  W",
"W WWW  WWWW        W",
"W   W     W W      W",
"W   W     W   WWW WW",
"W   WWW WWW   W W  W",
"W     W   W   W W  W",
"WWW   W   WWWWW W  W",
"W W      WW        W",
"W W   WWWW   WWW   W",
"W     W    E   W   W",
"WWWWWWWWWWWWWWWWWWWW",
]

level = Level()

x = y = 0
for row in word:
    for col in row:
        if col == "W":
            level.addWall(x,y)
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0

game = Game(800,640)
player = Player(level) # Create the player


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
    
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        print("you win!")
        return False
    
    # Draw the scene
    screen.fill((0, 0, 0))
    level.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    return True

game.init(loop)

exit()
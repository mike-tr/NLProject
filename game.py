import pygame
from level import Level
from maze import Maze
from player import Player, Direction
from pathFinder import find_path
from mazeToInput import generate_xSamples_on_maze, empty_spot, generate_xSamples_random, maze_to_1D
from engine import Engine

# generate level object

maze_width = 31
maze_height = 31


class Game:
    def __init__(self, width, height) -> None:
        self.game = Engine(width, height)
        self.m = Maze(maze_width, maze_height)
        self.level = Level(self.m.width * 16, self.m.height * 16,
                           (255, 255, 224), (222, 184, 135))
        self.input_loop = None
        self.init()

    def init(self):
        self.m.rebuildMaze()
        self.rebuildLevel()

        player_pos = empty_spot(self.m.width, self.m.height)
        self.player = Player(self.level, player_pos[0], player_pos[1], 16, 16)

        self.food_pos = empty_spot(self.m.width, self.m.height)
        self.food_rect = pygame.Rect(
            self.food_pos[0] * 16 + 1, self.food_pos[1] * 16 + 1, 14, 14)

    def rebuildLevel(self):
        self.level.reset()
        x = y = 0
        for y in range(self.m.height):
            for x in range(self.m.width):
                if self.m.maze[y][x] == 1:
                    self.level.addWall(x * 16, y * 16)

    def start(self, input_loop):
        self.input_loop = input_loop
        self.game.init(self)

    def loop(self, screen: pygame.Surface):
        key = self.input_loop()
        self.player.moveDir(key)
        # player.move(0, 1)
        # m.addWall()
        # rebuildLevel(level)
        screen.fill((0, 0, 0))
        self.level.draw(screen)
        pygame.draw.rect(screen, (0, 255, 0), self.food_rect)
        pygame.draw.rect(screen, (70, 130, 180), self.player.rect)

        # print(mazeToInput(m, player.posNormalized(), food_pos))
        # print(m.maze)

        # print(find_path(m, player.posNormalized(), food_pos))
        self.level.add_path(
            find_path(self.m, self.player.posNormalized(), self.food_pos))

        self.player.update()
        if self.player.rect.colliderect(self.food_rect):
            print("you win!")
            return False

        return True


def input_loop_human():
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        return Direction.LEFT
        # player.move(-1, 0)
    if key[pygame.K_RIGHT]:
        return Direction.RIGHT
        # player.move(1, 0)
    if key[pygame.K_UP]:
        return Direction.UP
        # player.move(0, -1)
    if key[pygame.K_DOWN]:
        return Direction.DOWN
    return Direction.NONE


def run_human():
    game = Game(640, 640)
    game.start(input_loop_human)
    exit()


# run_human()

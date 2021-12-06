import pygame
from pygame import math
import math


class Direction:
    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 2
    NONE = -1
    SKIP = -2

    def valid(direction):
        if 0 <= direction <= 4:
            return True

    def to_string(direction):
        if direction == Direction.LEFT:
            return "Left"
        if direction == Direction.RIGHT:
            return "RIGHT"
        if direction == Direction.UP:
            return "UP"
        if direction == Direction.DOWN:
            return "DOWN"


speed = 2


class Player(object):

    def __init__(self, level, x, y, width, height):
        self.level = level
        self.rect = pygame.Rect(x * width + width/4,
                                y * height + height/4, width/2, height/2)
        self.direction = Direction.NONE
        self.ticks_left = 0
        self.ticks_per_move = width / speed
        print(self.ticks_per_move)

    def posNormalized(self):
        return math.floor(self.rect.centerx / 16), math.floor(self.rect.centery / 16)

    def pos(self):
        return self.rect.center

    def update(self):
        # add velocity until in the correct position
        # print(self.direction, self.ticks_left, self.ticks_per_move)
        if self.direction != -1:
            if self.direction == Direction.LEFT:
                self.move(-speed, 0)
            if self.direction == Direction.RIGHT:
                self.move(speed, 0)
            if self.direction == Direction.UP:
                self.move(0, -speed)
            if self.direction == Direction.DOWN:
                self.move(0, speed)
            self.ticks_left -= 1
            if self.ticks_left <= 0:
                self.direction = Direction.NONE

    def moveDir(self, direction):
        if self.direction != Direction.NONE:
            return
        if Direction.valid(direction):
            self.direction = direction
            self.ticks_left = self.ticks_per_move

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in self.level.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                self.direction = Direction.NONE

import pygame

pygame.init()

import random

screen_height = 1080
screen_width = 1920
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 30


class Game:
    def __init__(self):
        uwu

    class Player:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Enemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class PlayerAttacks:
        def __init__(self, x, y, vx, vy, dmg, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.type = typ

    class EnemyAttacks:
        def __init__(self, x, y, vx, vy, dmg, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.type = typ

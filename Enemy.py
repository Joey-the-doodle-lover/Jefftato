import math
import pygame
import random

from GameSprite import GameSprite
from animation import ImageLoader, Animation


class Enemy(GameSprite):
    base_image = None

    repulsion_strength = 0.05

    def __init__(self, x, y, hp, speed, power, typ, viewport, *groups: pygame.sprite.Sprite):
        super().__init__(enemy_temp_image)
        self.flipped = False

        self.hp = hp
        self.speed = speed
        self.base_speed = 2.5
        self.type = typ
        self.power = power
        self.unstuned = 0  # frame when they will next be unstunned

        self.real_radius = 0.25
        self.width = self.real_radius * 2
        self.height = self.real_radius * 2

    def get_velocity(self, player, frame):
        if frame > self.unstuned:
            move_speed = (1 + (self.speed / 100)) * self.base_speed
            dx = player.x - self.x
            dy = player.y - self.y
            angle = math.atan2(dy, dx)
            self.vx = move_speed * math.cos(angle)
            self.vy = move_speed * math.sin(angle)

            pi = 3.1415926535897932384626433
            if angle > pi:
                self.flipped = False
            elif angle < pi:
                self.flipped = True
        else:
            self.vx = 0
            self.vy = 0

    def update(self, elapsed, enemies, player, frame_context):
        self.get_velocity(player, frame_context.frame)
        self.repel_from_enemies(enemies)
        super().update(elapsed, frame_context)

        self.remove_dead()




    @staticmethod
    def create_base_image(width, height):
        if Enemy.base_image is None \
                or Enemy.base_image.get_width() != width \
                or Enemy.base_image.get_height() != height:
            image = pygame.Surface([width, height], pygame.SRCALPHA)
            image.fill((0, 0, 0, 0))
            color = (255, 0, 0)
            pygame.draw.circle(image, color, (width / 2, height / 2), width / 2)
            Enemy.base_image = image
        return Enemy.base_image

    def repel_from_enemies(self, enemies):
        for enemy in enemies:
            distance = (((self.x - enemy.x) ** 2) + ((self.y - enemy.y) ** 2)) * 0.5
            if distance < 2:
                try:
                    force = -(self.repulsion_strength / (distance ** 2))
                except ZeroDivisionError:
                    force = 0

                dx = enemy.x - self.x
                dy = enemy.y - self.y
                angle = math.atan2(dy, dx)
                self.vx += force * math.cos(angle)
                self.vy += force * math.sin(angle)

    def remove_dead(self):
        if self.hp <= 0:
            self.kill()

    def knockbacked(self, x, y, distance):
        dx = self.x - x
        dy = self.y - y
        angle = math.atan2(dy, dx)
        self.x += (distance * math.cos(angle))
        self.y += (distance * math.sin(angle))


image_loader = ImageLoader('assets/enemy')
enemy_temp_image = Animation(image_loader.load_images('temp-bug'), 0.2)

import math
import pygame
import random


class Enemy(pygame.sprite.Sprite):
    base_image = None

    repulsion_strength = 0.01

    def __init__(self, x, y, hp, speed, typ, viewport, *groups: pygame.sprite.Sprite):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        self.hp = hp
        self.speed = speed
        self.base_speed = 2.5
        self.type = typ

        self.image = pygame.Surface([1920, 1080])
        self.real_radius = 0.25
        self.radius = math.ceil(viewport.convert_width(self.real_radius))

        self.image = Enemy.create_base_image(self.radius * 2, self.radius * 2)
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def update_position(self, player, enemys, elapsed, arena_bounds):
        move_speed = (1 + (self.speed / 100)) * self.base_speed

        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)

        self.vx = move_speed * math.cos(angle)
        self.vy = move_speed * math.sin(angle)

        self.repel_from_enemys(enemys)

        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

        self.stay_in_bounds(arena_bounds)

    def stay_in_bounds(self, arena_bounds):
        if self.x > arena_bounds[2]:
            self.x = arena_bounds[2]
        if self.x < arena_bounds[0]:
            self.x = arena_bounds[0]
        if self.y > arena_bounds[3]:
            self.y = arena_bounds[3]
        if self.y < arena_bounds[1]:
            self.y = arena_bounds[1]

    def update(self, elapsed, enemys, player, arena_bounds, viewport):
        self.remove_dead()

        self.update_position(player, enemys, elapsed, arena_bounds)

        self.rect = viewport.convert_rect_to_screen((self.x, self.y, self.real_radius * 2, self.real_radius * 2))
        self.image = Enemy.create_base_image(self.rect.w, self.rect.h)

    def repel_from_enemys(self, enemys):
        for enemy in enemys:
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

    @staticmethod
    def create_base_image(width, height):
        if Enemy.base_image is None \
                or Enemy.base_image.get_width() != width \
                or Enemy.base_image.get_height() != height:
            image = pygame.Surface([width, height], pygame.SRCALPHA)
            image.fill((0, 0, 0, 0))
            color = (255, 0, 0, 255)
            pygame.draw.circle(image, color, (width / 2, height / 2), width / 2)
            Enemy.base_image = image
        return Enemy.base_image

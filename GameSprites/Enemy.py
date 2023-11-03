import math

from ParentSpites.GameSprite import GameSprite
from ParentSpites.animation import ImageLoader, Animation


class Enemy(GameSprite):
    base_image = None
    knockbacked = False
    repulsion_strength = 0.05

    def __init__(self, x, y, hp, speed, power, typ):
        super().__init__(enemy_temp_image)
        self.x = x
        self.y = y
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
        if frame > self.knockbacked:
            if frame > self.unstuned:
                move_speed = (1 + (self.speed / 100)) * self.base_speed
                dx = player.x - self.x
                dy = player.y - self.y
                angle = math.atan2(dy, dx)
                self.vx = move_speed * math.cos(angle)
                self.vy = move_speed * math.sin(angle)
            else:
                self.vx = 0
                self.vy = 0

        if self.vx < 0:
            self.flipped = False
        elif self.vx > 0:
            self.flipped = True

    def update(self, elapsed, enemies, player, frame_context):
        self.get_velocity(player, frame_context.frame)
        self.repel_from_enemies(enemies)
        super().update(elapsed, frame_context)

        self.remove_dead()

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

    def knockback(self, hit_from, speed, duration, frame):
        dx = hit_from[0] - self.x
        dy = hit_from[1] - self.y
        angle = math.atan2(dy, dx)
        self.vx = -(speed * math.cos(angle))
        self.vy = -(speed * math.sin(angle))
        self.knockbacked = frame + duration


image_loader = ImageLoader('assets/enemy')
enemy_temp_image = Animation(image_loader.load_images('temp-bug'), 0.2)

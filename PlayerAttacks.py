import math
import random
import pygame


class PlayerAttacks(pygame.sprite.Sprite):
    base_image = None

    def __init__(self, player, weapon_dmg, rang, peirce, peirce_dmg, bounce, typ, viewport,
                 *groups: pygame.sprite.Sprite):
        super().__init__(*groups)
        self.x = player.x + (random.randint(-5, 5) / 10)
        self.y = player.y + (random.randint(-5, 5) / 10)
        self.vx = 0
        self.vy = 0

        self.start_x = self.x
        self.start_y = self.y

        self.damage = (1 + (player.damage / 100)) * weapon_dmg
        self.range = rang
        self.bounce = bounce
        self.peirce = peirce
        self.peirce_damage = 1 + (peirce_dmg / 100)
        if self.peirce_damage > 1:
            self.peirce_damage = 1
        self.type = typ

        self.enemys_hit = []

        self.color = (255, 255, 0)

        self.real_radius = 0.1
        self.radius = math.ceil(viewport.convert_width(self.real_radius))
        self.image = PlayerAttacks.create_base_image(self.radius * 2, self.radius * 2)
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def set_direction(self, player, enemys):
        move_speed = 10
        enemy = None
        if len(enemys) > 0:
            enemy = sorted(enemys, key=lambda enemy: (enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2)[0]

            dx = enemy.x - self.x
            dy = enemy.y - self.y
            angle = math.atan2(dy, dx)
        else:
            angle = random.randint(0, 360)

        self.vx = move_speed * math.cos(angle)
        self.vy = move_speed * math.sin(angle)

    def update(self, elapsed, viewport):
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed
        self.rect = viewport.convert_rect_to_screen((self.x, self.y, self.real_radius * 2, self.real_radius * 2))
        self.image = PlayerAttacks.create_base_image(self.rect.w, self.rect.h)

    def should_remove(self):
        return math.sqrt(((self.start_x - self.x) ** 2) + (self.start_y - self.y) ** 2) > self.range or self.peirce < 0

    def hit_enemy(self, enemy, player, enemys):
        if enemy not in self.enemys_hit:
            self.enemys_hit.append(enemy)
            enemy.hp -= self.damage
            if self.bounce > 0:
                self.set_direction(player, enemys)
            self.damage *= self.peirce_damage
            self.peirce -= 1

    @staticmethod
    def create_base_image(width, height):
        if PlayerAttacks.base_image is None \
                or PlayerAttacks.base_image.get_width() != width \
                or PlayerAttacks.base_image.get_height() != height:
            image = pygame.Surface([width, height], pygame.SRCALPHA)
            image.fill((0, 0, 0, 0))
            color = (255, 255, 0, 255)
            pygame.draw.circle(image, color, (width / 2, height / 2), width / 2)
            PlayerAttacks.base_image = image
        return PlayerAttacks.base_image

import math
import random

from ParentSpites.GameSprite import GameSprite
from GameSprites.Weapons import Weapons
from ParentSpites.animation import ImageLoader, Animation


class PlayerAttacks(GameSprite):
    base_image = None

    def __init__(self, point, weapon: Weapons, player):
        super().__init__(default_image)
        self.stay_in_bounds = False
        self.x = point[0]
        self.y = point[1]
        self.start_x = self.x
        self.start_y = self.y

        self.damage = (1 + (player.damage / 100)) * (weapon.damage
                                                     + (weapon.bonus_from_melee * player.melee_damage)
                                                     + (weapon.bonus_from_range * player.ranged_damage)
                                                     + (weapon.bonus_from_element * player.elemental_damage)
                                                     + (weapon.bonus_from_engin * player.engineering)
                                                     )
        self.range = (player.extra_range * weapon.range_modifier) + weapon.range
        self.bounce = player.bounces + weapon.bounces
        self.peirce = player.peircing + weapon.pierce
        self.peirce_damage = min(1, (player.peircing_damage + weapon.pierce_damage / 100))
        self.knockback = weapon.knockback + (player.knockback * weapon.knockback_modifier)
        self.crit_chance = (player.crit_chance * weapon.crit_chance_modifier) + weapon.crit_chance
        self.life_steal_chance = (player.life_steal * weapon.life_steal_modifier) + weapon.life_steal

        self.explosion = weapon.explode
        self.explosion_radius = 1 * (1 + player.explosion_size)
        self.explosion_damage = self.damage * (1 + (player.explosion_damage / 100))

        self.enemies_hit = []

        self.radius = 0.15
        self.width = self.radius * 2
        self.height = self.radius * 2


    def set_direction(self, enemies):
        move_speed = 20  # meters per second
        try:
            sorted_enemies = sorted(enemies, key=lambda enemy: (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            while sorted_enemies[0] in self.enemies_hit:
                sorted_enemies.pop()
            enemy = sorted_enemies[0]
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            angle = math.atan2(dy, dx)
            self.start_x = self.x
            self.start_y = self.y
        except IndexError:
            angle = random.randint(0, 200) / 100 * 3.14
        self.vx = move_speed * math.cos(angle)
        self.vy = move_speed * math.sin(angle)

    def update(self, elapsed, frame_context):
        super().update(elapsed, frame_context)

    def should_remove(self):
        return math.sqrt(((self.start_x - self.x) ** 2) + (self.start_y - self.y) ** 2) > self.range or self.peirce < 0

    def hit_enemy(self, enemy, player, enemies, frame_context):
        if enemy not in self.enemies_hit:
            self.enemies_hit.append(enemy)

            if random.randint(0, 100) <= self.crit_chance:
                self.damage *= 2
            if random.randint(0, 100) <= self.life_steal_chance:
                player.hp = min(player.max_hp, player.hp + 1)

            enemy.hp -= self.damage

            if self.explosion:
                player.explosions.add(Explosion((self.x, self.y), self.explosion_radius, 30))
                for enemy2 in enemies:
                    if self.explosion_radius > abs(enemy2.x - self.x) and self.explosion_radius > abs(enemy2.y - self.y):
                        distance = (((enemy2.x - self.x) ** 2) + ((enemy2.y - self.y) ** 2) ** 0.5)
                        if distance < self.explosion_radius:
                            enemy2.hp -= self.explosion_damage * (abs(self.radius - distance) / self.radius)




            # applys knockback on the enemy
            enemy.knockback((self.x, self.y), self.knockback / 50, 30, frame_context.frame)

            if self.bounce > 0:
                self.set_direction(enemies)
            else:
                self.damage *= self.peirce_damage
                self.peirce -= 1


class Explosion(GameSprite):
    def __init__(self, location, radius, duration):
        super().__init__(explosion)
        self.x = location[0]
        self.y = location[1]
        self.radius = radius
        self.width = self.radius * 2
        self.height = self.radius * 2
        self.duration = duration

    def update(self, elapsed, frame_context, *args):
        super().update(elapsed, frame_context)
        self.duration -= 1
        if self.duration < 0:
            self.kill()

image_loader = ImageLoader('assets/projectiles')
default_image = Animation(image_loader.load_images('player-bullet'), 0.2)
explosion = Animation(image_loader.load_images('explosion'))

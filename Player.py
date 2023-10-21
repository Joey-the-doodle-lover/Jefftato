import math
import pygame

from FrameContext import FrameContext
from PlayerAttacks import PlayerAttacks
from Viewport import Viewport
from Weapons import Weapons
from animation import ImageLoader, Animation
from GameSprite import GameSprite


class Player(GameSprite):
    level = 1
    xp = 0
    hp = 50
    max_hp = 50
    kibble = 30

    regeneration = 0
    life_steal = 0
    damage = 1000
    melee_damage = 0
    ranged_damage = 0
    elemental_damage = 0
    attack_speed = 0
    crit_chance = 0
    engineering = 0
    extra_range = 0
    armor = 0
    dodge = 0
    speed = 0
    luck = 0
    harvesting = 0
    consumable_heal = 0
    kibble_heal_chance = 0
    xp_gain = 0
    pick_up_range = 0
    shop_price = 0
    explosion_damage = 0
    explosion_size = 0
    bounces = 0
    peircing = 0
    peircing_damage = 0
    boss_damage = 0
    burn_speed = 0
    burn_spread = 0
    knockback = 0
    double_kibble_chance = 0
    treet_box_value = 0
    free_rerolls = 0

    base_speed = 5  # meters per sec

    last_hit = 0
    inmunity = 0.5  # in seconds

    gun = Weapons(("gun", "basic"), 50, 0, 1, 0, 0, 0.5, 5, 1, 250, 1, 1, -50, 0, 25, 1, 0, 1)
    infinity_gun = Weapons(("gun", "debug"), 1e7, 5, 5, 5, 5, 1 / 60, 100, 0, 1e5, 0, 5, 0, 0, 0, 0, 100, 0)
    knockback_gun = Weapons(("gun", "joke", "debug"), 0, 0, 0, 0, 0, 0.5, 0, 0, 250, 1, 0, -100, 5, 500, 10, 0, 0)
    bounce_test = Weapons(("gun", "test"), 100, 0, 0, 0, 0, 0.5, 0, 0, 500, 0, 0, 0, 100, 0, 0, 0, 0)
    pierce_test = Weapons(("gun", "test"), 1000, 0, 0, 0, 0, 1, 0, 0, 5000, 0, 10, 0, 0, 0, 0, 0, 0)

    weapons = []
    last_attacked = []  # stores the last framed that each weapon attacked on
    weapon_location = []  # stores an array of the weapon locations

    for i in range(len(weapons)):
        last_attacked.append(0)
        weapon_location.append([0, 0])

    weapon_distance = 1
    weapon_radian = 0
    weapon_spin_speed = 10  # in seconds
    projectiles = pygame.sprite.Group()

    def __init__(self):
        super().__init__(dog_idle_animation)

    def update(self, elapsed, arena_bounds, frame, enemys):
        self.player_hit_by_enemys(frame, enemys)

        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

        self.keep_player_on_map(arena_bounds)

        self.set_weapon_locations()

        if (self.animation != dog_woof_animation and self.animation != dog_blush_animation) \
                or self.animation.is_finished():
            if abs(self.vx) > 0.0 or abs(self.vy) > 0.0:
                self.animation = dog_run_animation
            else:
                self.animation = dog_cower_animation if self.cowering else dog_idle_animation

    def controls(self):
        self.vx = 0.0
        self.vy = 0.0

        move_speed = (1.0 + (self.speed / 100.0)) * self.base_speed

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.vy = move_speed
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.vx = -move_speed
            self.flipped = False
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.vy = -move_speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.vx = move_speed
        if abs(self.vx) > 0 and abs(self.vy) > 0:
            self.vx = (self.vx / math.sqrt(2))
            self.vy = (self.vy / math.sqrt(2))

        if keys_pressed[pygame.K_SPACE]:
            self.woof()
        elif keys_pressed[pygame.K_l]:
            self.blush()

        self.cowering = keys_pressed[pygame.K_c]

    @staticmethod
    def create_image(viewport, width, height):
        rect = (0, 0, width, height)

        image_rect = viewport.convert_rect_to_screen(rect)
        image = pygame.Surface((image_rect[2], image_rect[3]))

        color = (80, 0, 0)

        pygame.draw.rect(
            image,
            color,
            image_rect
        )

        return image

    def generate_projectiles(self, frame, enemys):
        for i in range(len(self.weapons)):
            weapon = self.weapons[i]
            if frame > self.last_attacked[i] + (weapon.use_time / (1 + self.attack_speed) * 60):
                bullet = PlayerAttacks(self, i, weapon.damage,
                                       weapon.range + (self.extra_range * weapon.range_modifier),
                                       weapon.pierce + self.peircing,
                                       weapon.pierce_damage + self.peircing_damage,
                                       weapon.bounces + self.bounces, weapon.knockback + self.knockback, weapon,
                                       self.viewport)
                self.projectiles.add(bullet)
                bullet.set_direction(enemies)
                self.last_attacked[i] = frame

    def remove_bullets(self):
        for bullet in self.projectiles:
            if bullet.should_remove():
                bullet.kill()

    def set_weapon_locations(self):
        if len(self.weapons) > 0:
            tau = 6.283185307
            self.weapon_radian += 1 / (self.weapon_spin_speed * 60) * tau
            self.weapon_radian %= tau
            radian_per_weapon = tau / len(self.weapons)
            radian = self.weapon_radian
            for location in self.weapon_location:
                radian += radian_per_weapon
                location[0] = self.x + self.weapon_distance * math.cos(radian)
                location[1] = self.y + self.weapon_distance * math.sin(radian)

    def player_hit_by_enemies(self, frame, enemies):
        if frame > self.last_hit + self.inmunity * 60:
            for enemy in enemies:
                if pygame.Rect.colliderect(self.rect, enemy.rect):
                    self.last_hit = frame
                    self.hp -= enemy.power


image_loader = ImageLoader('assets/jeff')
dog_run_animation = Animation(image_loader.load_images('dog-run'), 0.2)
dog_idle_animation = Animation(image_loader.load_images('dog-idle'), 0.4)
dog_woof_animation = Animation(image_loader.load_images('dog-woof'), 0.25, False)
dog_blush_animation = Animation(image_loader.load_images('dog-blush'), 0.35, False)
dog_cower_animation = Animation(image_loader.load_images('dog-cower'), 0.3)

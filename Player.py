import math
import pygame
from pygame import sprite
from PlayerAttacks import PlayerAttacks

class Player(sprite.Sprite):
    x = 0
    y = 0
    vx = 0
    vy = 0

    height = 0.3
    width = 0.6

    level = 1
    xp = 0
    hp = 10
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
    range = 0
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

    """
    weapon types is a dictinary storing all of the weapons. weapon stat stored as tuple
    0: type, as a tuple
    1: base damage
    2: base use time in seconds
    3: base crit chance
    4: crit chance modifier
    5: base range
    6: range modifier
    7: base peirce
    8: base peirce damage %
    9: base bounces
    10: knockback
    11: life steal
    """
    weapon_types = dict([
        ("gun", (("gun"), 5, 0.5, 5, 1, 5.0, 2, 0, -50, 0, 0.05, 5)),
        ("infinity gun", (("gun", "debug"), 100, 0, 100, 0, 100, 0, 100, 100, 0, 0, 100)),
        ("knockback gun", (("gun"), 0, 0.5, 0, 0, 5.0, 2, 0, 0, 0, 1, 0))
    ])
    weapons = ["infinity gun"]
    last_attacked = [0]  # stores the last framed that each weapon attacked on
    projectiles = pygame.sprite.Group()

    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.image = Player.create_image(self.viewport, self.width, self.height)
        self.rect = self.image.get_rect()

    def update(self, elapsed, arena_bounds):
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

        self.keep_player_on_map(arena_bounds)

        viewport_rect = self.viewport.convert_rect_to_screen(
            (self.x, self.y, self.width, self.height)
        )

        self.rect.x = viewport_rect.x
        self.rect.y = viewport_rect.y

    def keep_player_on_map(self, arena_bounds):
        if self.x > arena_bounds[2]:
            self.x = arena_bounds[2]
        if self.x < arena_bounds[0]:
            self.x = arena_bounds[0]
        if self.y > arena_bounds[3]:
            self.y = arena_bounds[3]
        if self.y < arena_bounds[1]:
            self.y = arena_bounds[1]

    def controls(self):
        self.vx = 0.0
        self.vy = 0.0

        move_speed = (1.0 + (self.speed / 100.0)) * self.base_speed

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.vy = move_speed
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.vx = -move_speed
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.vy = -move_speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.vx = move_speed
        if abs(self.vx) > 0 and abs(self.vy) > 0:
            self.vx = (self.vx / math.sqrt(2))
            self.vy = (self.vy / math.sqrt(2))

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
            if frame > self.last_attacked[i] + (self.weapon_types[weapon][2] / (1 + self.attack_speed) * 60):
                bullet = PlayerAttacks(self, self.weapon_types[weapon][1], self.weapon_types[weapon][5] +
                                       (self.range * self.weapon_types[weapon][6]),
                                       self.weapon_types[weapon][7] + self.peircing,
                                       self.weapon_types[weapon][8] + self.peircing_damage,
                                       self.weapon_types[weapon][9] + self.bounces, weapon,
                                       self.viewport)
                self.projectiles.add(bullet)
                bullet.set_direction(self, enemys)
                self.last_attacked[i] = frame

    def remove_bullets(self):
        for bullet in self.projectiles:
            if bullet.should_remove():
                bullet.kill()

import pygame
import time
from pygame import Rect
import random


class Game:

    def __init__(self, screen):
        self.screen = screen

        self.arena_bounds = (0.0, 0.0, 50.0, 50.0)  # 50 x 50 meters
        view_bounds = (15.0, 15.0, 20.0, 20.0)

        self.viewport = Viewport(screen, view_bounds)

        self.player = Player()
        self.player.x = 25.0
        self.player.y = 25.0

    def run(self):
        clock = pygame.time.Clock()
        fps = 60

        last_time = clock.get_time()

        running = True

        # Main game loop
        while running:
            # Calculate elapsed seconds
            current_time = time.time_ns()
            elapsed = (current_time - last_time) / 1e9
            last_time = current_time

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update object positions, health, state, etc
            self.player.controls()
            self.player.update(elapsed)
            # Draw background
            self.screen.fill((255, 255, 255))

            # Draw all objects
            self.player.draw(self.viewport, self.screen)
            pygame.display.flip()
            clock.tick(fps)


class Viewport:
    def __init__(self, screen, view_bounds):
        self.view_bounds = view_bounds
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.pixels_per_meter = (
            self.screen_width / self.view_bounds[2],
            self.screen_height / self.view_bounds[3]
        )

    def convert_width(self, width):
        return self.pixels_per_meter[0] * width

    def convert_height(self, height):
        return self.pixels_per_meter[1] * height

    def convert_rect_to_screen(self, rect):
        point = self.convert_point_to_screen((rect[0], rect[1]))
        width = self.convert_width(rect[2])
        height = self.convert_height(rect[3])
        return Rect(
            point[0], point[1], width, height
        )

    def convert_point_to_screen(self, arena_location):
        # Subtract the viewport bounds from the world bounds
        view_x = arena_location[0] - self.view_bounds[0]
        view_y = arena_location[1] - self.view_bounds[1]

        # Convert from view coordinates to pixel on screen
        pixel_x = view_x * self.pixels_per_meter[0]
        pixel_y = self.screen_height - (view_y * self.pixels_per_meter[1])

        return pixel_x, pixel_y


    class Enemy:
        def __init__(self, x, y, vx, vy, hp, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.hp = hp
            self.type = typ

    class PlayerAttacks:
        def __init__(self, x, y, vx, vy, dmg, rang, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.range = rang
            self.type = typ

    class EnemyAttacks:
        def __init__(self, x, y, vx, vy, dmg, typ):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.dmg = dmg
            self.type = typ

    class Structures:
        def __init__(self, x, y, typ):
            self.x = x
            self.y = y
            self.type = typ

    class Consumables:
        def __init__(self, x, y, value, typ):
            self.x = x
            self.y = y
            self.value = value
            self.type = typ


class Player:
    """
    hp = health, reg = regeneration, ls = life steal, dmg = damage, mdmg = melee damage, rdmg = ranged damage,
    edmg = elemental damage, a_s = attack speed, crit = crit chance, eng =  engineering, rng = range,
    amr = armor, dg = dodge, spd = speed, lk = luck, harv = harvesting, con_heal consumable heal,
    mhc = material heal chance, xp_g xp gain, pr = pickup range, price = item price, ex_dmg explosion damage,
    ex_size = explosion size, bonc = projectile bounces, prc = projectile peircing, prc_dmg = peircing damage,
    boss = damage agaist bosses, brn_spd = burning speed, brn_sprd = burning spread, kb = knockback,
    dmc = double material chance, trt_bx = materials from treat box, f_rll = free rerolls, tree = tree quanity,
    enm = enemy quanity, enm_spd = enemy speed.
    """
    level = 1
    hp = 10
    kibble = 30
    regeneration = 0
    life_steal = 0
    damage = 0
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

    base_speed = 3.0  # meters per sec

    def update(self, elapsed):
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

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

    def draw(self, viewport, screen):
        height = 0.3
        width = 0.6
        rect = (
            self.x - width / 2,
            self.y + height / 2,
            width,
            height
        )

        color = (0, 0, 0)

        pygame.draw.rect(
            screen,
            color,
            viewport.convert_rect_to_screen(rect)
        )


def create_pygame_screen():
    pygame.init()
    return pygame.display.set_mode((1920, 1080))


def main():
    screen = create_pygame_screen()
    game = Game(screen)

    # Create Game()
    game.run()


if __name__ == '__main__':
    main()

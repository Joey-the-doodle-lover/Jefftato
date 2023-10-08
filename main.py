import math
import random
import time
import pygame
from pygame import Rect
from pygame import sprite


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.aspect_ratio = 1080 / 1920

        self.arena_bounds = (0.0, 0.0, 50.0, 50.0)  # 50 x 50 meters
        zoom = 3
        view_bounds = [15.0 * zoom, 15.0 * zoom, 20.0 * zoom, 20.0 * self.aspect_ratio * zoom]
        self.viewport = Viewport(screen, view_bounds)

        self.player = Player(Viewport(screen, view_bounds))
        self.player.x = 25.0
        self.player.y = 25.0

        self.enemys = []

        self.spot_count = int(
            ((self.arena_bounds[0] + self.arena_bounds[2]) * (self.arena_bounds[1] + self.arena_bounds[3])) / 25)
        self.spot_color = (0, 255, 0)
        self.spot_size_range = (5, 50)  # in cm
        self.spots = []
        self.background_color = (100, 50, 0)

        self.wave = 10

    def run(self):
        pygame.font.init()
        clock = pygame.time.Clock()
        fps = 60
        last_time = clock.get_time()
        frame = 0

        self.generate_spots()

        sprites = pygame.sprite.Group()
        sprites.add(self.player)

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
            self.viewport.move(self.arena_bounds, self.player)

            sprites.update(elapsed, self.arena_bounds)

            self.spawn_enemys(frame, self.wave, self.player)
            self.remove_dead()
            for enemy in self.enemys:
                enemy.get_velocity(self.player)
                enemy.update_location(elapsed)
                enemy.stay_in_bounds(self.arena_bounds)

            self.player.generate_projectiles(frame, self.enemys)
            self.player.remove_bullets()

            for bullet in self.player.projectiles:
                for enemy in self.enemys:
                    if pygame.sprite.collide_circle(enemy, bullet):
                        bullet.hit_enemy(enemy)

                bullet.update(elapsed, self.viewport)

            # Draw background
            self.draw_background()

            # Draw all objects
            sprites.draw(self.screen)
            self.draw_enemys()
            self.draw_bullets()

            # finalize frame
            pygame.display.flip()
            frame += 1
            if frame % 60 == 0:
                print(f"fps: {1 // elapsed}")
            clock.tick(fps)

    def draw_bullets(self):
        for bullet in self.player.projectiles:
            viewx = self.viewport.view_bounds[0]
            viewy = self.viewport.view_bounds[1]
            vieww = self.viewport.view_bounds[2]
            viewh = self.viewport.view_bounds[3]
            if viewx < bullet.x < viewx + vieww and viewy < bullet.y < viewy + viewh:  # if in view
                pygame.draw.circle(self.screen, (255, 255, 0),
                                   self.viewport.convert_point_to_screen((bullet.x, bullet.y)), bullet.radius)

    def generate_spots(self):
        for i in range(self.spot_count):
            self.spots.append(random.randint(0, 5000) / 100)
            self.spots.append(random.randint(0, 5000) / 100)
            self.spots.append(random.randint(self.spot_size_range[0], self.spot_size_range[1]) / 100)

    def draw_background(self):
        self.screen.fill((0, 0, 255))
        pygame.draw.rect(self.screen, self.background_color, self.viewport.convert_rect_to_screen((0, 50, 50, 50)))
        for i in range(self.spot_count):
            location = self.viewport.convert_point_to_screen((self.spots[3 * i], self.spots[(3 * i) + 1]))
            size = self.viewport.convert_width(self.spots[(3 * i) + 2] / 2)
            pygame.draw.circle(self.screen, self.spot_color, location, size)

    def spawn_enemys(self, frame, wave, player):
        if frame % 60 == 0:
            print(f"enemy count: {len(self.enemys)}")
            for i in range(wave):
                self.enemys.append(Enemy(random.randint(0, 50), random.randint(0, 50), 5 * wave, 0, 0, self.viewport))
                # if the enemy spawns next to the player, it will teleport somewhere else.
                while math.sqrt(((self.enemys[len(self.enemys) - 1].x - player.x) ** 2) +
                                ((self.enemys[len(self.enemys) - 1].y - player.y) ** 2)) < 10:
                    self.enemys[len(self.enemys) - 1].x = random.randint(0, 50)
                    self.enemys[len(self.enemys) - 1].y = random.randint(0, 50)

    def draw_enemys(self):
        for enemy in self.enemys:
            viewx = self.viewport.view_bounds[0]
            viewy = self.viewport.view_bounds[1]
            vieww = self.viewport.view_bounds[2]
            viewh = self.viewport.view_bounds[3]
            if viewx < enemy.x < viewx + vieww and viewy < enemy.y < viewy + viewh:  # if in view
                pygame.draw.circle(self.screen, (255, 0, 0),
                                   self.viewport.convert_point_to_screen((enemy.x, enemy.y)), enemy.radius)

    def remove_dead(self):
        index = 0
        for enemy in self.enemys:
            if enemy.hp <= 0:
                self.enemys.pop(index)
            else:
                index += 1


class Viewport:
    def __init__(self, screen, view_bounds):
        self.base_view_bounds = view_bounds
        self.view_bounds = view_bounds
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.pixels_per_meter = (
            self.screen_width / self.view_bounds[2],
            self.screen_height / self.view_bounds[3]
        )

    def move(self, arena_bounds, player):
        movement = player.vx + player.vy
        # self.view_bounds[2] = self.base_view_bounds[2] + (movement / 100)
        # self.view_bounds[3] = self.base_view_bounds[3] + (movement / 100)
        self.view_bounds[0] = player.x - (self.view_bounds[2] / 2)
        self.view_bounds[1] = player.y - (self.view_bounds[3] / 2)
        if self.view_bounds[0] + self.view_bounds[2] > arena_bounds[2] + self.view_bounds[2] * 0.25:
            self.view_bounds[0] = arena_bounds[2] + self.view_bounds[2] * 0.25 - self.view_bounds[2]
        if self.view_bounds[0] < arena_bounds[0] - self.view_bounds[2] * 0.25:
            self.view_bounds[0] = arena_bounds[0] - self.view_bounds[2] * 0.25
        if self.view_bounds[1] + self.view_bounds[3] > arena_bounds[3] + self.view_bounds[3] * 0.25:
            self.view_bounds[1] = arena_bounds[3] - self.view_bounds[3] + self.view_bounds[3] * 0.25
        if self.view_bounds[1] < arena_bounds[1] - self.view_bounds[3] * 0.25:
            self.view_bounds[1] = arena_bounds[1] - self.view_bounds[3] * 0.25

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


class Enemy(pygame.sprite.Sprite):
    vx = 0
    vy = 0

    def __init__(self, x, y, hp, speed, typ, viewport, *groups: pygame.sprite.Sprite):
        super().__init__(*groups)
        self.x = x
        self.y = y

        self.hp = hp
        self.speed = speed
        self.base_speed = 2.5
        self.type = typ

        self.image = pygame.Surface([1920, 1080])
        self.color = (255, 0, 0)
        self.real_radius = 0.25
        self.radius = math.ceil(viewport.convert_width(self.real_radius))

        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

        pygame.draw.circle(self.image, self.color, (self.x, self.y), viewport.convert_width(self.radius))

    def get_velocity(self, player):
        move_speed = (1 + (self.speed / 100)) * self.base_speed

        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)

        self.vx = move_speed * math.cos(angle)
        self.vy = move_speed * math.sin(angle)

    def stay_in_bounds(self, arena_bounds):
        if self.x > arena_bounds[2]:
            self.x = arena_bounds[2]
        if self.x < arena_bounds[0]:
            self.x = arena_bounds[0]
        if self.y > arena_bounds[3]:
            self.y = arena_bounds[3]
        if self.y < arena_bounds[1]:
            self.y = arena_bounds[1]

    def update_location(self, elapsed):
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)


class PlayerAttacks(pygame.sprite.Sprite):
    vx = 0
    vy = 0

    enemys_hit = []

    def __init__(self, player, weapon_dmg, rang, peirce, peirce_dmg, bounce, typ, viewport, *groups: pygame.sprite.Sprite):
        super().__init__(*groups)
        self.x = player.x + (random.randint(-5, 5) / 10)
        self.y = player.y + (random.randint(-5, 5) / 10)
        self.vx = 0
        self.vy = 

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

        pygame.draw.circle(self.image, self.color, (self.x, self.y), viewport.convert_width(self.radius))

    def set_direction(self, player, enemys):
        move_speed = 10
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
        if math.sqrt(((self.start_x - self.x) ** 2) + (self.start_y - self.y) ** 2) > self.range or self.peirce < 0:
            return True
        else:
            return False

    def hit_enemy(self, enemy):
        if enemy not in self.enemys_hit:
            self.enemys_hit.append(enemy)
            enemy.hp -= self.damage
            self.damage *= self.peirce_damage
            self.peirce -= 1


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
    weapons = ["gun"]
    last_attacked = [0]  # stores the last framed that each weapon attacked on
    projectiles = []

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
                self.projectiles.append(
                    PlayerAttacks(self, self.weapon_types[weapon][1], self.weapon_types[weapon][5] +
                                  (self.range * self.weapon_types[weapon][6]),
                                  self.weapon_types[weapon][7] + self.peircing,
                                  self.weapon_types[weapon][8] + self.peircing_damage,
                                  self.weapon_types[weapon][9] + self.bounces, weapon,
                                  self.viewport))
                self.projectiles[len(self.projectiles) - 1].set_direction(self, enemys)
                self.last_attacked[i] = frame

    def remove_bullets(self):
        popped = 0
        for i in range(len(self.projectiles)):
            if self.projectiles[i - popped].should_remove():
                self.projectiles.pop(i - popped)
                popped += 1


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

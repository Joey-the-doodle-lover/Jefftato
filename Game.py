import math
import random
import time
import pygame

from FrameContext import FrameContext
from Player import Player
from Viewport import Viewport
from Enemy import Enemy
from ui import draw_health_bar, draw_stamina_bar


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.aspect_ratio = 1080 / 1920

        self.arena_bounds = (0.0, 0.0, 50.0, 50.0)  # 50 x 50 meters
        zoom = 1
        view_bounds = [15.0 * zoom, 15.0 * zoom, 20.0 * zoom, 20.0 * self.aspect_ratio * zoom]
        self.viewport = Viewport(screen, view_bounds)

        self.player = Player()
        self.player.x = self.arena_bounds[0] + (self.arena_bounds[2] / 2)
        self.player.y = self.arena_bounds[1] + (self.arena_bounds[3] / 2)

        self.enemies = pygame.sprite.Group()

        self.spot_count = int(
            ((self.arena_bounds[0] + self.arena_bounds[2]) * (self.arena_bounds[1] + self.arena_bounds[3])) / 5)
        self.spot_color = (0, 255, 0)
        self.spot_size_range = (5, 50)  # in cm
        self.spots = []
        self.background_color = (100, 50, 0)

        self.wave = 5
        self.state = "wave"
        self.enemy_cap = 200

        # self.font = pygame.font.Font("arial", 16)

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
            frame_context = FrameContext(frame, self.viewport, self.arena_bounds, self.enemies)

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.state == "main menu":
                self.main_menu()
            elif self.state == "wave":
                self.wave_code(elapsed, sprites, frame_context)

            # finalize frame
            pygame.display.flip()
            frame += 1
            if frame % 60 == 0:
                print(f"fps: {1 // elapsed}")
                print(f"projectiles: {len(self.player.projectiles)}")
                print(f"enemy count: {len(self.enemies)}")
                print("")
            clock.tick(fps)

    def generate_spots(self):
        for i in range(self.spot_count):
            self.spots.append(random.randint(int(self.arena_bounds[0]),
                                             int(self.arena_bounds[0]) + int(self.arena_bounds[2] * 100)) / 100)
            self.spots.append(random.randint(int(self.arena_bounds[1]),
                                             int(self.arena_bounds[1]) + int(self.arena_bounds[3] * 100)) / 100)
            self.spots.append(random.randint(self.spot_size_range[0], self.spot_size_range[1]) / 100)

    def draw_background(self):
        self.screen.fill((0, 0, 255))
        pygame.draw.rect(self.screen, self.background_color, self.viewport.convert_rect_to_screen((self.arena_bounds[0],
                                                                                                   self.arena_bounds[
                                                                                                       1] +
                                                                                                   self.arena_bounds[3],
                                                                                                   self.arena_bounds[2],
                                                                                                   self.arena_bounds[
                                                                                                       3])))
        for i in range(self.spot_count):
            location = self.viewport.convert_point_to_screen((self.spots[3 * i], self.spots[(3 * i) + 1]))
            size = self.viewport.convert_width(self.spots[(3 * i) + 2] / 2)
            pygame.draw.circle(self.screen, self.spot_color, location, size)

    def spawn_enemies(self, frame, wave, player):
        if frame % 60 == 0:
            for i in range(min(wave, self.enemy_cap - len(self.enemies))):
                enemy = Enemy(
                    random.randint(int(self.arena_bounds[0] * 100), int(self.arena_bounds[2] * 100)) / 100,
                    random.randint(int(self.arena_bounds[1] * 100), int(self.arena_bounds[3] * 100)) / 100,
                    5 * wave, 0, wave, "default", self.viewport)
                self.enemies.add(enemy)

    def draw_weapons(self):
        for weapon in self.player.weapon_location:
            location = self.viewport.convert_point_to_screen((weapon[0], weapon[1]))
            radius = self.viewport.convert_width(0.15)
            pygame.draw.circle(self.screen, (0, 255, 255), location, radius)

    def wave_code(self, elapsed, sprites, frame_context: FrameContext):
        # Update object positions, health, state, etc
        self.player.controls(self.enemies, frame_context)
        self.viewport.move(self.arena_bounds, self.player)

        sprites.update(elapsed, frame_context)

        self.spawn_enemies(frame_context.frame, self.wave, self.player)
        self.enemies.update(elapsed, self.enemies, self.player, frame_context)

        self.player.generate_projectiles(frame_context.frame, self.enemies, self.viewport)
        self.player.remove_bullets()

        for bullet in self.player.projectiles:
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(enemy, bullet):
                    bullet.hit_enemy(enemy, self.player, self.enemies)

            bullet.update(elapsed, self.viewport)

        # Draw background
        self.draw_background()

        # Draw all objects
        sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player.projectiles.draw(self.screen)
        self.draw_weapons()
        draw_health_bar(self.player, self.screen)
        draw_stamina_bar(self.player, self.screen)

        def end_wave():
            self.state = "shop"
            for enemy in self.enemies:
                enemy.kill()
            for bullet in self.player.projectiles:
                bullet.kill()

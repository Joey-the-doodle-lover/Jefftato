import math
import random
import time
import pygame
from Player import Player
from Viewport import Viewport
from Enemy import Enemy


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.aspect_ratio = 1080 / 1920

        self.arena_bounds = (0.0, 0.0, 25.0, 25.0)  # 50 x 50 meters
        zoom = 2
        view_bounds = [15.0 * zoom, 15.0 * zoom, 20.0 * zoom, 20.0 * self.aspect_ratio * zoom]
        self.viewport = Viewport(screen, view_bounds)

        self.player = Player(Viewport(screen, view_bounds))
        self.player.x = 25.0
        self.player.y = 25.0

        self.enemys = pygame.sprite.Group()

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
            self.enemys.update(elapsed, self.enemys, self.player, self.arena_bounds, self.viewport)

            self.player.generate_projectiles(frame, self.enemys)
            self.player.remove_bullets()

            for bullet in self.player.projectiles:
                for enemy in self.enemys:
                    if pygame.sprite.collide_circle(enemy, bullet):
                        bullet.hit_enemy(enemy, self.player, self.enemys)

                bullet.update(elapsed, self.viewport)

            # Draw background
            self.draw_background()

            # Draw all objects
            sprites.draw(self.screen)
            self.enemys.draw(self.screen)
            self.player.projectiles.draw(self.screen)

            # finalize frame
            pygame.display.flip()
            frame += 1
            if frame % 60 == 0:
                print(f"fps: {1 // elapsed}")
            clock.tick(fps)

    def generate_spots(self):
        for i in range(self.spot_count):
            self.spots.append(random.randint(int(self.arena_bounds[0]), int(self.arena_bounds[0]) + int(self.arena_bounds[2] * 100)) / 100)
            self.spots.append(random.randint(int(self.arena_bounds[1]), int(self.arena_bounds[1]) + int(self.arena_bounds[3] * 100)) / 100)
            self.spots.append(random.randint(self.spot_size_range[0], self.spot_size_range[1]) / 100)

    def draw_background(self):
        self.screen.fill((0, 0, 255))
        pygame.draw.rect(self.screen, self.background_color, self.viewport.convert_rect_to_screen((self.arena_bounds[0], self.arena_bounds[1] + self.arena_bounds[3], self.arena_bounds[2], self.arena_bounds[3])))
        for i in range(self.spot_count):
            location = self.viewport.convert_point_to_screen((self.spots[3 * i], self.spots[(3 * i) + 1]))
            size = self.viewport.convert_width(self.spots[(3 * i) + 2] / 2)
            pygame.draw.circle(self.screen, self.spot_color, location, size)

    def spawn_enemys(self, frame, wave, player):
        if frame % 60 == 0:
            print(f"enemy count: {len(self.enemys)}")
            for i in range(wave):
                enemy = Enemy(random.randint(0, 50), random.randint(0, 50), 5 * wave, 0, "default", self.viewport)
                self.enemys.add(enemy)
                # if the enemy spawns next to the player, it will teleport somewhere else.
                while math.sqrt(((enemy.x - player.x) ** 2) +
                                ((enemy.y - player.y) ** 2)) < 10:
                    enemy.x = random.randint(0, 50)
                    enemy.y = random.randint(0, 50)

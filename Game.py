import random
import time
import pygame

from FrameContext import FrameContext
from ParentSpites.GameSprite import GameSprite
from GameSprites.Player import Player
from Viewport import Viewport
from GameSprites.Enemy import Enemy
from ParentSpites.animation import ImageLoader, Animation
from ui import draw_health_bar, draw_stamina_bar, draw_ability_cooldowns


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
        self.next_spawn = 1

        self.water = BackgroundSprite(25, water)
        self.sand = BackgroundSprite(0, sand)
        self.grass = BackgroundSprite(-5, grass)

        self.wave = 20
        self.state = "wave"
        self.enemy_cap = 200

    def run(self):
        pygame.font.init()
        clock = pygame.time.Clock()
        fps = 60
        last_time = clock.get_time()
        frame = 0

        previus = 0

        sprites = pygame.sprite.Group()
        sprites.add(self.water, self.sand, self.grass, self.player)

        running = True
        last_time = time.time_ns()
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
                new = time.time_ns()
                passed = (current_time - previus) / 1e9
                previus = new

                print(f"fps: {round(60 / passed, 3)}")
                print(f"projectiles: {len(self.player.projectiles)}")
                print(f"explosions: {len(self.player.explosions)}")
                print(f"enemy count: {len(self.enemies)}\n")
            clock.tick(fps)

    def spawn_enemies(self, wave, elapsed):
        self.next_spawn -= elapsed
        while self.next_spawn < 0 and len(self.enemies) < self.enemy_cap:
            self.next_spawn += 1 / wave
            enemy = Enemy(random.randint(int(self.arena_bounds[0] * 100), int((self.arena_bounds[0] + self.arena_bounds[2] / 2) * 100)) / 100,
                          random.randint(int(self.arena_bounds[1] * 100), int((self.arena_bounds[1] + self.arena_bounds[3] / 2) * 100)) / 100,
                          wave * 5, 1, wave, "enemy")
            self.enemies.add(enemy)

    def draw_weapons(self):
        for weapon in self.player.weapon_location:
            location = self.viewport.convert_point_to_screen((weapon[0], weapon[1]))
            radius = self.viewport.convert_width(0.15)
            pygame.draw.circle(self.screen, (0, 255, 255), location, radius)

    def wave_code(self, elapsed, sprites, frame_context: FrameContext):
        # Update object positions, health, state, etc
        self.player.controls(self.enemies, elapsed)
        self.player.controls(self.enemies, elapsed)
        self.viewport.move(self.arena_bounds, self.player)

        sprites.update(elapsed, frame_context)

        self.spawn_enemies(self.wave, elapsed)
        self.enemies.update(elapsed, self.enemies, self.player, frame_context)

        self.player.generate_projectiles(elapsed, self.enemies)
        self.player.remove_bullets()

        for bullet in self.player.projectiles:
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(enemy, bullet):
                    bullet.hit_enemy(enemy, self.player, self.enemies, frame_context)

            bullet.update(elapsed, frame_context)

        self.player.explosions.update(elapsed, frame_context)

        # Draw all objects
        sprites.draw(self.screen)
        self.player.explosions.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player.projectiles.draw(self.screen)
        self.draw_weapons()
        draw_health_bar(self.player, self.screen)
        draw_stamina_bar(self.player, self.screen)
        draw_ability_cooldowns(self.player, frame_context.frame, self.screen)

        def end_wave():
            self.state = "shop"
            for enemy in self.enemies:
                enemy.kill()
            for bullet in self.player.projectiles:
                bullet.kill()


class BackgroundSprite(GameSprite):
    def __init__(self, extra_space, animation):
        super().__init__(animation)
        self.extra = extra_space

    def update(self, elapsed, frame_context):
        super().update(elapsed, frame_context)
        arena_bounds = frame_context.arena_bounds
        self.width = arena_bounds[2] + (2 * self.extra)
        self.height = arena_bounds[3] + (2 * self.extra)
        self.x = arena_bounds[0] - self.extra + (self.width / 2)
        self.y = arena_bounds[1] - self.extra + (self.height / 2)


image_loader = ImageLoader('assets/background')
grass = Animation(image_loader.load_images('grass'), 2)
water = Animation(image_loader.load_images('ocean'))
sand = Animation(image_loader.load_images('beach'))


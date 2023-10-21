import time
import pygame

from pathlib import Path

from FrameContext import FrameContext
from Viewport import Viewport


class Image:
    def __init__(self, surface):
        self.base_surface = surface
        self.surface = self.base_surface
        self.flipped = False

    def get(self, width, height, flipped=False):
        rect = self.surface.get_rect()
        if rect.w != width or rect.h != height or self.flipped != flipped:
            self.surface = pygame.transform.scale(self.base_surface, (width, height))
            if flipped:
                self.surface = pygame.transform.flip(self.surface, True, False)
            self.flipped = flipped
        return self.surface


class ImageLoader:
    def __init__(self, assets_folder):
        self.assets_folder = Path(assets_folder)

    def load_image(self, name):
        path = self.assets_folder / name
        return self.load_image_at_path(path)

    def load_images(self, prefix):
        paths = self.assets_folder.glob(prefix + '*')
        return list(map(self.load_image_at_path, sorted(paths)))

    def load_image_at_path(self, path):
        return Image(pygame.image.load(path))


class Animation:
    def __init__(self, images, frame_duration=0.25, loop=True):
        self.images = images
        self.frame_duration = frame_duration
        self.loop = loop
        self.reset()

    def reset(self):
        self.current_frame = 0
        self.total_elapsed = 0.0

    def update(self, elapsed):
        self.total_elapsed += elapsed
        self.current_frame = int(self.total_elapsed / self.frame_duration)
        if self.loop:
            self.current_frame = self.current_frame % len(self.images)
        if self.current_frame >= len(self.images):
            self.current_frame = len(self.images) - 1

    def is_finished(self):
        return self.total_elapsed > self.frame_duration * len(self.images)

    def get_image(self):
        return self.images[self.current_frame]


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation: Animation, *groups):
        super().__init__(*groups)

        self.flipped = False

        self.animation = animation
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.image = self.animation.get_image().get(self.rect.w, self.rect.h, self.flipped)

    def update(self, elapsed, frame_context: FrameContext, *args):
        self.animation.update(elapsed)
        self.image = self.animation.get_image().get(self.rect.w, self.rect.h, self.flipped)



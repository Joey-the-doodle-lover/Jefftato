from pygame.sprite import Group

from Viewport import Viewport


class FrameContext:
    def __init__(self, frame: int, viewport: Viewport, arena_bounds, enemies: Group):
        self.frame = frame
        self.viewport = viewport
        self.arena_bounds = arena_bounds
        self.enemies = enemies

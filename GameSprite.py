from FrameContext import FrameContext
from animation import AnimatedSprite, Animation


class GameSprite(AnimatedSprite):
    def __init__(self, animation: Animation, *groups):
        super().__init__(animation, *groups)

        # World coordinates (meters)
        self.x = 0.0
        self.y = 0.0
        self.width = 1.0
        self.height = 1.0

        self.stay_in_bounds = True

        # Velocity (meters / sec)
        self.vx = 0.0
        self.vy = 0.0

    def update(self, elapsed, frame_context: FrameContext, *args):
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

        if self.stay_in_bounds:
            self.check_bounds(frame_context.arena_bounds)

        # Convert from world coordinates to viewport
        self.rect = frame_context.viewport.convert_rect_to_screen(
            (self.x - (self.width / 2), self.y + (self.height / 2), self.width, self.height)
        )

        # Now that the coordinates are updated, let the parent class update the animation and image
        super().update(elapsed, frame_context, *args)

    def check_bounds(self, arena_bounds):
        if self.x > arena_bounds[2]:
            self.x = arena_bounds[2]
        if self.x < arena_bounds[0]:
            self.x = arena_bounds[0]
        if self.y > arena_bounds[3]:
            self.y = arena_bounds[3]
        if self.y < arena_bounds[1]:
            self.y = arena_bounds[1]

from pygame import Rect


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

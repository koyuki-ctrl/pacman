from pyray import (
    load_texture,
    unload_texture,
    draw_texture_ex
)
from colors import WHITE


class GameScene:
    def __init__(self):
        self.bg = load_texture("assets/pacman_bg_title.jpeg")

    def draw(self):
        draw_texture_ex(self.bg, (0, 0), 0.0, 0.95, WHITE)

    def cleanup(self):
        unload_texture(self.bg)

from pyray import (
    load_texture,
    unload_texture,
    draw_texture_ex
)
from colors import WHITE
from utils import Utils


class ControlScene:
    def __init__(self):
        self.bg = load_texture("assets/pacman_bg_title.jpeg")
        self.return_btn = load_texture("assets/return-game-button.png")
        self.return_btn_hover = load_texture(
            "assets/return-game-button-hovered.png"
        )
        self.utils = Utils()
        self.menu = load_texture("assets/game_control.png")

    def draw(self):
        draw_texture_ex(self.bg, (0, 0), 0.0, 0.95, WHITE)
        draw_texture_ex(self.menu, (150, 80), 0.0, 1, WHITE)
        if self.utils.draw_button_image(
            self.return_btn, self.return_btn_hover,
            (10, 10), 0.0, 0.3, WHITE
        ):
            return "menu"

    def cleanup(self):
        unload_texture(self.bg)
        unload_texture(self.return_btn)
        unload_texture(self.return_btn_hover)

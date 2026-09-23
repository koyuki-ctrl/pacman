from pyray import (
    unload_texture,
    load_texture,
    draw_texture_ex
)
from utils import Utils
from colors import WHITE


class MenuScene:
    def __init__(self) -> None:

        self.bg = load_texture("assets/pacman_bg_title.jpeg")
        self.logo = load_texture("assets/pacman_Logo.png")

        self.start_btn = load_texture("assets/start-game-button.png")
        self.start_btn_hover = load_texture(
            "assets/start-game-button-hovered.png"
        )
        self.command_btn = load_texture("assets/command-game-button.png")
        self.command_btn_hover = load_texture(
            "assets/command-game-button-hovered.png"
        )
        self.high_score_btn = load_texture("assets/highScore-game-button.png")
        self.high_score_btn_hover = load_texture(
            "assets/highScore-game-button-hovered.png"
        )
        self.quit_btn = load_texture("assets/quit-game-button.png")
        self.quit_btn_hover = load_texture(
            "assets/quit-game-button-hovered.png"
        )
        self.utils = Utils()

    def draw(self) -> str | None:
        draw_texture_ex(self.bg, (0, 0), 0.0, 0.95, WHITE)
        draw_texture_ex(self.logo, (300, 0), 0.0, 1.0, WHITE)

        if self.utils.draw_button_image(
            self.start_btn, self.start_btn_hover,
            (500, 300), 0.0, 0.7, WHITE
        ):
            return "game"

        elif self.utils.draw_button_image(
            self.command_btn, self.command_btn_hover,
            (500, 380), 0.0, 0.7, WHITE
        ):
            return "command"

        elif self.utils.draw_button_image(
            self.high_score_btn, self.high_score_btn_hover,
            (500, 460), 0.0, 0.7, WHITE
        ):
            return "score"

        elif self.utils.draw_button_image(
            self.quit_btn, self.quit_btn_hover,
            (500, 550), 0.0, 0.7, WHITE
        ):
            return "quit"
        else:
            return None

    def cleanup(self) -> None:
        unload_texture(self.bg)
        unload_texture(self.logo)
        unload_texture(self.start_btn)
        unload_texture(self.start_btn_hover)
        unload_texture(self.command_btn)
        unload_texture(self.command_btn_hover)
        unload_texture(self.high_score_btn)
        unload_texture(self.high_score_btn_hover)
        unload_texture(self.quit_btn)
        unload_texture(self.quit_btn_hover)

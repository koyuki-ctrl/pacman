from pyray import (
    load_texture,
    unload_texture,
    draw_texture_ex,
    is_key_pressed,
    KeyboardKey
)
from colors import WHITE
from maze import Maze
from parsing import GameConfigFile
from pacgum import PacgumManager
from utils import Utils


class GameScene:
    MAZE_COLS = 31
    MAZE_ROWS = 28

    def __init__(self, w, h):
        self.maze = Maze()
        self.maze_obj = self.maze.load_maze(
            width=self.MAZE_COLS,
            height=self.MAZE_ROWS,
            seed=45,
        )
        self.w = w
        self.h = h
        self.bg = load_texture("assets/pacman_bg_title.jpeg")
        self.bg_color = load_texture("assets/game_maze.png")
        self.pause_menu = load_texture("assets/pause_game.png")
        self.ready_menu = load_texture("assets/Ready.png")
        self.home_btn = load_texture('assets/return-game-button.png')
        self.home_btn_hovered = load_texture(
            "assets/return-game-button-hovered.png"
        )
        self.restart_btn = load_texture("assets/restart-game-button@2x.png")
        self.restart_btn_hovered = load_texture(
            "assets/restart-game-button-hovered.png")
        self.margin = 10

        self.cell_w = 0
        self.cell_h = 0
        self.offset_x = 0
        self.offset_y = 0
        self._layout_ready = False
        self.json_config_file = GameConfigFile.from_json()

        self.pacgum_manager = PacgumManager(
            self.maze_obj.maze,
            nb_pacgum=self.json_config_file.pacgum,
        )
        self.paused = False
        self.is_first = True
        self.ready = True
        self.counter = 0
        self.utils = Utils()

    def _ensure_layout(self, screen_w: int, screen_h: int) -> None:
        if self._layout_ready:
            return

        cols = self.MAZE_COLS
        rows = self.MAZE_ROWS

        cw = (screen_w - 2 * self.margin) // cols
        ch = (screen_h - 2 * self.margin) // rows
        self.cell_w = self.cell_h = max(1, min(cw, ch))

        maze_px_w = cols * self.cell_w
        maze_px_h = rows * self.cell_h

        self.offset_x = (screen_w - maze_px_w) // 2
        self.offset_y = (screen_h - maze_px_h) // 2

        self._layout_ready = True

    def draw(self, screen_w: int, screen_h: int) -> None | str:
        draw_texture_ex(self.bg, (0, 0), 0.0, 0.95, WHITE)
        draw_texture_ex(self.bg_color, (0, 0), 0.0, 1, WHITE)

        self._ensure_layout(screen_w, screen_h)

        self.maze.draw_maze(
            self.maze_obj,
            self.cell_w,
            self.cell_h,
            self.offset_x,
            self.offset_y,
            thick=2,
            color=WHITE,
        )

        self.pacgum_manager.draw(
            self.cell_w, self.cell_h,
            self.offset_x, self.offset_y,
            color=WHITE,
        )
        if is_key_pressed(KeyboardKey.KEY_SPACE):
            if self.is_first:
                self.ready = False

            if not self.is_first or self.counter == 1:
                self.paused = not self.paused
            self.counter = 1

        if self.ready:
            draw_texture_ex(
                self.ready_menu, (self.w / 3, self.h / 3), 0.0, 1.0, WHITE)

        if self.paused:
            action = self.pause_game_menu()
            if action is not None:
                return action

        return None

    def cleanup(self) -> None:
        unload_texture(self.bg)
        unload_texture(self.bg_color)
        unload_texture(self.pause_menu)
        unload_texture(self.ready_menu)
        unload_texture(self.home_btn)
        unload_texture(self.home_btn_hovered)
        unload_texture(self.restart_btn)
        unload_texture(self.restart_btn_hovered)

    def pause_game_menu(self) -> str | None:
        draw_texture_ex(
            self.pause_menu, (self.w / 3, self.h / 3), 0.0, 1.0, WHITE)

        if self.utils.draw_button_image(
            self.home_btn,
            self.home_btn_hovered,
            (self.w / 2.3, self.h / 1.8),
            0.0, 0.4, WHITE
        ):
            return "menu"

        elif self.utils.draw_button_image(
            self.restart_btn,
            self.restart_btn_hovered,
            (self.w / 1.9, self.h / 1.8),
            0.0, 0.4, WHITE
        ):
            return 'game'
        else:
            return None

    def over_game(self):
        pass

from pyray import (
    load_texture,
    unload_texture,
    draw_texture_ex,
)
from colors import WHITE
from maze import Maze


class GameScene:
    MAZE_COLS = 31
    MAZE_ROWS = 28

    def __init__(self):
        self.maze = Maze()
        self.maze_obj = self.maze.load_maze(
            width=self.MAZE_COLS,
            height=self.MAZE_ROWS,
            seed=45,
        )
        self.bg = load_texture("assets/pacman_bg_title.jpeg")
        self.bg_color = load_texture("assets/game_maze.png")
        self.margin = 10

        self.cell_w = 0
        self.cell_h = 0
        self.offset_x = 0
        self.offset_y = 0
        self._layout_ready = False

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

    def draw(self, screen_w: int, screen_h: int) -> None:
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

    def cleanup(self) -> None:
        unload_texture(self.bg)

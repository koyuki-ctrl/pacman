from __future__ import annotations
from enum import Enum
import pyautogui
from pyray import (
    get_window_position,
    draw_texture_ex,
    is_mouse_button_pressed,
    draw_pixel,
    MouseButton
)


class SceneModel(Enum):
    MENU = 0
    GAME = 1
    HIGHSCORE = 2
    COMMAND = 3


class Utils:
    def get_mouse_position(self) -> tuple[int, int]:
        global_x, global_y = pyautogui.position()
        window_pos = get_window_position()

        mx = global_x - int(window_pos.x)
        my = global_y - int(window_pos.y)

        return (mx, my)

    def draw_button_image(
        self,
        base_btn,
        hover_btn,
        position: tuple,
        rotation: float,
        scale: float,
        color: tuple,
    ) -> bool:
        x, y = position
        w = base_btn.width * scale
        h = base_btn.height * scale

        mx, my = self.get_mouse_position()
        hover = (x <= mx <= x + w) and (y <= my <= y + h)

        if hover:
            draw_texture_ex(hover_btn, (x + 10, y), rotation, scale, color)
        else:
            draw_texture_ex(base_btn, position, rotation, scale, color)
        return hover and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)

    def draw_line(
            self,
            x0: int,
            y0: int,
            x1: int,
            y1: int,
            color: tuple[int, int, int]
    ) -> None:
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else - 1
        sy = 1 if y0 < y1 else - 1
        err = dx + dy

        while True:
            draw_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = err << 1
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dy:
                err += dx
                y0 += sy

    def hline(
            self,
            x: int,
            y: int,
            length: int,
            color: tuple[int, int, int]
    ) -> None:
        for i in range(length):
            draw_pixel(x + i, y, color)

    def vline(
            self,
            x: int,
            y: int,
            length: int,
            color: tuple[int, int, int]
    ) -> None:
        for i in range(length):
            draw_pixel(x, y + i, color)

    def thick_hline(
            self, x: int, y: int, length: int, thick: int, color
    ) -> None:
        for t in range(thick):
            self.hline(x, y + t, length, color)

    def thick_vline(
            self, x: int, y: int, length: int, thick: int, color
    ) -> None:
        for t in range(thick):
            self.vline(x + t, y, length, color)

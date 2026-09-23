from enum import Enum
import pyautogui
from pyray import (
    get_window_position,
    draw_texture_ex,
    is_mouse_button_pressed,
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

        mx, my = Utils().get_mouse_position()
        hover = (x <= mx <= x + w) and (y <= my <= y + h)

        if hover:
            draw_texture_ex(hover_btn, (x + 10, y), rotation, scale, color)
        else:
            draw_texture_ex(base_btn, position, rotation, scale, color)
        return hover and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)

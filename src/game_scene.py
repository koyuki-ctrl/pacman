from pyray import draw_text
from colors import WHITE


class GameScene:
    def __init__(self):
        pass

    def draw(self):
        draw_text("Hello Game Scene", 80, 80, 25, WHITE)

    def cleanup(self):
        pass

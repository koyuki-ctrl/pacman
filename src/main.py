from pyray import (
    window_should_close,
    init_window,
    begin_drawing,
    end_drawing,
    close_window,
    clear_background
)
from colors import BLACK
from utils import SceneModel
from menu_scene import MenuScene
from game_scene import GameScene
from control_scene import ControlScene
from hight_score import HighScoreScene


class App:
    def __init__(self):
        self.scene_status = SceneModel.MENU.value
        self.game_scene = None
        self.high_score_scene = None
        self.menu_scene = None
        self.command_scene = None
        self.w = 0
        self.h = 0

    def init_window(self, w: int, h: int, title: str) -> None:
        self.w = w
        self.h = h

        init_window(self.w, self.h, title)
        self.menu_scene = MenuScene()

    def run(self) -> None:
        while not window_should_close():
            clear_background(BLACK)
            begin_drawing()
            if self.scene_status == SceneModel.MENU.value:
                action = self.menu_scene.draw()
                if action == "game":
                    self.game_scene = GameScene()
                    self.scene_status = SceneModel.GAME.value
                elif action == "command":
                    self.command_scene = ControlScene()
                    self.scene_status = SceneModel.COMMAND.value
                elif action == "score":
                    self.high_score_scene = HighScoreScene()
                    self.scene_status = SceneModel.HIGHSCORE.value
                elif action == "quit":
                    break

            elif self.scene_status == SceneModel.HIGHSCORE.value:
                action = self.high_score_scene.draw()
                if action == "menu":
                    self.scene_status = SceneModel.MENU.value
            elif self.scene_status == SceneModel.GAME.value:
                self.game_scene.draw()
            elif self.scene_status == SceneModel.COMMAND.value:
                action = self.command_scene.draw()
                if action == "menu":
                    self.scene_status = SceneModel.MENU.value

            end_drawing()

        if action == "game":
            GameScene().cleanup()
        elif action == "command":
            ControlScene().cleanup()
        elif action == "score":
            HighScoreScene().cleanup()

        close_window()


if __name__ == "__main__":
    app = App()
    app.init_window(1280, 720, "Pacman")
    app.run()

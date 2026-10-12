from pyray import (
    window_should_close,
    init_window,
    begin_drawing,
    end_drawing,
    close_window,
    clear_background,
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
        action = None

        while not window_should_close():
            clear_background(BLACK)
            begin_drawing()

            # -------- MENU --------
            if self.scene_status == SceneModel.MENU.value:
                action = self.menu_scene.draw()

                if action == "game":
                    self.game_scene = GameScene(w=self.w, h=self.h)
                    self.scene_status = SceneModel.GAME.value
                elif action == "command":
                    self.command_scene = ControlScene()
                    self.scene_status = SceneModel.COMMAND.value
                elif action == "score":
                    self.high_score_scene = HighScoreScene()
                    self.scene_status = SceneModel.HIGHSCORE.value
                elif action == "quit":
                    break

            # -------- HIGHSCORE --------
            elif self.scene_status == SceneModel.HIGHSCORE.value:
                action = self.high_score_scene.draw()
                if action == "menu":
                    self.high_score_scene.cleanup()
                    self.high_score_scene = None
                    self.scene_status = SceneModel.MENU.value

            # -------- GAME --------
            elif self.scene_status == SceneModel.GAME.value:
                action = self.game_scene.draw(self.w, self.h)

                if action == "menu":
                    self.game_scene.cleanup()
                    self.game_scene = None
                    self.scene_status = SceneModel.MENU.value

                elif action == "game":
                    self.game_scene.cleanup()
                    self.game_scene = GameScene(w=self.w, h=self.h)

            elif self.scene_status == SceneModel.COMMAND.value:
                action = self.command_scene.draw()
                if action == "menu":
                    self.command_scene.cleanup()
                    self.command_scene = None
                    self.scene_status = SceneModel.MENU.value

            end_drawing()

        if self.game_scene is not None:
            self.game_scene.cleanup()
        if self.command_scene is not None:
            self.command_scene.cleanup()
        if self.high_score_scene is not None:
            self.high_score_scene.cleanup()
        if self.menu_scene is not None:
            self.menu_scene.cleanup()

        close_window()


if __name__ == "__main__":
    app = App()
    app.init_window(1280, 720, "Pacman")
    app.run()

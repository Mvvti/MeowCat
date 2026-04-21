import sys

from PyQt6.QtWidgets import QApplication

from src.animator import Animator
from src.behavior import CatBehavior
from src.sprite_sheet import load_sprite_sheet
from src.tray import CatTray
from src.window import CatWindow


def main() -> None:
    app = QApplication(sys.argv)

    load_sprite_sheet("cat animation/64x64/2d")
    window = CatWindow()
    window.show()

    tray = CatTray(app=app, window=window)
    animator = Animator(fps=8, on_frame=window.set_frame)
    behavior = CatBehavior(window=window, animator=animator)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

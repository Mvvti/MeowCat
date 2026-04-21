from __future__ import annotations

import ctypes

from PIL import Image
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class FoodWindow(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setStyleSheet("background: transparent;")
        self.setFixedSize(48, 48)

        pil_image = Image.open("assets/vecteezy_fish-bone-logo-icon_32514470.jpg").convert("RGBA")
        pixels = []
        for r, g, b, a in pil_image.getdata():
            if r > 200 and g > 200 and b > 200:
                pixels.append((r, g, b, 0))
            else:
                pixels.append((r, g, b, a))
        pil_image.putdata(pixels)
        pil_image = pil_image.resize((48, 48), Image.LANCZOS)

        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, 48, 48, QImage.Format.Format_RGBA8888)
        self._fish_pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(self._fish_pixmap)
        self.hide()

    def _apply_win32_fixes(self) -> None:
        try:
            hwnd = int(self.winId())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_NOACTIVATE = 0x08000000
            ex = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(
                hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED | WS_EX_NOACTIVATE
            )
        except Exception:
            pass

    def show_at(self, x: int, y: int) -> None:
        self.move(x, y)
        self.show()
        self._apply_win32_fixes()
        self._send_to_bottom()

    def _send_to_bottom(self) -> None:
        try:
            hwnd = int(self.winId())
            HWND_BOTTOM = 1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_BOTTOM, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
        except Exception:
            pass

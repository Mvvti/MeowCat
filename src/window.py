from __future__ import annotations

import ctypes
import ctypes.wintypes
from typing import Callable

from PIL import Image, ImageDraw
from PIL.Image import Transpose
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QMouseEvent, QPixmap, QShowEvent
from PyQt6.QtWidgets import QLabel

_TRANSPOSE_MAP = {
    90: Transpose.ROTATE_90,
    180: Transpose.ROTATE_180,
    270: Transpose.ROTATE_270,
}


class CatWindow(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self._pixmap: QPixmap | None = None
        self._on_click: Callable[[], None] | None = None
        self._rotation: int = 0

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setStyleSheet("background: transparent;")
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setFixedSize(128, 128)
        self._bottom_timer = QTimer(self)
        self._bottom_timer.timeout.connect(self._send_to_bottom)
        self._bottom_timer.start(1000)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
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

            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_DONOTROUND = 1
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_DONOTROUND)),
                ctypes.sizeof(ctypes.c_int),
            )

            class MARGINS(ctypes.Structure):
                _fields_ = [
                    ("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int),
                ]

            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(
                hwnd, ctypes.byref(MARGINS(0, 0, 0, 0))
            )
        except Exception:
            pass

    def set_frame(self, pil_image: Image.Image) -> None:
        if self._rotation == 0:
            canvas = Image.new("RGBA", pil_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(canvas)
            cx = 64
            draw.ellipse(
                [cx - 28, 120, cx + 28, 130],
                fill=(0, 0, 0, 80),
            )
            canvas.paste(pil_image, (0, 0), pil_image)
            pil_image = canvas
        if self._rotation in _TRANSPOSE_MAP:
            pil_image = pil_image.transpose(_TRANSPOSE_MAP[self._rotation])
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, 128, 128, QImage.Format.Format_RGBA8888)
        self._pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(self._pixmap)

    def set_rotation(self, degrees: int) -> None:
        self._rotation = degrees % 360

    def move_to(self, x: int, y: int) -> None:
        self.move(x, y)

    def set_on_click(self, callback: Callable[[], None]) -> None:
        self._on_click = callback

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._on_click is not None:
            self._on_click()
        super().mousePressEvent(event)

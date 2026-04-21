from __future__ import annotations

from typing import Callable

from PIL import Image
from PyQt6.QtCore import QTimer

from src.sprite_sheet import get_frames


class Animator:
    def __init__(self, fps: int, on_frame: Callable[[Image.Image], None]) -> None:
        self._fps = fps
        self._on_frame = on_frame
        self._frames: list[Image.Image] = []
        self._index = 0

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)

    def play(self, anim_name: str) -> None:
        self._frames = get_frames(anim_name)
        self._index = 0

        if not self._frames:
            self.stop()
            return

        interval_ms = 1000 // self._fps
        self._timer.start(interval_ms)

    def stop(self) -> None:
        self._timer.stop()

    def _tick(self) -> None:
        if not self._frames:
            return

        frame = self._frames[self._index]
        self._on_frame(frame)
        self._index = (self._index + 1) % len(self._frames)

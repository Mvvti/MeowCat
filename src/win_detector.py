from __future__ import annotations

from typing import Any

import win32gui


def get_windows() -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []

    def _enum_callback(hwnd: int, _: int) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()
        if not title:
            return

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        if width == 0 or height == 0:
            return

        windows.append(
            {
                "hwnd": hwnd,
                "title": title,
                "rect": (left, top, right, bottom),
            }
        )

    win32gui.EnumWindows(_enum_callback, 0)
    return windows


def find_window_edge_at(cat_x: int, cat_y: int, cat_w: int = 64) -> dict[str, Any] | None:
    cat_left = cat_x
    cat_right = cat_x + cat_w
    cat_bottom = cat_y + 64
    tolerance = 10

    best_match: dict[str, Any] | None = None
    best_delta: int | None = None

    for window in get_windows():
        left, top, right, _ = window["rect"]
        overlap_width = min(cat_right, right) - max(cat_left, left)
        if overlap_width <= 0:
            continue

        delta = abs(cat_bottom - top)
        if delta > tolerance:
            continue

        if best_delta is None or delta < best_delta:
            best_match = window
            best_delta = delta

    return best_match

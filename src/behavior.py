from __future__ import annotations

import ctypes
import ctypes.wintypes
import math
import random

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QCursor

from src.animator import Animator
from src.food_window import FoodWindow
from src.win_detector import find_window_edge_at
from src.window import CatWindow

_BUBBLE_TEXTS = [
    "Miau!",
    "Mrrr...",
    "...",
    "Głodny!",
    "Hej!",
    "*mruczy*",
    "Miau?",
    "*ziewa*",
]


class CatBehavior:
    def __init__(self, window: CatWindow, animator: Animator) -> None:
        self._window = window
        self._animator = animator

        # Pobierz rzeczywisty obszar roboczy ekranu (bez paska zadan) przez Win32.
        work_rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(work_rect), 0)
        self._screen_width = work_rect.right - work_rect.left
        self._screen_height = work_rect.bottom - work_rect.top
        self._screen_offset_x = work_rect.left
        self._screen_offset_y = work_rect.top

        # Wykryj dolna krawedz paska zadan bezposrednio przez uchwyt okna.
        ground_y = work_rect.bottom
        try:
            taskbar_hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar_hwnd:
                tb_rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(tb_rect))
                # Stopy kota staja na gorze paska zadan (lub przy dolnej krawedzi ekranu).
                ground_y = min(work_rect.bottom, tb_rect.top)
        except Exception:
            pass
        self._ground_y = ground_y

        self._x = float(
            self._screen_offset_x + random.randint(0, max(0, self._screen_width - 128))
        )
        self._y = self._ground_y - 128
        self._velocity_x = 0.0
        self._state = "idle"
        self._climb_window: dict | None = None
        self._target_y = self._y
        self._state_before_click = self._state
        self._chase_dir = "right"
        self._click_restore_id = 0

        self._movement_timer = QTimer()
        self._movement_timer.timeout.connect(self.update_position)
        self._movement_timer.start(16)

        self._edge_timer = QTimer()
        self._edge_timer.timeout.connect(self._check_window_edge)
        self._edge_timer.start(500)

        self._state_timer = QTimer()
        self._state_timer.setSingleShot(True)
        self._state_timer.timeout.connect(self._random_state_change)

        self._cursor_timer = QTimer()
        self._cursor_timer.timeout.connect(self._check_cursor_proximity)
        self._cursor_timer.start(100)

        self._hidden_by_fullscreen: bool = False

        self._fullscreen_timer = QTimer()
        self._fullscreen_timer.timeout.connect(self._check_fullscreen)
        self._fullscreen_timer.start(2000)

        self._last_hour_reaction: int = -1
        self._state_before_hourly: str = "idle"

        self._hourly_timer = QTimer()
        self._hourly_timer.timeout.connect(self._check_hourly)
        self._hourly_timer.start(30000)

        self._bubble_timer = QTimer()
        self._bubble_timer.setSingleShot(True)
        self._bubble_timer.timeout.connect(self._show_bubble)
        self._bubble_timer.start(random.randint(20000, 40000))

        self._fatigue: float = 0.0

        self._fatigue_timer = QTimer()
        self._fatigue_timer.timeout.connect(self._update_fatigue)
        self._fatigue_timer.start(5000)

        self._food_window = FoodWindow()
        self._food_x: float = 0.0
        self._food_spawn_timer = QTimer()
        self._food_spawn_timer.setSingleShot(True)
        self._food_spawn_timer.timeout.connect(self._spawn_food)
        self._food_spawn_timer.start(random.randint(60000, 120000))

        self._window_sit_timer = QTimer()
        self._window_sit_timer.setSingleShot(True)
        self._window_sit_timer.timeout.connect(self._try_sit_on_window)
        self._window_sit_timer.start(random.randint(90000, 180000))

        self._window.set_on_click(self._on_cat_clicked)
        self._window.move_to(int(self._x), int(self._y))
        self._enter_state("walk_right")
        self._schedule_next_state_change()

    def _enter_state(self, state: str) -> None:
        self._state = state
        self._window.set_rotation(0)

        if state == "walk_right":
            self._velocity_x = 2.0
            self._animator.play("walk_right")
        elif state == "walk_left":
            self._velocity_x = -2.0
            self._animator.play("walk_left")
        elif state == "idle":
            self._velocity_x = 0.0
            self._animator.play("rest_stand")
        elif state == "sit":
            self._velocity_x = 0.0
            self._animator.play("rest_sit")
        elif state == "sleep":
            self._velocity_x = 0.0
            self._animator.play("sleep_4_l")
        elif state == "yawn":
            self._velocity_x = 0.0
            self._animator.play("yawn_sit")
        elif state == "climb_up":
            self._velocity_x = 0.0
            self._animator.play("walk_up")
        elif state == "climb_down":
            self._velocity_x = 0.0
            self._animator.play("walk_down")
        elif state == "walk_right_on_win":
            self._velocity_x = 0.0
            self._animator.play("walk_right")
        elif state == "walk_left_on_win":
            self._velocity_x = 0.0
            self._animator.play("walk_left")
        elif state == "clicked":
            self._velocity_x = 0.0
            self._animator.play("meow_sit")
        elif state == "chase":
            self._velocity_x = 0.0
            self._chase_dir = "right"
            self._animator.play("walk_right")
        elif state == "climb_right_wall":
            self._velocity_x = 0.0
            self._window.set_rotation(90)
            self._animator.play("walk_right")
        elif state == "walk_ceiling_left":
            self._velocity_x = 0.0
            self._window.set_rotation(180)
            self._animator.play("walk_right")
        elif state == "descend_left_wall":
            self._velocity_x = 0.0
            self._window.set_rotation(270)
            self._animator.play("walk_right")
        elif state == "climb_left_wall":
            self._velocity_x = 0.0
            self._window.set_rotation(270)
            self._animator.play("walk_left")
        elif state == "walk_ceiling_right":
            self._velocity_x = 0.0
            self._window.set_rotation(180)
            self._animator.play("walk_left")
        elif state == "descend_right_wall":
            self._velocity_x = 0.0
            self._window.set_rotation(90)
            self._animator.play("walk_left")
        elif state == "attack":
            self._velocity_x = 0.0
            anim = random.choice(["paw_att_right", "paw_att_left"])
            self._animator.play(anim)
            QTimer.singleShot(1000, self._end_attack)
        elif state == "seek_food":
            self._velocity_x = 0.0
            dx = self._food_x - self._x
            if dx >= 0:
                self._chase_dir = "right"
                self._animator.play("walk_right")
            else:
                self._chase_dir = "left"
                self._animator.play("walk_left")
        elif state == "eat_food":
            self._velocity_x = 0.0
            self._animator.play("eat_right")
            QTimer.singleShot(2000, self._end_eat)
        elif state == "on_window_sit":
            self._velocity_x = 0.0
            self._animator.play("rest_sit")
        elif state == "hourly":
            self._velocity_x = 0.0
            self._animator.play("meow_sit")
            QTimer.singleShot(2500, self._end_hourly)
        else:
            raise ValueError(f"Unknown state: {state}")

    def update_position(self) -> None:
        if self._state == "climb_up":
            if self._climb_window is None:
                self._enter_state("walk_right")
            else:
                self._y -= 2
                self._x = self._climb_window["rect"][0] - 64
                if self._y <= self._target_y:
                    self._enter_state("walk_right_on_win")
        elif self._state == "climb_down":
            if self._climb_window is None:
                self._enter_state("walk_right")
            else:
                self._y += 2
                self._x = self._climb_window["rect"][2] - 64
                if self._y >= self._ground_y - 128:
                    self._y = self._ground_y - 128
                    self._climb_window = None
                    self._enter_state("walk_right")
        elif self._state == "walk_right_on_win":
            if self._climb_window is None:
                self._enter_state("walk_right")
            else:
                self._x += 2
                self._y = self._climb_window["rect"][1] - 128
                if self._x > self._climb_window["rect"][2] - 128:
                    self._enter_state("climb_down")
        elif self._state == "walk_left_on_win":
            if self._climb_window is None:
                self._enter_state("walk_left")
            else:
                self._x -= 2
                self._y = self._climb_window["rect"][1] - 128
                if self._x < self._climb_window["rect"][0]:
                    self._enter_state("climb_down")
        elif self._state == "climb_right_wall":
            self._x = float(self._screen_offset_x + self._screen_width - 128)
            self._y -= 2
            if self._y <= self._screen_offset_y:
                self._y = float(self._screen_offset_y)
                self._enter_state("walk_ceiling_left")
        elif self._state == "walk_ceiling_left":
            self._y = float(self._screen_offset_y)
            self._x -= 2
            if self._x <= self._screen_offset_x:
                self._x = float(self._screen_offset_x)
                self._enter_state("descend_left_wall")
        elif self._state == "descend_left_wall":
            self._x = float(self._screen_offset_x)
            self._y += 2
            if self._y >= self._ground_y - 128:
                self._y = float(self._ground_y - 128)
                self._enter_state("walk_right")
        elif self._state == "climb_left_wall":
            self._x = float(self._screen_offset_x)
            self._y -= 2
            if self._y <= self._screen_offset_y:
                self._y = float(self._screen_offset_y)
                self._enter_state("walk_ceiling_right")
        elif self._state == "walk_ceiling_right":
            self._y = float(self._screen_offset_y)
            self._x += 2
            if self._x >= self._screen_offset_x + self._screen_width - 128:
                self._x = float(self._screen_offset_x + self._screen_width - 128)
                self._enter_state("descend_right_wall")
        elif self._state == "descend_right_wall":
            self._x = float(self._screen_offset_x + self._screen_width - 128)
            self._y += 2
            if self._y >= self._ground_y - 128:
                self._y = float(self._ground_y - 128)
                self._enter_state("walk_left")
        elif self._state == "seek_food":
            self._y = self._ground_y - 128
            dx = self._food_x - self._x
            if abs(dx) < 32:
                self._enter_state("eat_food")
            elif dx > 0:
                self._x += 2
                if self._chase_dir != "right":
                    self._chase_dir = "right"
                    self._animator.play("walk_right")
            else:
                self._x -= 2
                if self._chase_dir != "left":
                    self._chase_dir = "left"
                    self._animator.play("walk_left")
        elif self._state == "chase":
            self._y = self._ground_y - 128
            cursor = QCursor.pos()
            dx = cursor.x() - (self._x + 64)
            if dx > 0:
                self._x += 3
                if self._chase_dir == "left":
                    self._chase_dir = "right"
                    self._animator.play("walk_right")
            elif dx < 0:
                self._x -= 3
                if self._chase_dir == "right":
                    self._chase_dir = "left"
                    self._animator.play("walk_left")

            min_x = self._screen_offset_x
            max_x = self._screen_offset_x + self._screen_width - 128
            if self._x < min_x:
                self._x = min_x
            elif self._x > max_x:
                self._x = max_x
        else:
            self._y = self._ground_y - 128
            self._x += self._velocity_x

            min_x = self._screen_offset_x
            max_x = self._screen_offset_x + self._screen_width - 128
            if self._x < min_x:
                self._x = float(min_x)
                if self._state == "walk_left":
                    self._enter_state("climb_left_wall")
                else:
                    self._enter_state("walk_right")
            elif self._x > max_x:
                self._x = float(max_x)
                if self._state == "walk_right":
                    self._enter_state("climb_right_wall")
                else:
                    self._enter_state("walk_left")

        self._window.move_to(int(self._x), int(self._y))

    def _random_state_change(self) -> None:
        if self._state in (
            "climb_up",
            "climb_down",
            "walk_right_on_win",
            "walk_left_on_win",
            "clicked",
            "chase",
            "attack",
            "seek_food",
            "eat_food",
            "on_window_sit",
            "hourly",
            "climb_right_wall",
            "walk_ceiling_left",
            "descend_left_wall",
            "climb_left_wall",
            "walk_ceiling_right",
            "descend_right_wall",
        ):
            self._schedule_next_state_change()
            return

        if self._state in ("walk_right", "walk_left"):
            if self._fatigue > 66:
                next_state = random.choice(["sit", "sit", "sleep", "yawn", "idle"])
            elif self._fatigue < 33:
                next_state = random.choice(
                    ["walk_right", "walk_right", "walk_left", "walk_left", "idle", "attack"]
                )
            else:
                next_state = random.choice(
                    ["walk_right", "walk_left", "idle", "sit", "yawn", "attack"]
                )
        elif self._state in ("idle", "sit"):
            if self._fatigue > 66:
                next_state = random.choice(["sleep", "sleep", "sit"])
            elif self._fatigue < 33:
                next_state = random.choice(
                    ["walk_right", "walk_left", "walk_right", "walk_left"]
                )
            else:
                next_state = random.choice(["walk_right", "walk_left", "sleep"])
        elif self._state == "sleep":
            next_state = "idle"
        elif self._state == "yawn":
            next_state = "sit"
        else:
            next_state = "idle"

        self._enter_state(next_state)
        self._schedule_next_state_change()

    def _schedule_next_state_change(self) -> None:
        self._state_timer.start(random.randint(3000, 8000))

    def _end_attack(self) -> None:
        if self._state == "attack":
            self._enter_state("idle")

    def _end_hourly(self) -> None:
        if self._state == "hourly":
            self._enter_state(self._state_before_hourly)

    def _check_window_edge(self) -> None:
        if self._state not in ("walk_right", "walk_left"):
            return

        window = find_window_edge_at(int(self._x), self._y, cat_w=128)
        if window is None:
            return

        self._climb_window = window
        self._target_y = window["rect"][1]
        self._enter_state("climb_up")

    def _on_cat_clicked(self) -> None:
        if self._state in (
            "climb_up",
            "climb_down",
            "walk_right_on_win",
            "walk_left_on_win",
            "climb_right_wall",
            "walk_ceiling_left",
            "descend_left_wall",
            "climb_left_wall",
            "walk_ceiling_right",
            "descend_right_wall",
            "attack",
        ):
            return

        self._state_before_click = self._state
        self._click_restore_id += 1
        current_restore_id = self._click_restore_id
        self._enter_state("clicked")

        def _restore_state() -> None:
            if current_restore_id != self._click_restore_id:
                return
            if self._state == "clicked":
                self._enter_state(self._state_before_click)

        QTimer.singleShot(1500, _restore_state)

    def _check_cursor_proximity(self) -> None:
        cursor = QCursor.pos()
        cat_center_x = self._x + 64
        cat_center_y = self._y + 64
        dist = math.sqrt((cursor.x() - cat_center_x) ** 2 + (cursor.y() - cat_center_y) ** 2)

        if dist < 150 and self._state in ("walk_right", "walk_left"):
            self._enter_state("chase")
        elif dist >= 150 and self._state == "chase":
            self._enter_state("walk_right")

    def _is_fullscreen_active(self) -> bool:
        _SKIP_CLASSES = {"Progman", "WorkerW", "Shell_TrayWnd", "DV2ControlHost"}
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd:
                return False
            if hwnd == int(self._window.winId()):
                return False
            if hwnd == int(self._food_window.winId()):
                return False
            buf = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, buf, 256)
            if buf.value in _SKIP_CLASSES:
                return False
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            screen_w = ctypes.windll.user32.GetSystemMetrics(0)
            screen_h = ctypes.windll.user32.GetSystemMetrics(1)
            return (
                rect.left <= 0
                and rect.top <= 0
                and rect.right >= screen_w
                and rect.bottom >= screen_h
            )
        except Exception:
            return False

    def _check_fullscreen(self) -> None:
        if self._is_fullscreen_active():
            if self._window.isVisible():
                self._hidden_by_fullscreen = True
                self._window.hide()
        else:
            if self._hidden_by_fullscreen:
                self._hidden_by_fullscreen = False
                self._window.show()

    def _check_hourly(self) -> None:
        from datetime import datetime
        now = datetime.now()
        if now.minute != 0:
            return
        if now.hour == self._last_hour_reaction:
            return
        self._last_hour_reaction = now.hour
        if self._state in (
            "climb_up", "climb_down", "walk_right_on_win", "walk_left_on_win",
            "clicked", "hourly",
            "climb_right_wall", "walk_ceiling_left", "descend_left_wall",
            "climb_left_wall", "walk_ceiling_right", "descend_right_wall",
        ):
            return
        self._state_before_hourly = self._state
        self._enter_state("hourly")

    def _show_bubble(self) -> None:
        if self._state in ("walk_right", "walk_left", "idle", "sit", "sleep"):
            text = random.choice(_BUBBLE_TEXTS)
            self._window.set_bubble(text)
            QTimer.singleShot(3000, self._hide_bubble)
        self._bubble_timer.start(random.randint(20000, 40000))

    def _hide_bubble(self) -> None:
        self._window.set_bubble(None)

    def _update_fatigue(self) -> None:
        if self._state in ("walk_right", "walk_left"):
            self._fatigue = min(100.0, self._fatigue + 3.0)
        elif self._state == "chase":
            self._fatigue = min(100.0, self._fatigue + 5.0)
        elif self._state == "sleep":
            self._fatigue = max(0.0, self._fatigue - 8.0)
        elif self._state in ("idle", "sit", "yawn"):
            self._fatigue = max(0.0, self._fatigue - 3.0)

    def _spawn_food(self) -> None:
        if self._state not in ("walk_right", "walk_left", "idle", "sit", "sleep"):
            self._food_spawn_timer.start(random.randint(60000, 120000))
            return
        self._food_x = float(random.randint(
            self._screen_offset_x + 48,
            self._screen_offset_x + self._screen_width - 48
        ))
        self._food_window.show_at(int(self._food_x), self._ground_y - 48)
        self._enter_state("seek_food")

    def _end_eat(self) -> None:
        if self._state == "eat_food":
            self._food_window.hide()
            self._fatigue = max(0.0, self._fatigue - 30.0)
            self._food_spawn_timer.start(random.randint(60000, 120000))
            self._enter_state("idle")

    def _try_sit_on_window(self) -> None:
        from src.win_detector import get_windows
        candidates = [
            w for w in get_windows()
            if self._screen_offset_y + 100 < w["rect"][1] < self._ground_y - 200
            and w["rect"][2] - w["rect"][0] > 200
        ]
        if candidates and self._state in ("walk_right", "walk_left", "idle", "sit"):
            win = random.choice(candidates)
            left, top, right, _ = win["rect"]
            self._x = float(left + (right - left) // 2 - 64)
            self._y = float(top - 128)
            self._enter_state("on_window_sit")
            QTimer.singleShot(random.randint(8000, 15000), self._leave_window_sit)
        self._window_sit_timer.start(random.randint(90000, 180000))

    def _leave_window_sit(self) -> None:
        if self._state == "on_window_sit":
            self._y = float(self._ground_y - 128)
            self._enter_state("idle")

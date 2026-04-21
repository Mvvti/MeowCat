# Task 18 — Wspinaczka po krawędziach ekranu

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Okno kota (CatWindow) ma metodę set_rotation(degrees) dodaną w task_17.
Kot chodzi po dolnej krawędzi ekranu. Chcemy, żeby zamiast odbijać od lewej/prawej
krawędzi ekranu, wspinał się po boku, szedł po suficie i schodził z powrotem.

ZADANIE:
Rozszerz src/behavior.py o 6 nowych stanów wspinaczki po krawędziach ekranu.

PLIK DO MODYFIKACJI:
- src/behavior.py

WYMAGANIA:

--- 1. Na początku metody _enter_state, zaraz po linii self._state = state, dodaj: ---

    self._window.set_rotation(0)

(Resetuje rotację przy każdej zmianie stanu; stany ścienne ją nadpiszą.)

--- 2. Dodaj 6 nowych stanów w _enter_state (przed linią `else: raise ValueError`): ---

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
            self._window.set_rotation(90)
            self._animator.play("walk_left")
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
            self._window.set_rotation(270)
            self._animator.play("walk_right")

--- 3. Dodaj 6 nowych bloków w update_position (przed blokiem `elif self._state == "chase"`): ---

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

--- 4. W bloku `else` w update_position zmień warunki odbicia od krawędzi ekranu: ---

Znajdź:
            if self._x < min_x:
                self._x = min_x
                self._enter_state("walk_right")
            elif self._x > max_x:
                self._x = max_x
                self._enter_state("walk_left")

Zmień na:
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

--- 5. W _random_state_change rozszerz listę stanów do zignorowania: ---

Znajdź:
        if self._state in (
            "climb_up",
            "climb_down",
            "walk_right_on_win",
            "walk_left_on_win",
            "clicked",
            "chase",
        ):

Zmień na:
        if self._state in (
            "climb_up",
            "climb_down",
            "walk_right_on_win",
            "walk_left_on_win",
            "clicked",
            "chase",
            "climb_right_wall",
            "walk_ceiling_left",
            "descend_left_wall",
            "climb_left_wall",
            "walk_ceiling_right",
            "descend_right_wall",
        ):

--- 6. W _on_cat_clicked rozszerz listę stanów do zignorowania: ---

Znajdź:
        if self._state in ("climb_up", "climb_down", "walk_right_on_win", "walk_left_on_win"):
            return

Zmień na:
        if self._state in (
            "climb_up", "climb_down", "walk_right_on_win", "walk_left_on_win",
            "climb_right_wall", "walk_ceiling_left", "descend_left_wall",
            "climb_left_wall", "walk_ceiling_right", "descend_right_wall",
        ):
            return

CZEGO NIE RUSZAĆ:
- src/window.py — nie modyfikować
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Logika stanów climb_up/climb_down/walk_on_win — nie modyfikować
- Logika chase i _check_cursor_proximity — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot chodzi po dolnej krawędzi. Gdy dotrze do prawej krawędzi ekranu,
wspina się w górę po prawej ścianie (sprite obrócony 90°), przechodzi po suficie w lewo
(sprite 180°), schodzi po lewej ścianie (sprite 90°) i wraca do chodzenia w prawo.
Analogicznie od lewej strony. python -m py_compile src/behavior.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: 6 nowych stanów, rotacje, logika ruchu, listy ignorowanych stanów — wszystko zgodnie z taskiem. Kompilacja ok.

# Task 07 — Interakcja z myszą

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–6 są ukończone.

Gotowe moduły:
- src/sprite_sheet.py  — load_sprite_sheet(path), get_frames(anim_name)
- src/window.py        — CatWindow z set_frame(pil_image), move_to(x, y)
- src/animator.py      — Animator(fps, on_frame), play(anim_name), stop()
- src/win_detector.py  — get_windows(), find_window_edge_at(cat_x, cat_y)
- src/behavior.py      — CatBehavior — ruch, stany, wspinaczka po oknach
- main.py              — QApplication + CatWindow + Animator + CatBehavior

ZADANIE:
Rozszerz CatWindow i CatBehavior o dwie formy interakcji z myszą:
1. Kliknięcie lewym przyciskiem na kota → kot reaguje (animacja "meow_sit") a następnie wraca do poprzedniego stanu
2. Gonienie kursora → gdy kursor jest blisko kota, kot biegnie w jego kierunku

PLIKI DO MODYFIKACJI:
- src/window.py   — dodaj obsługę kliknięcia myszy
- src/behavior.py — dodaj stany "clicked" i "chase"

WYMAGANIA — src/window.py:

Dodaj do CatWindow:
- Sygnał kliknięcia: użyj Callable (nie Qt Signal) — przechowaj
  self._on_click: Callable[[], None] | None = None
- Metoda set_on_click(callback: Callable[[], None]) -> None:
    ustawia self._on_click = callback
- Nadpisz mousePressEvent(self, event: QMouseEvent):
    jeśli event.button() == Qt.MouseButton.LeftButton i self._on_click nie jest None:
        wywołaj self._on_click()

WYMAGANIA — src/behavior.py:

1. Dodaj 2 nowe stany:
   "clicked" — kot reaguje na kliknięcie (animacja "meow_sit"), velocity_x = 0
   "chase"   — kot goni kursor (animacja zależna od kierunku: walk_right/walk_left)

2. W __init__ po stworzeniu timers:
   - wywołaj window.set_on_click(self._on_cat_clicked)
   - dodaj timer kursora: QTimer co 100 ms → _check_cursor_proximity()

3. Metoda _on_cat_clicked(self) -> None:
   - jeśli aktualny stan to stan wspinaczki (climb_up/down/walk_*_on_win) — ignoruj
   - zapamiętaj self._state_before_click = self._state
   - wejdź w stan "clicked"
   - po 1500 ms (QTimer.singleShot) wróć do self._state_before_click

4. Metoda _check_cursor_proximity(self) -> None:
   - pobierz pozycję kursora: QCursor.pos() z PyQt6.QtGui
   - oblicz odległość kursora od środka kota:
       cat_center_x = self._x + 32
       cat_center_y = self._y + 32
       dist = sqrt((cursor.x() - cat_center_x)**2 + (cursor.y() - cat_center_y)**2)
   - jeśli dist < 150 i stan to "walk_right" lub "walk_left":
       wejdź w stan "chase"
   - jeśli dist >= 150 i stan to "chase":
       wejdź w stan "walk_right"

5. W stanie "chase" update_position():
   - oblicz kierunek do kursora:
       cursor = QCursor.pos()
       dx = cursor.x() - (self._x + 32)
   - jeśli dx > 0: self._x += 3, jeśli aktualny kierunek był lewy → animator.play("walk_right")
   - jeśli dx < 0: self._x -= 3, jeśli aktualny kierunek był prawy → animator.play("walk_left")
   - zapamiętaj kierunek w self._chase_dir ("right"/"left") żeby nie resetować animacji co tick
   - ogranicz x do [0, screen_width - 64]

6. _enter_state obsłuż nowe stany:
   "clicked" -> animacja "meow_sit", velocity_x = 0
   "chase"   -> animacja "walk_right" (domyślnie), velocity_x = 0,
                zainicjuj self._chase_dir = "right"

7. _random_state_change: ignoruj jeśli stan to "clicked" lub "chase"
   (dodaj je do listy stanów blokowanych obok stanów wspinaczki)

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
- Kliknięcie na kota → kot mówi "meow" (animacja meow_sit przez ~1.5s) i wraca do poprzedniego stanu.
- Zbliżenie kursora do kota na < 150 px → kot zaczyna gonić kursor.
- Odsunięcie kursora → kot wraca do chodzenia.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: window.py z callbackiem kliknięcia, super().mousePressEvent zachowany. behavior.py: stany clicked/chase, _click_restore_id (debounce kliknięć), chase z lazy animation switch, _check_cursor_proximity z math.sqrt.

# Task 06 — Detekcja okien i wspinaczka

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–5 są ukończone.

Gotowe moduły:
- src/sprite_sheet.py — load_sprite_sheet(path), get_frames(anim_name)
- src/window.py       — CatWindow z set_frame(pil_image), move_to(x, y)
- src/animator.py     — Animator(fps, on_frame), play(anim_name), stop()
- src/behavior.py     — CatBehavior — kot chodzi po dole ekranu, stany: walk/idle/sit/sleep/yawn
- main.py             — QApplication + CatWindow + Animator + CatBehavior

ZADANIE:
Stwórz moduł src/win_detector.py do wykrywania otwartych okien przez pywin32.
Następnie rozszerz CatBehavior o logikę wspinaczki po krawędziach wykrytych okien.

PLIKI DO STWORZENIA / MODYFIKACJI:
- src/win_detector.py — nowy moduł
- src/behavior.py     — dodaj stany wspinaczki i integrację z win_detector

WYMAGANIA — src/win_detector.py:

1. Funkcja get_windows() -> list[dict]:
   - używa win32gui.EnumWindows() do enumeracji okien
   - dla każdego okna sprawdza: IsWindowVisible, GetWindowText (niepusty tytuł),
     GetWindowRect
   - pomija okna z zerową powierzchnią (width=0 lub height=0)
   - pomija okno naszego kota (po tytule — CatWindow nie ustawia tytułu, więc
     jego tytuł to pusty string — jest już pomijane)
   - zwraca listę słowników: {"hwnd": int, "title": str, "rect": (left, top, right, bottom)}

2. Funkcja find_window_edge_at(cat_x: int, cat_y: int, cat_w: int = 64) -> dict | None:
   - sprawdza czy kot (prostokąt cat_x, cat_y, cat_x+cat_w, cat_y+64) stoi
     na górnej krawędzi jakiegoś okna (w tolerancji ±10 px)
   - jeśli tak — zwraca słownik okna, inaczej None

WYMAGANIA — src/behavior.py (rozszerzenie):

Dodaj 4 nowe stany:
   "climb_up"    — kot wspina się w górę po lewej krawędzi okna (+animacja "walk_up")
   "climb_down"  — kot schodzi w dół po prawej krawędzi okna (+animacja "walk_down")
   "walk_right_on_win" — kot chodzi w prawo po górnej krawędzi okna (animacja "walk_right")
   "walk_left_on_win"  — kot chodzi w lewo  po górnej krawędzi okna (animacja "walk_left")

Logika wspinaczki:
- Co 500 ms sprawdzaj (osobny QTimer) czy pod kotem jest krawędź okna
  przez find_window_edge_at(int(self._x), self._y)
- Jeśli wykryto krawędź i aktualny stan to "walk_right" lub "walk_left":
    - wejdź w stan "climb_up" (wspinanie po lewej krawędzi wykrytego okna)
    - zapamiętaj self._climb_window = wykryte okno
    - self._target_y = wykryte_okno["rect"][1]  (top okna — cel wspinaczki)
- W update_position() obsłuż nowe stany:
    "climb_up":
        - self._y -= 2
        - self._x = self._climb_window["rect"][0] - 32  (lewa krawędź okna)
        - jeśli self._y <= self._target_y: wejdź w "walk_right_on_win"
    "climb_down":
        - self._y += 2
        - self._x = self._climb_window["rect"][2] - 32  (prawa krawędź okna)
        - jeśli self._y >= screen_height - 80: wejdź w "walk_right"
    "walk_right_on_win":
        - self._x += 2
        - self._y = self._climb_window["rect"][1] - 64  (siedzi na górze okna)
        - jeśli self._x > self._climb_window["rect"][2] - 64: wejdź w "climb_down"
    "walk_left_on_win":
        - self._x -= 2
        - self._y = self._climb_window["rect"][1] - 64
        - jeśli self._x < self._climb_window["rect"][0]: wejdź w "climb_down"

- _enter_state obsłuż nowe stany:
    "climb_up"          -> animacja "walk_up",    velocity_x = 0
    "climb_down"        -> animacja "walk_down",  velocity_x = 0
    "walk_right_on_win" -> animacja "walk_right", velocity_x = 0
    "walk_left_on_win"  -> animacja "walk_left",  velocity_x = 0

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po `python main.py` kot chodzi po dole ekranu jak dotąd. Gdy napotka krawędź
otwartego okna (np. Eksploratora plików), wspina się po jego lewej krawędzi
na górę, chodzi po górnej belce okna, a następnie schodzi po prawej krawędzi
z powrotem na pulpit.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: win_detector z best-match delta, behavior rozszerzony o 4 stany wspinaczki, guardy na None, _random_state_change nie przerywa wspinaczki, reset _y do ground w stanach naziemnych.

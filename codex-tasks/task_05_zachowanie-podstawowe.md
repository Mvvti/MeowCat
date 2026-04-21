# Task 05 — Zachowanie podstawowe

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–4 są ukończone.

Gotowe moduły:
- src/sprite_sheet.py — load_sprite_sheet(path), get_frames(anim_name)
- src/window.py       — CatWindow z set_frame(pil_image), move_to(x, y)
- src/animator.py     — Animator(fps, on_frame), play(anim_name), stop()
- main.py             — QApplication + CatWindow + Animator, odtwarza "walk_right"

ZADANIE:
Stwórz moduł src/behavior.py z klasą CatBehavior, która steruje logiką zachowań
kota — porusza nim po dolnej krawędzi ekranu i losowo przełącza stany.

PLIKI DO STWORZENIA / MODYFIKACJI:
- src/behavior.py — nowy moduł z klasą CatBehavior
- main.py          — zastąp bezpośrednie play("walk_right") przez CatBehavior

WYMAGANIA:

1. Klasa CatBehavior:
   def __init__(self, window: CatWindow, animator: Animator) -> None
     - przechowuje referencje do window i animator
     - pobiera rozmiary ekranu przez QScreen (QApplication.primaryScreen().geometry())
     - ustawia startową pozycję kota: x losowy na szerokości ekranu, y = screen_height - 80
     - uruchamia wewnętrzny QTimer (interval 16 ms ≈ 60 FPS) do update_position()
     - uruchamia wewnętrzny QTimer (interval losowy 3000–8000 ms) do zmiany stanu
     - wywołuje _enter_state("walk_right") na starcie

2. Stany kota (self._state: str):
   "walk_right"  — kot idzie w prawo (prędkość +2 px/tick), animacja "walk_right"
   "walk_left"   — kot idzie w lewo  (prędkość -2 px/tick), animacja "walk_left"
   "idle"        — kot stoi, animacja "rest_stand"
   "sit"         — kot siedzi, animacja "rest_sit"
   "sleep"       — kot śpi, animacja "sleep_4_l"
   "yawn"        — kot ziewa (jednorazowo), animacja "yawn_sit"

3. Metoda _enter_state(state: str) -> None:
   - ustawia self._state
   - ustawia self._velocity_x (dla walk: ±2, dla reszty: 0)
   - wywołuje animator.play(odpowiednia_animacja)

4. Metoda update_position() — wywoływana co 16 ms:
   - przesuwa kota: self._x += self._velocity_x
   - odbicie od krawędzi ekranu: jeśli x < 0 → x=0, zmień stan na "walk_right";
     jeśli x > screen_width - 64 → x=screen_width-64, zmień stan na "walk_left"
   - wywołuje window.move_to(int(self._x), self._y)

5. Metoda _random_state_change() — wywoływana co losowy czas:
   - jeśli aktualny stan to "walk_right" lub "walk_left": losowo wybierz nowy stan
     spośród ["walk_right", "walk_left", "idle", "sit", "yawn"]
   - jeśli aktualny stan to "idle" lub "sit": losowo wybierz spośród
     ["walk_right", "walk_left", "sleep"]
   - jeśli aktualny stan to "sleep": zmień na "idle"
   - jeśli aktualny stan to "yawn": zmień na "sit"
   - po zmianie stanu ustaw nowy losowy timer 3000–8000 ms

6. Losowy czas timera stanu:
   - użyj: random.randint(3000, 8000)
   - timer stanu powinien być single-shot (QTimer.singleShot lub setSingleShot(True))

7. W main.py:
   - usuń bezpośrednie wywołanie animator.play("walk_right")
   - usuń ręczne frames = get_frames("rest_sit") i window.set_frame(frames[0])
   - stwórz behavior = CatBehavior(window=window, animator=animator)
   - zastąp TODO dla pętli zachowań tym kodem

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/__init__.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- TODO komentarz dla tray w main.py — zostawić

OCZEKIWANY WYNIK:
Po `python main.py` kot pojawia się na dolnej krawędzi ekranu i:
- chodzi w lewo/prawo, odbija się od krawędzi
- co kilka sekund losowo: siada, ziewa, zasypia lub zmienia kierunek
- okno pozostaje przezroczyste i zawsze na wierzchu
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: CatBehavior z timers 16ms/single-shot, _enter_state z mapą animacji, update_position z odbiciem od krawędzi, _random_state_change z poprawnymi przejściami. Bonus: _schedule_next_state_change jako osobna metoda, ValueError dla nieznanego stanu.

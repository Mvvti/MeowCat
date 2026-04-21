# Task 04 — System animacji

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–3 są ukończone.

Gotowe moduły:
- src/sprite_sheet.py — load_sprite_sheet(path), get_frames(anim_name) -> list[PIL.Image]
- src/window.py — CatWindow.set_frame(pil_image), CatWindow.move_to(x, y)
- main.py — tworzy QApplication, CatWindow, ładuje sprite sheet, pokazuje okno

ZADANIE:
Stwórz moduł src/animator.py z klasą Animator, która:
- przechowuje listę klatek bieżącej animacji
- odtwarza je w pętli (loopowanie) z zadanym FPS
- przy każdym ticku wywołuje callback z bieżącą klatką (PIL.Image)
- używa QTimer z PyQt6 do taktowania (nie wątki)
- pozwala zmienić animację w trakcie działania (play(anim_name))

PLIKI DO STWORZENIA / MODYFIKACJI:
- src/animator.py — nowy moduł z klasą Animator
- main.py          — zastąp TODO dla pętli zachowań: uruchom Animator z animacją "walk_right"

WYMAGANIA:
- Klasa Animator:
    def __init__(self, fps: int, on_frame: Callable[[Image.Image], None]) -> None
      - fps: liczba klatek na sekundę (domyślnie 8)
      - on_frame: callback wywoływany przy każdej nowej klatce
    def play(self, anim_name: str) -> None
      - pobiera klatki przez get_frames(anim_name) z src.sprite_sheet
      - resetuje indeks klatki do 0
      - uruchamia (lub restartuje) QTimer z interwałem 1000 // fps ms
    def stop(self) -> None
      - zatrzymuje QTimer
    def _tick(self) -> None  (slot QTimer)
      - pobiera bieżącą klatkę (self._frames[self._index])
      - wywołuje on_frame(klatka)
      - inkrementuje self._index, z zawinięciem do 0 (modulo len(frames))
- QTimer musi być podłączony do slotu _tick przez timer.timeout.connect(self._tick)
- W main.py:
    - stwórz animator = Animator(fps=8, on_frame=window.set_frame)
    - wywołaj animator.play("walk_right")
    - zastąp TODO dla pętli zachowań tym kodem

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/__init__.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- TODO komentarz dla tray w main.py — zostawić

OCZEKIWANY WYNIK:
Po `python main.py` na ekranie w pozycji (100, 800) kot animuje się w pętli
— chodzi w prawo (animacja "walk_right", 6 klatek, 8 FPS). Okno pozostaje
przezroczyste i zawsze na wierzchu.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Animator z QTimer, play/stop/_tick, modulo loopowanie. Defensywne guardy na pustą listę klatek. main.py odtwarza walk_right w 8 FPS. TODO dla tray zachowane.

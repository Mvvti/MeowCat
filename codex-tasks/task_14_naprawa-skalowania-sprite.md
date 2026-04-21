# Task 14 — Naprawa skalowania sprite'a z paczki 2D

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Kot używa teraz sprite'ów z folderu "cat animation/64x64/2d" (pliki walk.png, idle.png itd.).
Każdy plik to poziomy pasek klatek 64x64px na klatkę.

Aktualny problem:
Funkcja _load_strip w src/sprite_sheet.py używa _normalize_frame, która tylko skaluje
całą ramkę 64x64 → 128x128 bez wyrównania do dołu.
Efekt: faktyczna zawartość kota (bbox ~35x35px) siedzi w środku ramki — kot "unosi się"
zamiast stać na ziemi. Stopy kota są na y=96 zamiast y=128 okna.
Gotowa funkcja _fit_to_canvas (już w pliku) robi to poprawnie: przycina do bbox,
skaluje do 128x128 i wyrównuje do dołu.

ZADANIE:
Dwie zmiany:
1. W src/sprite_sheet.py: w funkcji _load_strip zamień _normalize_frame na _fit_to_canvas.
2. W src/behavior.py: w metodzie __init__ usuń margines -15 (był kompensatą złego wyrównania).

PLIKI DO MODYFIKACJI:
- src/sprite_sheet.py — jedna linia w _load_strip
- src/behavior.py — jedna linia w __init__

WYMAGANIA:

W src/sprite_sheet.py znajdź w funkcji _load_strip linię:
    frames.append(_normalize_frame(frame))
Zmień na:
    frames.append(_fit_to_canvas(frame))

W src/behavior.py znajdź w metodzie __init__ linię:
    self._y = self._ground_y - 128 - 15
Zmień na:
    self._y = self._ground_y - 128

CZEGO NIE RUSZAĆ:
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Definicja funkcji _fit_to_canvas — nie modyfikować
- Definicja funkcji _normalize_frame — nie modyfikować (może być używana gdzie indziej)
- Wszystkie linie self._y = self._ground_y - 128 w update_position() — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot stoi na ziemi (stopy wyrównane do dolnej krawędzi okna),
widoczny w całości nad paskiem zadań.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: _load_strip zmieniony na _fit_to_canvas. Efekt uboczny: kot za duży (128px). Naprawione w task_15.

# Task 13 — Margines od dołu ekranu

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.

Aktualny stan:
- Stopy kota są na y=1078, a pasek zadań zaczyna się również na y=1078
- Dolna krawędź ekranu (1080px) za blisko — dolne piksele kota są niewidoczne
- Pasek zadań (auto-ukryty, 2px widocznego paska) zasłania stopy kota

ZADANIE:
Jednolinijkowa zmiana w src/behavior.py — dodaj 15px margines od dołu,
żeby kot stał pewnie nad paskiem zadań.

PLIK DO MODYFIKACJI:
- src/behavior.py

WYMAGANIA:

Znajdź linię (w __init__):
    self._y = self._ground_y - 128

Zmień ją na:
    self._y = self._ground_y - 128 - 15

Sprawdź czy w pliku jest jeszcze linia inicjalizacji _y i czy należy też ją zmienić.
NIE zmieniaj linii resetu _y w update_position() (self._y = self._ground_y - 128)
— tam pozostaw bez marginesu, bo ground_y już jest powyżej taskbara.

Uwaga: zmień TYLKO linię inicjalizacji w __init__, nie resetów w update_position.

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Kot pojawia się 15px wyżej niż poprzednio — stopy w całości widoczne ponad
paskiem zadań, żaden piksel kota nie jest ucięty.
```

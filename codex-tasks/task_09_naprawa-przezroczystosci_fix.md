# Task 09 FIX — Przezroczystość + pozycjonowanie kota

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.

Aktualny stan:
- Białe tło okna jest w większości usunięte (widać pulpit przez okno) ✅
- Ale kot jest widoczny tylko jako fragment — jest częściowo ucięty przez pasek zadań
  lub krawędź ekranu ❌
- Okno kota ma rozmiar 64x64 px, sprite kota zajmuje ok. 21% tej przestrzeni
  (reszta to przezroczyste piksele) — to normalne i oczekiwane dla pixel art 16x16 → 4x scale

DWA PROBLEMY DO NAPRAWIENIA:

PROBLEM 1 — Pozycjonowanie (behavior.py):
Funkcja QApplication.primaryScreen().geometry() zwraca pełną rozdzielczość ekranu
WŁĄCZNIE z paskiem zadań. Kot jest pozycjonowany na y = screen_height - 80, co
sprawia że częściowo chowa się pod paskiem zadań.

PROBLEM 2 — Przezroczystość (window.py):
Przepisz CatWindow z QWidget na QLabel dla lepszej obsługi przezroczystości na Windows 11.

PLIKI DO MODYFIKACJI:
- src/behavior.py  — naprawa pozycjonowania
- src/window.py    — przepisanie na QLabel

WYMAGANIA — src/behavior.py:

Zmień pobieranie rozmiaru ekranu w __init__:
  PRZED: geometry = QApplication.primaryScreen().geometry()
  PO:    geometry = QApplication.primaryScreen().availableGeometry()

availableGeometry() zwraca obszar ekranu BEZ paska zadań.
Zmień też pozycję startową y:
  PRZED: self._y = self._screen_height - 80
  PO:    self._y = self._screen_height - 64

Zmień też reset _y w update_position() (linia "self._y = self._screen_height - 80"):
  PO: self._y = self._screen_height - 64

WYMAGANIA — src/window.py:

Przepisz CatWindow z QWidget na QLabel:
- class CatWindow(QLabel) zamiast class CatWindow(QWidget)
- Dodaj import QLabel z PyQt6.QtWidgets
- W __init__:
    - Zachowaj te same flagi okna (FramelessWindowHint, WindowStaysOnTopHint, Tool)
    - Zachowaj WA_TranslucentBackground
    - Dodaj: self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    - Dodaj: self.setStyleSheet("background: transparent;")
    - Dodaj: self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    - Zachowaj setFixedSize(64, 64)
- Metoda set_frame(pil_image):
    - Konwersja PIL→QPixmap (bez zmian)
    - Wywołaj self.setPixmap(self._pixmap) zamiast self.update()
- Usuń paintEvent całkowicie (QLabel sam obsługuje rysowanie pixmapy)
- Zachowaj showEvent z _apply_win32_fixes (ctypes DWM fixes)
- Zachowaj move_to(), set_on_click(), mousePressEvent() bez zmian

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py:
- Kot pojawia się w całości nad paskiem zadań przy dolnej krawędzi ekranu
- Widoczny jest tylko sprite kota — bez białego tła, bez prostokąta
- Kot chodzi w lewo/prawo wzdłuż dolnej krawędzi ekranu
```

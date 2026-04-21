# Task 10 — Skala kota i poprawka pozycjonowania

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.

Aktualny stan:
- Przezroczystość działa ✅
- Kot jest za mały: 64x64px = zaledwie 3.3% szerokości ekranu 1920x1080 ❌
- availableGeometry() nie wykrywa paska zadań (zwraca pełne 1080px) ❌
- Kot jest częściowo schowany pod paskiem zadań ❌

DWA ZADANIA:

ZADANIE 1 — Powiększ kota do 128x128px (src/sprite_sheet.py + src/window.py)

W src/sprite_sheet.py:
  Zmień: SCALE = 4  →  SCALE = 8
  Zmień: SCALED_SIZE = (FRAME_SIZE * SCALE, FRAME_SIZE * SCALE)  (już tak jest, bez zmian)
  Efekt: klatki będą 128x128px zamiast 64x64px

W src/window.py:
  Zmień: self.setFixedSize(64, 64)  →  self.setFixedSize(128, 128)
  Zmień w set_frame(): qimage = QImage(data, 64, 64, ...)  →  QImage(data, 128, 128, ...)

ZADANIE 2 — Popraw pozycjonowanie kota (src/behavior.py)

Pobieranie dostępnego obszaru ekranu (bez paska zadań) przez Win32 API:
Dodaj na górze pliku:
  import ctypes
  import ctypes.wintypes

W __init__ zastąp pobieranie geometry tym kodem:
  # Pobierz rzeczywisty obszar roboczy ekranu (bez paska zadań) przez Win32
  work_rect = ctypes.wintypes.RECT()
  ctypes.windll.user32.SystemParametersInfoW(48, 0, ctypes.byref(work_rect), 0)
  self._screen_width = work_rect.right - work_rect.left
  self._screen_height = work_rect.bottom - work_rect.top
  self._screen_offset_x = work_rect.left
  self._screen_offset_y = work_rect.top

Gdzie 48 = SPI_GETWORKAREA — zwraca prostokąt ekranu BEZ paska zadań.

Zmień pozycję startową y i rozmiar kota:
  self._x = float(random.randint(0, max(0, self._screen_width - 128)))
  self._y = self._screen_height - 128

Zaktualizuj wszystkie miejsca gdzie było 64 (rozmiar okna kota) na 128:
- max_x = self._screen_width - 128  (w update_position)
- if self._x > self._screen_width - 128  (w update_position)
- self._y = self._screen_height - 128  (wszystkie resety _y)
- cat_center_x = self._x + 64  (środek kota — był 32, teraz 64)
- cat_center_y = self._y + 64  (środek kota — był 32, teraz 64)
- find_window_edge_at(int(self._x), self._y, cat_w=128)  (szerokość kota)
- self._y = self._climb_window["rect"][1] - 128  (pozycja nad oknem)
- self._x = self._climb_window["rect"][2] - 64   (prawa krawędź — był 32)
- self._x > self._climb_window["rect"][2] - 128  (warunek walk_right_on_win)

CZEGO NIE RUSZAĆ:
- src/win_detector.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py:
- Kot jest wyraźnie widoczny na pulpicie (128x128px = ok. 6.7% szerokości ekranu)
- Kot chodzi tuż nad paskiem zadań, nie pod nim
- Przezroczystość bez zmian (działa)
```

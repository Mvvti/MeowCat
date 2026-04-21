# Task 12 — Poprawka pozycji kota nad paskiem zadań

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.

Aktualny stan:
- Przezroczystość działa ✅
- Sprite wycentrowany w klatce ✅
- Ale dolna część kota (nogi) jest ukryta pod paskiem zadań ❌
  SPI_GETWORKAREA zwraca bottom=1080 (pełna wysokość ekranu) bo pasek zadań
  jest ustawiony jako auto-ukrywany lub nakładający się — więc metoda z task_10
  nie działa na tym systemie

ZADANIE:
Zmodyfikuj src/behavior.py — wykryj pasek zadań bezpośrednio przez jego uchwyt okna
(FindWindow "Shell_TrayWnd") i ustaw kota nad nim.

PLIK DO MODYFIKACJI:
- src/behavior.py

WYMAGANIA:

W metodzie __init__, po obliczeniu work_rect (SPI_GETWORKAREA),
ZASTĄP obliczenie self._y tym kodem:

    # Wykryj dolną krawędź paska zadań bezpośrednio przez uchwyt okna
    ground_y = work_rect.bottom  # domyślnie: dół obszaru roboczego
    try:
        taskbar_hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
        if taskbar_hwnd:
            tb_rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(taskbar_hwnd, ctypes.byref(tb_rect))
            # Stopy kota stają na górze paska zadań (lub przy dolnej krawędzi ekranu)
            ground_y = min(work_rect.bottom, tb_rect.top)
    except Exception:
        pass
    self._ground_y = ground_y
    self._y = ground_y - 128  # okno: stopy kota = ground_y, głowa = ground_y - 128

Zapisz self._ground_y = ground_y jako atrybut instancji.

Zaktualizuj WSZYSTKIE miejsca w pliku gdzie wcześniej było:
    self._screen_height - 128
lub:
    self._screen_height - 80
na:
    self._ground_y - 128

Czyli wszędzie gdzie kot ma być "na ziemi" (nie podczas wspinaczki),
użyj self._ground_y - 128 zamiast self._screen_height - 128.

Dotyczy to w szczególności:
- self._y = ... (inicjalizacja pozycji)
- self._y = self._screen_height - 128 (resety w update_position)
- self._y >= self._screen_height - 128 (warunek w climb_down)

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot stoi w całości nad paskiem zadań — wszystkie 4 łapy
i cała sylwetka widoczna. Chodzi wzdłuż dolnej krawędzi ekranu tuż
ponad paskiem zadań.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: FindWindowW("Shell_TrayWnd") wykryło pasek (top=1078, auto-ukryty). ground_y=1078, okno kota y=950, kot widoczny y=1014-1078. Wszystkie resety _y i warunki climb_down zaktualizowane.

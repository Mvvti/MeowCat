# Task 16 — Kot na pulpicie (za oknami)

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Aktualnie okno kota ma flagę WindowStaysOnTopHint — jest zawsze nad innymi oknami.
Chcemy odwrotnego zachowania: kot ma być widoczny tylko na pulpicie, za wszystkimi oknami.

ZADANIE:
Zmodyfikuj src/window.py tak, żeby okno kota było zawsze na dole stosu okien (za innymi
oknami), ale nadal reagowało na kliknięcia myszą.

PLIK DO MODYFIKACJI:
- src/window.py

WYMAGANIA:

1. Usuń WindowStaysOnTopHint z flag okna w __init__:
   Stara linia (do usunięcia z listy flag):
       Qt.WindowType.WindowStaysOnTopHint |

2. Dodaj metodę _send_to_bottom w klasie CatWindow:

    def _send_to_bottom(self) -> None:
        try:
            hwnd = int(self.winId())
            HWND_BOTTOM = 1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_BOTTOM, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
            )
        except Exception:
            pass

3. W metodzie showEvent, po wywołaniu self._apply_win32_fixes(), dodaj:
       self._send_to_bottom()

4. Dodaj w __init__ timer wywołujący _send_to_bottom co 1000ms (żeby okno
   wracało za inne okna po każdej interakcji):
       self._bottom_timer = QTimer(self)
       self._bottom_timer.timeout.connect(self._send_to_bottom)
       self._bottom_timer.start(1000)

5. W _apply_win32_fixes dodaj WS_EX_NOACTIVATE do extended styles, żeby kliknięcie
   w kota nie przenosiło fokusa na okno kota:
   Po linii:
       ex = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
   Zmień:
       ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED)
   Na:
       WS_EX_NOACTIVATE = 0x08000000
       ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED | WS_EX_NOACTIVATE)

CZEGO NIE RUSZAĆ:
- src/behavior.py — nie modyfikować
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Reszta logiki window.py (set_frame, move_to, mousePressEvent itd.) — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot pojawia się na pulpicie za wszystkimi oknami.
Gdy otworzymy dowolne okno — zasłoni kota. Kliknięcie w kota nadal działa
(meow/chase), ale nie przenosi fokusa na okno kota.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: WindowStaysOnTopHint usunięty, HWND_BOTTOM + WS_EX_NOACTIVATE + timer 1000ms dodane. Kompilacja ok.

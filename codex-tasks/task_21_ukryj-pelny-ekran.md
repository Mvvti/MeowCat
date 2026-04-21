# Task 21 — Ukryj kota przy pełnym ekranie

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Chcemy, żeby kot automatycznie się chował gdy jakakolwiek aplikacja przejdzie w tryb
pełnoekranowy, i wracał gdy pełny ekran zniknie. Ukrycie z trayu (przez użytkownika)
nie powinno być nadpisywane — kot wraca tylko jeśli to my go schowaliśmy.

ZADANIE:
Dodaj do src/behavior.py detekcję pełnego ekranu i automatyczne ukrywanie/pokazywanie
okna kota.

PLIK DO MODYFIKACJI:
- src/behavior.py

WYMAGANIA:

--- 1. W __init__ dodaj atrybut i timer (np. po _cursor_timer): ---

        self._hidden_by_fullscreen: bool = False

        self._fullscreen_timer = QTimer()
        self._fullscreen_timer.timeout.connect(self._check_fullscreen)
        self._fullscreen_timer.start(2000)

--- 2. Dodaj metodę _is_fullscreen_active (np. po _check_cursor_proximity): ---

    def _is_fullscreen_active(self) -> bool:
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd:
                return False
            if hwnd == int(self._window.winId()):
                return False
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            screen_w = ctypes.windll.user32.GetSystemMetrics(0)
            screen_h = ctypes.windll.user32.GetSystemMetrics(1)
            return (
                rect.left <= 0
                and rect.top <= 0
                and rect.right >= screen_w
                and rect.bottom >= screen_h
            )
        except Exception:
            return False

--- 3. Dodaj metodę _check_fullscreen (np. po _is_fullscreen_active): ---

    def _check_fullscreen(self) -> None:
        if self._is_fullscreen_active():
            if self._window.isVisible():
                self._hidden_by_fullscreen = True
                self._window.hide()
        else:
            if self._hidden_by_fullscreen:
                self._hidden_by_fullscreen = False
                self._window.show()

CZEGO NIE RUSZAĆ:
- src/window.py — nie modyfikować
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Pozostała logika behavior.py — nie modyfikować

OCZEKIWANY WYNIK:
Gdy jakakolwiek aplikacja przejdzie w tryb pełnoekranowy — kot znika.
Gdy pełny ekran się wyłączy — kot wraca. Jeśli użytkownik ręcznie ukrył kota
przez tray, pełny ekran nie przywraca go z powrotem.
python -m py_compile src/behavior.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: _hidden_by_fullscreen, timer 2000ms, _is_fullscreen_active (GetForegroundWindow + GetSystemMetrics), _check_fullscreen z flagą. Kompilacja ok.

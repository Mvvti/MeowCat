# Task 08 — Tray icon i menu kontekstowe

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–7 są ukończone.

Gotowe moduły:
- src/sprite_sheet.py  — load_sprite_sheet(path), get_frames(anim_name)
- src/window.py        — CatWindow (frameless, transparent, always-on-top, kliknięcie)
- src/animator.py      — Animator(fps, on_frame)
- src/win_detector.py  — get_windows(), find_window_edge_at()
- src/behavior.py      — CatBehavior (ruch, stany, wspinaczka, interakcja z myszą)
- main.py              — QApplication + CatWindow + Animator + CatBehavior

ZADANIE:
Stwórz moduł src/tray.py z klasą CatTray — ikonę w zasobniku systemowym z menu
kontekstowym. Następnie podepnij ją do main.py.

PLIKI DO STWORZENIA / MODYFIKACJI:
- src/tray.py — nowy moduł
- main.py     — zastąp TODO dla tray przez CatTray

WYMAGANIA — src/tray.py:

1. Klasa CatTray:
   def __init__(self, app: QApplication, window: CatWindow) -> None

2. Ikona tray:
   - użyj QSystemTrayIcon z PyQt6.QtWidgets
   - jako ikonę użyj pierwszej klatki animacji "rest_sit" ze sprite sheeta
     (pobierz przez get_frames("rest_sit")[0], przekonwertuj PIL→QIcon tak samo
     jak w CatWindow: PIL→QImage→QPixmap→QIcon)
   - jeśli ikona nie jest dostępna (wyjątek) — użyj pustego QIcon()
   - wywołaj tray.show() żeby ikona była widoczna

3. Menu kontekstowe (QMenu):
   - akcja "Pokaż / ukryj kota":
       przełącza window.show() / window.hide()
       aktualizuje tekst akcji odpowiednio
   - separator
   - akcja "Zamknij":
       wywołuje app.quit()

4. Podpięcie menu:
   - tray.setContextMenu(menu)

5. Podwójne kliknięcie na ikonę tray:
   - tray.activated.connect(...)
   - przy QSystemTrayIcon.ActivationReason.DoubleClick:
       wywołaj akcję pokaż/ukryj (taką samą logikę jak akcja menu)

WYMAGANIA — main.py:
- zaimportuj CatTray z src.tray
- stwórz tray = CatTray(app=app, window=window)
- zastąp TODO komentarz dla tray tym kodem

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/behavior.py — nie modyfikować
- src/__init__.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po `python main.py`:
- w zasobniku systemowym pojawia się ikona kota
- prawy klik → menu z "Pokaż / ukryj kota" i "Zamknij"
- "Zamknij" kończy aplikację
- "Pokaż / ukryj kota" oraz podwójny klik na ikonę przełączają widoczność kota
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: CatTray z dynamicznym tekstem akcji (Ukryj/Pokaż), fallback QIcon(), double-click obsłużony. main.py czysty bez TODO. Projekt kompletny.

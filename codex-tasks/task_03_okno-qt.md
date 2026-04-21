# Task 03 — Okno Qt (przezroczyste, bez ramki, always-on-top)

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etapy 1–2 są ukończone.

Gotowe moduły:
- main.py — szkielet QApplication z TODO komentarzami
- src/sprite_sheet.py — load_sprite_sheet(path) + get_frames(anim_name)
  Klatki to obiekty PIL.Image w trybie RGBA, rozmiar 64x64 px.

ZADANIE:
Stwórz moduł src/window.py z klasą CatWindow — okno PyQt6 które:
- jest przezroczyste (brak tła, widać przez nie pulpit)
- nie ma ramki ani paska tytułu
- jest zawsze na wierzchu wszystkich okien
- wyświetla jedną klatkę kota (PIL.Image RGBA 64x64) w bieżącej pozycji
- pozwala ustawić pozycję okna (x, y) na ekranie
- pozwala zmienić wyświetlaną klatkę przez metodę set_frame(image: PIL.Image)

Następnie podepnij CatWindow do main.py — stwórz instancję, załaduj sprite sheet,
wyświetl pierwszą klatkę animacji "rest_sit" w pozycji (100, 800) i pokaż okno.

PLIKI DO MODYFIKACJI / STWORZENIA:
- src/window.py — nowy moduł z klasą CatWindow
- main.py       — podpięcie CatWindow (zastąp TODO dla okna)

WYMAGANIA:
- CatWindow dziedziczy po QWidget
- Flagi okna (setWindowFlags):
    Qt.WindowType.FramelessWindowHint
    Qt.WindowType.WindowStaysOnTopHint
    Qt.WindowType.Tool           ← ukrywa z taskbara
- setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
- Rozmiar okna: zawsze 64x64 px (setFixedSize(64, 64))
- Metoda set_frame(pil_image: Image.Image):
    - konwertuje PIL.Image (RGBA) na QPixmap
    - zapamiętuje jako self._pixmap
    - wywołuje self.update() aby przerysować
- Metoda move_to(x: int, y: int): ustawia pozycję okna przez self.move(x, y)
- paintEvent: rysuje self._pixmap przez QPainter (jeśli nie None)
- Konwersja PIL→QPixmap:
    data = pil_image.tobytes("raw", "RGBA")
    qimage = QImage(data, 64, 64, QImage.Format.Format_RGBA8888)
    self._pixmap = QPixmap.fromImage(qimage)
- W main.py:
    - załaduj sprite sheet: load_sprite_sheet("cat animation/cat 1.6.png")
    - pobierz frames = get_frames("rest_sit")
    - stwórz window = CatWindow()
    - wywołaj window.set_frame(frames[0])
    - wywołaj window.move_to(100, 800)
    - wywołaj window.show()
    - zastąp TODO dla okna tym kodem

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/__init__.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- TODO komentarze dla tray i zachowań w main.py — zostawić

OCZEKIWANY WYNIK:
Po `python main.py` na ekranie w pozycji (100, 800) pojawia się kot (pierwsza
klatka animacji "rest_sit", 64x64 px) bez żadnego okna dookoła — tylko
pikselowy kot bezpośrednio na pulpicie, zawsze na wierzchu.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: CatWindow poprawnie implementuje wszystkie flagi, WA_TranslucentBackground, set_frame z konwersją PIL→QPixmap, move_to, paintEvent z QPainter. main.py ładuje sprite sheet i wyświetla pierwszą klatkę rest_sit w (100, 800). TODO dla tray i zachowań zachowane.

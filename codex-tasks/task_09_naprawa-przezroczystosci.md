# Task 09 — Naprawa przezroczystości okna

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Projekt działa, ale okno kota wyświetla
białe tło zamiast pełnej przezroczystości. Kot (21% klatki 64x64 to pixele kota,
reszta przezroczysta w pliku) pojawia się jako mała figurka na białym prostokącie
zamiast bezpośrednio na pulpicie.

DIAGNOZA:
- Sprite sheet ma poprawny kanał alpha (tło = alpha 0) — problem NIE jest po stronie grafiki
- WA_TranslucentBackground jest ustawiony, ale na Windows 11 DWM renderuje własne
  białe tło za oknem Qt, co sprawia że okno wygląda na białe
- CompositionMode_Clear w paintEvent nie pomógł
- ctypes DwmExtendFrameIntoClientArea i DwmSetWindowAttribute (zaokrąglenia) nie
  pomogły wystarczająco

ZADANIE:
Przepisz src/window.py tak, żeby okno CatWindow było w 100% przezroczyste na
Windows 11 — widoczny ma być TYLKO kot, bez żadnego białego tła.

Wypróbuj podejście oparte na QLabel zamiast QWidget:

PLIKI DO MODYFIKACJI:
- src/window.py — przepisz CatWindow

WYMAGANIA:

Podejście 1 (preferowane) — QLabel:
- Zmień bazę klasy z QWidget na QLabel
- Usuń niestandardowy paintEvent całkowicie
- W set_frame() wywołuj self.setPixmap(pixmap) zamiast self.update()
- Dodaj self.setStyleSheet("background: transparent;") w __init__
- Dodaj self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
- Zachowaj te same flagi okna:
    Qt.WindowType.FramelessWindowHint
    Qt.WindowType.WindowStaysOnTopHint
    Qt.WindowType.Tool
- Zachowaj WA_TranslucentBackground
- Zachowaj setFixedSize(64, 64)
- Zachowaj metody: move_to(), set_on_click(), mousePressEvent()
- W showEvent zastosuj Windows DWM fixes przez ctypes (zostaw istniejący kod
  z _apply_win32_fixes — wyłącz zaokrąglenia i usuń cień)

Jeśli podejście 1 nie zadziała — w tym samym pliku dodaj komentarz i wypróbuj
Podejście 2 — QWidget z setStyleSheet:
- Zostań przy QWidget
- Dodaj self.setStyleSheet("background: transparent;") w __init__
- Usuń CompositionMode_Clear, zostaw samo drawPixmap w paintEvent

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/behavior.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py na pulpicie widoczny jest KOT bezpośrednio na tle pulpitu —
bez żadnego białego prostokąta, bez żadnego tła. Tylko pikselowy kot chodzący
po dolnej krawędzi ekranu.
```

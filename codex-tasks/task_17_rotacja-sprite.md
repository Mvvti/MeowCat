# Task 17 — Rotacja sprite'a w oknie

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Kot będzie się wspinał po krawędziach ekranu — do tego potrzebna jest możliwość
obracania sprite'a (0°/90°/180°/270°) w zależności od tego, na której ścianie się znajduje.

ZADANIE:
Dodaj do klasy CatWindow w src/window.py obsługę rotacji sprite'a.

PLIK DO MODYFIKACJI:
- src/window.py

WYMAGANIA:

1. W __init__ dodaj atrybut przechowujący aktualny kąt obrotu:
       self._rotation: int = 0

2. Dodaj metodę set_rotation:
       def set_rotation(self, degrees: int) -> None:
           self._rotation = degrees % 360

3. W metodzie set_frame, przed konwersją PIL image do QImage, zastosuj rotację:
   Jeśli self._rotation != 0, obróć obraz używając PIL:
       from PIL.Image import Transpose
       _TRANSPOSE_MAP = {
           90:  Transpose.ROTATE_90,
           180: Transpose.ROTATE_180,
           270: Transpose.ROTATE_270,
       }
       if self._rotation in _TRANSPOSE_MAP:
           pil_image = pil_image.transpose(_TRANSPOSE_MAP[self._rotation])

   Słownik _TRANSPOSE_MAP zdefiniuj jako stałą modułową (na poziomie modułu,
   nie wewnątrz metody), żeby nie tworzyć go przy każdym wywołaniu set_frame.

CZEGO NIE RUSZAĆ:
- src/behavior.py — nie modyfikować
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Reszta logiki window.py — nie modyfikować

OCZEKIWANY WYNIK:
Klasa CatWindow ma metodę set_rotation(degrees). Wywołanie set_rotation(90)
przed kolejną klatką animacji spowoduje, że sprite zostanie obrócony o 90° CCW.
python -m py_compile src/window.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: _TRANSPOSE_MAP na poziomie modułu, set_rotation + rotacja w set_frame. Kompilacja ok.

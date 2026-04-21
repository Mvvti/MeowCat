# Task 20 — Cień pod kotem

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Okno kota to przezroczyste 128x128px QLabel. Kot ma stopy wyrównane do dolnej krawędzi
ramki (y=128). Chcemy dodać subtelny owalny cień pod stopami kota widoczny gdy stoi
na ziemi (rotation=0). Gdy kot jest na ścianie lub suficie (rotation != 0) — cień
nie powinien być widoczny.

ZADANIE:
Zmodyfikuj metodę set_frame w src/window.py — przed wyświetleniem klatki dorysuj
półprzezroczysty owalny cień na dole obrazu, ale tylko gdy self._rotation == 0.

PLIK DO MODYFIKACJI:
- src/window.py

WYMAGANIA:

1. Dodaj import ImageDraw z PIL na początku pliku (obok istniejącego `from PIL import Image`):
       from PIL import Image, ImageDraw

2. W metodzie set_frame, NA POCZĄTKU (przed sprawdzeniem rotacji), dodaj logikę cienia:

    def set_frame(self, pil_image: Image.Image) -> None:
        if self._rotation == 0:
            pil_image = pil_image.copy()
            draw = ImageDraw.Draw(pil_image)
            cx = 64
            draw.ellipse(
                [cx - 28, 120, cx + 28, 130],
                fill=(0, 0, 0, 80),
            )
        if self._rotation in _TRANSPOSE_MAP:
            ...  # reszta bez zmian

   Uwaga: elipsa jest narysowana przy y=120–130, co odpowiada stopom kota
   (bottom-aligned). Część elipsy (y=128–130) wychodzi poza ramkę i jest
   automatycznie przycinana przez PIL — to prawidłowe zachowanie.

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
Pod kotem chodzącym po ziemi widoczny jest subtelny owalny cień.
Gdy kot wspina się po ścianie lub suficie — cień znika.
python -m py_compile src/window.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: ImageDraw dodany, elipsa (36,120,92,130) fill=(0,0,0,80) przed rotacją. Kompilacja ok.

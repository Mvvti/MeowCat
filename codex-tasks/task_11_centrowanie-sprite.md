# Task 11 — Centrowanie sprite'a w klatce

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Przezroczystość działa.

DIAGNOZA PROBLEMU:
Sprite'y kota są zapisane w arkuszu z przezroczystym "paddingiem" wokół figury.
Przykładowe bounding boxy oryginalnych klatek 16x16:
  walk_right frame 0: (6, 8, 16, 16) — kot w prawym-dolnym rogu
  rest_sit   frame 0: (9, 0, 16, 9)  — kot w prawym-górnym rogu
  walk_left  frame 0: (7, 0, 16, 6)  — kot w prawym-górnym rogu

Oznacza to, że po skalowaniu do 128x128, kot siedzi w ROGU okna,
a nie na środku. Użytkownik widzi tylko fragment kota przy krawędzi.

ZADANIE:
Zmodyfikuj src/sprite_sheet.py — po skalowaniu każdej klatki wycentruj
zawartość (piksele kota) poziomo i wyrównaj ją do DOŁU w obrębie klatki.

PLIK DO MODYFIKACJI:
- src/sprite_sheet.py

WYMAGANIA:

W funkcji load_sprite_sheet(), po linii:
    frame = frame.resize(SCALED_SIZE, Image.NEAREST)

Dodaj centrowanie/wyrównanie:
    bbox = frame.getbbox()
    if bbox:
        content = frame.crop(bbox)
        canvas = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
        # Wyśrodkuj poziomo
        paste_x = (SCALED_SIZE[0] - content.width) // 2
        # Wyrównaj do dołu (stopy kota zawsze przy dolnej krawędzi)
        paste_y = SCALED_SIZE[1] - content.height
        canvas.paste(content, (paste_x, paste_y))
        frame = canvas

CZEGO NIE RUSZAĆ:
- src/window.py    — nie modyfikować
- src/behavior.py  — nie modyfikować
- src/animator.py  — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/__init__.py  — nie modyfikować
- main.py          — nie modyfikować
- folder "cat animation/" — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot jest wycentrowany w swojej przezroczystej klatce —
widoczny na środku, z "stopami" przy dolnej krawędzi okna.
Efekt: kot wygląda jakby stał/chodził bezpośrednio na pulpicie lub na
górze okna, a nie siedział w rogu.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Centrowanie poziome + wyrównanie do dołu działa. walk_right: bbox(24,64,104,128), rest_sit: bbox(36,56,92,128) — kot wycentrowany, stopy przy y=128.

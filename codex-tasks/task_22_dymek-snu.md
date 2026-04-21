# Task 22 — Dymek snu (Zzz nad kotem)

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Chcemy, żeby gdy kot śpi, nad jego głową pojawiały się unoszące się literki "Zzz"
rysowane bezpośrednio na klatce PIL — klasyczny efekt snu.

ZADANIE:
Dodaj dymek snu do src/window.py oraz podepnij go w src/behavior.py.

PLIKI DO MODYFIKACJI:
- src/window.py
- src/behavior.py

WYMAGANIA:

--- src/window.py ---

1. W __init__ dodaj atrybut (np. po self._rotation):

        self._show_zzz: bool = False

2. Dodaj metodę (np. po set_rotation):

    def set_zzz(self, visible: bool) -> None:
        self._show_zzz = visible

3. W metodzie set_frame, NA KOŃCU bloku "if self._rotation == 0:" (po canvas.paste),
   tuż przed "if self._rotation in _TRANSPOSE_MAP:", dodaj rysowanie Zzz:

        if self._show_zzz:
            from PIL import ImageFont
            draw2 = ImageDraw.Draw(pil_image)
            try:
                font_s = ImageFont.load_default(size=9)
                font_m = ImageFont.load_default(size=12)
                font_l = ImageFont.load_default(size=16)
            except TypeError:
                font_s = font_m = font_l = ImageFont.load_default()
            draw2.text((70, 55), "z", font=font_s, fill=(160, 160, 255, 180))
            draw2.text((76, 42), "z", font=font_m, fill=(180, 180, 255, 210))
            draw2.text((83, 26), "Z", font=font_l, fill=(200, 200, 255, 240))

   Zzz rysujemy na pil_image (już po naklejeniu kota na canvas z cieniem),
   tylko gdy rotation == 0 (kot leży na ziemi).

--- src/behavior.py ---

4. Na początku metody _enter_state, jako pierwsza linia po "self._state = state":

        self._window.set_zzz(False)

5. W gałęzi elif state == "sleep": po self._animator.play(...) dodaj:

        self._window.set_zzz(True)

CZEGO NIE RUSZAĆ:
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Pozostała logika behavior.py i window.py — nie modyfikować

OCZEKIWANY WYNIK:
Gdy kot wejdzie w stan "sleep" — nad jego głową pojawia się "z z Z" (małe rosnące
litery w kolorze jasnoniebieskawym). Gdy stan się zmieni — dymek znika.
Zzz widoczne tylko gdy rotation == 0 (kot na podłodze).
python -m py_compile src/window.py && python -m py_compile src/behavior.py — bez błędów.
```

---
## STATUS
- Wykonany: —
- Wynik: —
- Uwagi: —

# Task 20 fix — Cień rysowany pod kotem (nie na wierzchu)

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
W task_20 dodano cień jako elipsę rysowaną bezpośrednio na obrazie kota — przez co
cień zasłania stopy kota. Trzeba odwrócić kolejność: cień rysowany na pustym płótnie,
kot przyklejany NA WIERZCH.

ZADANIE:
Zmień logikę rysowania cienia w metodzie set_frame w src/window.py.

PLIK DO MODYFIKACJI:
- src/window.py

WYMAGANIA:

Znajdź w set_frame blok:
        if self._rotation == 0:
            pil_image = pil_image.copy()
            draw = ImageDraw.Draw(pil_image)
            cx = 64
            draw.ellipse(
                [cx - 28, 120, cx + 28, 130],
                fill=(0, 0, 0, 80),
            )

Zastąp go:
        if self._rotation == 0:
            canvas = Image.new("RGBA", pil_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(canvas)
            cx = 64
            draw.ellipse(
                [cx - 28, 120, cx + 28, 130],
                fill=(0, 0, 0, 80),
            )
            canvas.paste(pil_image, (0, 0), pil_image)
            pil_image = canvas

Różnica: cień trafia na puste przezroczyste płótno, potem kot jest przyklejany
na wierzch z użyciem własnej maski alpha — stopy kota nie są zasłaniane.

CZEGO NIE RUSZAĆ:
- Pozostała logika set_frame (rotacja, konwersja QImage) — nie modyfikować
- Reszta window.py — nie modyfikować
- Żadne inne pliki — nie modyfikować

OCZEKIWANY WYNIK:
Cień widoczny pod kotem, stopy kota nie są zasłonięte.
python -m py_compile src/window.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Cień na osobnym canvas, kot nakładany na wierzch przez paste z maską alpha. Kompilacja ok.

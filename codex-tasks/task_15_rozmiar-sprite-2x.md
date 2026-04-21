# Task 15 — Poprawka rozmiaru sprite'a (2× zamiast fit)

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Sprite'y ładowane z folderu "cat animation/64x64/2d" — klatki 64x64px.

Aktualny stan po task_14:
_load_strip używa _fit_to_canvas, która skaluje zawartość kota do pełnych 128x128px.
Efekt: kot jest za duży.

ZADANIE:
Dodaj nową funkcję _normalize_and_align w src/sprite_sheet.py i użyj jej w _load_strip.
Funkcja ma skalować klatkę 2× (64→128px) i wyrównywać zawartość do dołu — bez
rozciągania kota do pełnych 128px.

PLIKI DO MODYFIKACJI:
- src/sprite_sheet.py

WYMAGANIA:

Dodaj nową funkcję _normalize_and_align bezpośrednio po definicji _normalize_frame:

    def _normalize_and_align(frame: Image.Image) -> Image.Image:
        scaled = frame.resize(SCALED_SIZE, Image.NEAREST)
        bbox = scaled.getbbox()
        if not bbox:
            return scaled
        content = scaled.crop(bbox)
        canvas = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
        paste_x = (SCALED_SIZE[0] - content.width) // 2
        paste_y = SCALED_SIZE[1] - content.height
        canvas.paste(content, (paste_x, paste_y))
        return canvas

W funkcji _load_strip zamień:
    frames.append(_fit_to_canvas(frame))
Na:
    frames.append(_normalize_and_align(frame))

CZEGO NIE RUSZAĆ:
- src/behavior.py — nie modyfikować
- src/window.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Funkcje _fit_to_canvas, _normalize_frame — nie modyfikować

OCZEKIWANY WYNIK:
Po python main.py kot ma rozmiar ~70px (2× oryginał 35px), stoi na ziemi,
widoczny w całości.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Dodano _normalize_and_align, _load_strip używa jej zamiast _fit_to_canvas. Kompilacja ok.

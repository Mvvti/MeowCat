# Task 01 — Inicjalizacja projektu

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot widoczny
bezpośrednio na pulpicie, bez okna aplikacji, z przezroczystym tłem, zawsze na wierzchu.
Styl: Shimeji / Desktop Goose. Stack: PyQt6, pywin32, Pillow.

ZADANIE:
Stwórz szkielet projektu: plik requirements.txt z zależnościami oraz main.py
jako punkt wejścia aplikacji (tylko szkielet — bez logiki).

PLIKI DO STWORZENIA:
- requirements.txt       — lista zależności pip
- main.py                — punkt wejścia, importuje moduły z src/, uruchamia aplikację
- src/__init__.py        — pusty plik (oznaczenie pakietu)

WYMAGANIA:
- requirements.txt musi zawierać: PyQt6, pywin32, Pillow
- main.py musi:
  - importować QApplication z PyQt6.QtWidgets
  - tworzyć instancję QApplication
  - zawierać komentarze TODO wskazujące gdzie podpiąć: okno, tray, pętlę zachowań
  - wywoływać sys.exit(app.exec())
- src/__init__.py może być pusty
- Żadnej dodatkowej logiki — sam szkielet

CZEGO NIE RUSZAĆ:
- folder "cat animation/" — nie modyfikować, nie przenosić
- folder "workflow/" — nie modyfikować

OCZEKIWANY WYNIK:
Po wykonaniu `pip install -r requirements.txt` oraz `python main.py` aplikacja
uruchamia się i natychmiast kończy (brak okna) — bez błędów importu.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Wszystkie pliki zgodne z wymaganiami. main.py poprawnie importuje QApplication, tworzy instancję, ma TODO dla okna/tray/zachowań, wywołuje sys.exit(app.exec()).

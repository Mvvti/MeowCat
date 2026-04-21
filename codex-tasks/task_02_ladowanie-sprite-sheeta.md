# Task 02 — Ładowanie sprite sheeta

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow. Etap 1 (szkielet projektu) jest ukończony.
Sprite sheet to plik PNG z klatkami 16x16 px, ułożonymi w rzędach poziomych.
Dostępne są 3 warianty kolorystyczne kota w folderze "cat animation/":
  - "cat 1.png"   — czarny kot
  - "cat 1.6.png" — rudy kot
  - "cat 1.9.png" — biały kot

Na podstawie pliku "cat animation/cat 16x16 with text.png" (sprite sheet z etykietami)
zidentyfikowano następujące animacje i ich rozmieszczenie w arkuszu (wiersze od góry, 0-based):

REST (wiersze 0–3):
  Row 0: "rest_stand"    — 8 klatek (stanie, oddychanie)
  Row 1: "rest_sit"      — 8 klatek (siedzenie)
  Row 2: "rest_lie"      — 5 klatek (leżenie)
  Row 3: "rest_special"  — 10 klatek (rozciąganie/specjalne)

WALK (wiersze 4–11):
  Row 4:  "walk_down"       — 4 klatki
  Row 5:  "walk_up"         — 4 klatki
  Row 6:  "walk_right"      — 6 klatek
  Row 7:  "walk_left"       — 6 klatek
  Row 8:  "walk_left_d"     — 5 klatek (skośnie lewo-dół)
  Row 9:  "walk_right_d"    — 5 klatek (skośnie prawo-dół)
  Row 10: "walk_right_up"   — 5 klatek (skośnie prawo-góra)
  Row 11: "walk_left_up"    — 5 klatek (skośnie lewo-góra)

SLEEP (wiersze 12–19):
  Row 12: "sleep_1_l" — 2 klatki
  Row 13: "sleep_1_r" — 2 klatki
  Row 14: "sleep_2_l" — 2 klatki
  Row 15: "sleep_2_r" — 2 klatki
  Row 16: "sleep_3_l" — 2 klatki
  Row 17: "sleep_3_r" — 2 klatki
  Row 18: "sleep_4_l" — 2 klatki (poziome leżenie)
  Row 19: "sleep_4_r" — 2 klatki

EAT (wiersze 20–27):
  Row 20: "eat_down"     — 7 klatek
  Row 21: "eat_up"       — 7 klatek
  Row 22: "eat_left"     — 6 klatek
  Row 23: "eat_right"    — 6 klatek
  Row 24: "eat_right_d"  — 6 klatek
  Row 25: "eat_left_d"   — 6 klatek
  Row 26: "eat_right_up" — 6 klatek
  Row 27: "eat_left_up"  — 6 klatek

MEOW (wiersze 28–31):
  Row 28: "meow_sit"    — 3 klatki
  Row 29: "meow_stand"  — 2 klatki
  Row 30: "meow_sit2"   — 2 klatki
  Row 31: "meow_lie"    — 3 klatki

YAWN (wiersze 32–35):
  Row 32: "yawn_sit"    — 6 klatek
  Row 33: "yawn_stand"  — 6 klatek
  Row 34: "yawn_sit2"   — 6 klatek
  Row 35: "yawn_lie"    — 5 klatek

WASH (wiersze 36–38):
  Row 36: "wash_sit"   — 6 klatek
  Row 37: "wash_stand" — 5 klatek
  Row 38: "wash_lie"   — 5 klatek

SCRATCH (wiersze 39–40):
  Row 39: "scratch_l"  — 8 klatek
  Row 40: "scratch_r"  — 8 klatek

HISS (wiersze 41–42):
  Row 41: "hiss_l"  — 2 klatki
  Row 42: "hiss_r"  — 2 klatki

DEAD (wiersz 43):
  Row 43: "dead"    — 1 klatka

PAW ATTACK (wiersze 44–51):
  Row 44: "paw_att_down"     — 7 klatek
  Row 45: "paw_att_up"       — 7 klatek
  Row 46: "paw_att_left"     — 5 klatek
  Row 47: "paw_att_right"    — 5 klatek
  Row 48: "paw_att_right_d"  — 6 klatek
  Row 49: "paw_att_left_d"   — 6 klatek
  Row 50: "paw_att_right_up" — 5 klatek
  Row 51: "paw_att_left_up"  — 5 klatek

ON HIND LEGS (wiersz 52):
  Row 52: "hind_legs" — 2 klatki

ZADANIE:
Stwórz moduł src/sprite_sheet.py, który:
1. Wczytuje wybrany plik PNG sprite sheeta (np. "cat animation/cat 1.6.png")
2. Parsuje klatki 16x16 z każdego wiersza zgodnie z mapą animacji podaną wyżej
3. Zwraca słownik {nazwa_animacji: [lista obiektów PIL.Image]}
4. Skaluje każdą klatkę do rozmiaru 64x64 px (scale x4, nearest neighbor)
5. Udostępnia funkcję get_frames(anim_name) -> list[PIL.Image]

PLIKI DO STWORZENIA / MODYFIKACJI:
- src/sprite_sheet.py — moduł parsujący sprite sheet

WYMAGANIA:
- Klasa lub moduł z funkcją: load_sprite_sheet(path: str) -> dict[str, list[Image]]
- Funkcja get_frames(anim_name: str) -> list[Image] (rzuca KeyError jeśli brak animacji)
- Skalowanie: PIL Image.resize((64, 64), Image.NEAREST)
- Klatki wycinane przez: image.crop((col*16, row*16, col*16+16, row*16+16))
- Obsługa tła: klatki mają przezroczyste tło (tryb RGBA) — zachować kanał alpha
- Mapa animacji zakodowana jako stała ANIMATION_MAP = {nazwa: (row, num_frames)}
  w tym samym pliku
- Prosty skrypt testowy na dole pliku (if __name__ == "__main__") — wczytuje
  "cat animation/cat 1.6.png" i printuje nazwy animacji + liczbę klatek

CZEGO NIE RUSZAĆ:
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować zawartości
- src/__init__.py — nie modyfikować

OCZEKIWANY WYNIK:
python src/sprite_sheet.py uruchamia się bez błędów i wypisuje listę animacji
z liczbą klatek, np.:
  rest_stand: 8 frames
  walk_right: 6 frames
  sleep_1_l: 2 frames
  ...
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: ANIMATION_MAP kompletna (53 animacje, wiersze 0–52). load_sprite_sheet poprawnie konwertuje do RGBA, wycina klatki 16x16, skaluje do 64x64 nearest neighbor, cache w module. get_frames rzuca KeyError. Blok testowy używa Path do relative path. Składniowo poprawny.
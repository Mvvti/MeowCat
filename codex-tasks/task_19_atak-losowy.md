# Task 19 — Losowa animacja ataku

```
KONTEKST:
Budujemy desktopową aplikację w Pythonie (tylko Windows 11) — animowany kot na pulpicie,
styl Shimeji. Stack: PyQt6, pywin32, Pillow.
Sprite'y ładowane z "cat animation/64x64/2d". Animacja ataku (paw_att_right / paw_att_left)
jest już załadowana w sprite_sheet.py, ale nigdy nie jest wywoływana.
Chcemy, żeby kot losowo wykonywał animację ataku — tak jak sit/sleep/yawn.

ZADANIE:
Dodaj stan "attack" do src/behavior.py. Stan ma być wybierany losowo podczas chodzenia,
trwać ~1 sekundę i automatycznie wracać do idle.

PLIK DO MODYFIKACJI:
- src/behavior.py

WYMAGANIA:

--- 1. Dodaj nowy stan w _enter_state (przed linią `else: raise ValueError`): ---

        elif state == "attack":
            self._velocity_x = 0.0
            anim = random.choice(["paw_att_right", "paw_att_left"])
            self._animator.play(anim)
            QTimer.singleShot(1000, self._end_attack)

--- 2. Dodaj nową metodę _end_attack (np. po metodzie _schedule_next_state_change): ---

    def _end_attack(self) -> None:
        if self._state == "attack":
            self._enter_state("idle")

--- 3. W _random_state_change dodaj "attack" do możliwych przejść z chodzenia: ---

Znajdź:
        if self._state in ("walk_right", "walk_left"):
            next_state = random.choice(["walk_right", "walk_left", "idle", "sit", "yawn"])

Zmień na:
        if self._state in ("walk_right", "walk_left"):
            next_state = random.choice(["walk_right", "walk_left", "idle", "sit", "yawn", "attack"])

--- 4. W _random_state_change dodaj "attack" do listy stanów ignorowanych: ---

Znajdź linię z "chase" w liście ignorowanych stanów i dodaj "attack" obok:
            "chase",
            "attack",

--- 5. W _on_cat_clicked dodaj "attack" do listy stanów ignorowanych: ---

Znajdź:
            "climb_right_wall", "walk_ceiling_left", "descend_left_wall",
            "climb_left_wall", "walk_ceiling_right", "descend_right_wall",

Zmień na:
            "climb_right_wall", "walk_ceiling_left", "descend_left_wall",
            "climb_left_wall", "walk_ceiling_right", "descend_right_wall",
            "attack",

CZEGO NIE RUSZAĆ:
- src/window.py — nie modyfikować
- src/sprite_sheet.py — nie modyfikować
- src/animator.py — nie modyfikować
- src/win_detector.py — nie modyfikować
- src/tray.py — nie modyfikować
- src/__init__.py — nie modyfikować
- main.py — nie modyfikować
- folder "cat animation/" — nie modyfikować
- Pozostała logika behavior.py — nie modyfikować

OCZEKIWANY WYNIK:
Kot podczas chodzenia czasem losowo zatrzymuje się i odgrywa animację ataku
(łapą w prawo lub lewo), po ~1 sekundzie wraca do idle.
python -m py_compile src/behavior.py przechodzi bez błędów.
```

---
## STATUS
- Wykonany: 2026-04-21
- Wynik: ✅ ukończony
- Uwagi: Stan attack z losowym paw_att_right/left, QTimer 1000ms, _end_attack, przejście z walk, listy ignorowanych. Kompilacja ok.

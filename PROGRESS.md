# PROGRESS — Desktop Cat

## Etap 1 — Inicjalizacja projektu
- Status: ✅ ukończony
- Co zostało zrobione: Stworzono requirements.txt (PyQt6, pywin32, Pillow), main.py ze szkieletem QApplication i komentarzami TODO, src/__init__.py
- Pliki zmienione: requirements.txt, main.py, src/__init__.py
- Następny etap: Ładowanie sprite sheeta

## Etap 2 — Ładowanie sprite sheeta
- Status: ✅ ukończony
- Co zostało zrobione: src/sprite_sheet.py z ANIMATION_MAP (53 animacje), load_sprite_sheet(), get_frames(), skalowanie 64x64, cache modułu, blok testowy
- Pliki zmienione: src/sprite_sheet.py
- Następny etap: Okno Qt

## Etap 3 — Okno Qt
- Status: ✅ ukończony
- Co zostało zrobione: src/window.py z klasą CatWindow (frameless, transparent, always-on-top, Tool), set_frame/move_to/paintEvent. main.py podpięty — wyświetla pierwszą klatkę rest_sit na pozycji (100, 800)
- Pliki zmienione: src/window.py, main.py
- Następny etap: System animacji

## Etap 4 — System animacji
- Status: ✅ ukończony
- Co zostało zrobione: src/animator.py z klasą Animator (QTimer, play/stop/_tick, loopowanie). main.py odtwarza walk_right 8 FPS przez window.set_frame
- Pliki zmienione: src/animator.py, main.py
- Następny etap: Zachowanie podstawowe

## Etap 5 — Zachowanie podstawowe
- Status: ✅ ukończony
- Co zostało zrobione: src/behavior.py z CatBehavior — ruch po dole ekranu, odbicia, 6 stanów z przejściami, losowy timer single-shot
- Pliki zmienione: src/behavior.py, main.py
- Następny etap: Detekcja okien i wspinaczka

## Etap 6 — Detekcja okien i wspinaczka
- Status: ✅ ukończony
- Co zostało zrobione: src/win_detector.py (get_windows, find_window_edge_at z best-match), behavior.py rozszerzony o climb_up/down/walk_on_win, timer 500ms, guardy
- Pliki zmienione: src/win_detector.py, src/behavior.py
- Następny etap: Interakcja z myszą

## Etap 7 — Interakcja z myszą
- Status: ✅ ukończony
- Co zostało zrobione: CatWindow z callbackiem kliknięcia. CatBehavior: stany clicked/chase, debounce ID, gonienie kursora z lazy animation switch
- Pliki zmienione: src/window.py, src/behavior.py
- Następny etap: Tray icon

## Etap 8 — Tray icon
- Status: ✅ ukończony
- Co zostało zrobione: src/tray.py z CatTray (ikona z sprite sheeta, menu Pokaż/Ukryj + Zamknij, double-click, dynamiczny tekst akcji). main.py kompletny.
- Pliki zmienione: src/tray.py, main.py
- Następny etap: — (projekt ukończony)

## Etap 9 — Naprawa przezroczystości
- Status: ✅ ukończony
- Co zostało zrobione: Przepisanie CatWindow na QLabel + setStyleSheet("background: transparent;") + Win32 DWM fixes (brak zaokrągleń, brak cienia)
- Pliki zmienione: src/window.py

## Etap 10 — Skala i pozycjonowanie
- Status: ✅ ukończony
- Co zostało zrobione: SCALE 4→8 (64→128px), Win32 SPI_GETWORKAREA dla pozycjonowania, wszystkie referencje do rozmiaru zaktualizowane
- Pliki zmienione: src/sprite_sheet.py, src/window.py, src/behavior.py

## Etap 11 — Centrowanie sprite'a
- Status: ✅ ukończony
- Co zostało zrobione: Po skalowaniu każda klatka centrowana poziomo i wyrównana do dołu. Kot nie siedzi już w rogu klatki.
- Pliki zmienione: src/sprite_sheet.py
- Następny etap: — (projekt ukończony)
## Etap 12 — Pozycja nad paskiem zadań
- Status: ✅ ukończony
- Co zostało zrobione: FindWindowW("Shell_TrayWnd") wykryto pasek (ground_y=1078), kot pozycjonowany na ground_y - 128, wszystkie resety _y zaktualizowane
- Pliki zmienione: src/behavior.py

## Etap 13 — Margines od dołu ekranu
- Status: ✅ ukończony
- Co zostało zrobione: Dodano 15px margines w inicjalizacji _y w __init__ (ground_y - 128 - 15). Resety w update_position bez zmian. Stopy kota widoczne w całości ponad paskiem zadań.
- Pliki zmienione: src/behavior.py

## Etap 14 — Naprawa skalowania sprite'a z paczki 2D
- Status: ✅ ukończony
- Co zostało zrobione: _load_strip zmieniony na _fit_to_canvas — kot wyrównany do dołu. Cofnięto margines -15 z behavior.py. Efekt uboczny: kot za duży (128px), naprawione w etapie 15.
- Pliki zmienione: src/sprite_sheet.py, src/behavior.py

## Etap 15 — Rozmiar sprite'a 2× zamiast fit
- Status: ✅ ukończony
- Co zostało zrobione: Dodano _normalize_and_align (2× scale + bottom-align). _load_strip używa jej zamiast _fit_to_canvas. Kot ~70px, stoi na ziemi.
- Pliki zmienione: src/sprite_sheet.py

## Etap 16 — Kot na pulpicie (za oknami)
- Status: ✅ ukończony
- Co zostało zrobione: Usunięto WindowStaysOnTopHint. Dodano _send_to_bottom (SetWindowPos HWND_BOTTOM), WS_EX_NOACTIVATE, timer co 1000ms. Kot za wszystkimi oknami, kliknięcia nadal działają.
- Pliki zmienione: src/window.py

## Etap 17 — Rotacja sprite'a
- Status: ✅ ukończony
- Co zostało zrobione: _TRANSPOSE_MAP modułowy, self._rotation=0, set_rotation(degrees), rotacja w set_frame przez PIL.transpose.
- Pliki zmienione: src/window.py

## Etap 18 — Wspinaczka po krawędziach ekranu
- Status: ✅ ukończony
- Co zostało zrobione: 6 nowych stanów (climb_right_wall, walk_ceiling_left, descend_left_wall, climb_left_wall, walk_ceiling_right, descend_right_wall). Rotacje 90°/180°/270°. Reset rotacji w _enter_state. Logika ruchu i listy ignorowanych stanów zaktualizowane.
- Pliki zmienione: src/behavior.py

## Etap 21 — Ukryj kota przy pełnym ekranie
- Status: ✅ ukończony
- Co zostało zrobione: Detekcja fullscreen przez GetForegroundWindow + GetSystemMetrics. Timer co 2s. Flaga _hidden_by_fullscreen chroni przed nadpisaniem ręcznego ukrycia z trayu.
- Pliki zmienione: src/behavior.py

## Etap 20 — Cień pod kotem
- Status: ✅ ukończony
- Co zostało zrobione: ImageDraw importowany, cień rysowany na osobnym canvas, kot nakładany na wierzch przez paste z maską alpha. Cień widoczny tylko gdy rotation=0.
- Pliki zmienione: src/window.py

## Etap 19 — Losowa animacja ataku
- Status: ✅ ukończony
- Co zostało zrobione: Nowy stan "attack" z losowym paw_att_right/left, automatyczny powrót do idle po 1s przez _end_attack. Dodany do losowych przejść z walk i list ignorowanych stanów.
- Pliki zmienione: src/behavior.py

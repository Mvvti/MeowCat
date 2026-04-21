# MeowCat

Desktop pet cat for Windows 11 built with Python.

## Stack
- PyQt6
- pywin32
- Pillow

## Features
- Transparent frameless cat window on desktop
- Sprite animation system
- Behavior states (walk, sit, sleep, yawn, attack)
- Mouse interaction (click/chase)
- Edge and window climbing logic
- Tray icon controls
- Auto-hide when a fullscreen app is active

## Project Structure
- `main.py` - app entry point
- `src/sprite_sheet.py` - sprite loading and frame normalization
- `src/window.py` - cat window rendering and effects
- `src/animator.py` - frame timer and playback
- `src/behavior.py` - movement/state machine
- `src/win_detector.py` - open-window detection helpers
- `src/tray.py` - system tray integration

## Setup
```powershell
pip install -r requirements.txt
python main.py
```

## Notes
- The project targets Windows 11.
- Sprite assets are stored in `cat animation/`.

# Turtle Runaway

## Outline
**Turtle Runaway** is a top-down, 2D **chase/evade arcade** game.  
You (the **red** turtle, *chaser*) try to catch the **blue** turtle (*runner*) as many times as possible within the time limit.  
Each tick, the runner takes **one action** (turn or move) and tries to head **away from the chaser**. Near screen edges the runner **respawns**.

- Blue = runner (AI)
- Red = chaser (player)
- HUD: top-left = caught count, top-right = remaining time
- Background image: `background.png` (PNG/GIF recommended)

---

## Features
- **Simple controls:** Arrow keys to move/turn the chaser.
- **Runner AI:** Per tick, randomly **turns or moves** opposite to the chaser.
- **Difficulty ramp:** On every catch, the runner’s `step_move` and `step_turn` each **increase by +2**.
- **Edge handling:**
  - Runner: within 20 px of any border → **random respawn** inside bounds.
  - Chaser: movement is **clamped** so it cannot cross the border.
- **Timer & score:** Countdown starts at **300.0 s**; score is total catches (`catched N runners`).

---

## Requirements
- Python 3.9+ (tested on 3.11)
- Standard library modules: `tkinter`, `turtle`, `random`, `math`
- (Optional) **Pillow** (`pip install pillow`) — only if you want to use JPG backgrounds via `ImageTk`

> Note: `turtle`/`tkinter` load **PNG/GIF** out of the box. **JPG** is not supported by default (`PhotoImage`) and will raise `TclError` unless you use Pillow.

---

## Run
```bash
# Recommended: run from a terminal / command prompt
python turtle_runaway.py

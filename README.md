# My Pygame 2D Shooter 🎮

Hey! Welcome to my 2D shooter platformer game. I built this entirely in Python using the `pygame` library. It started as a fun project to learn game dev, and I ended up adding a lot of cool stuff to it.

## Features
* **Custom Engine:** Built from scratch using Pygame.
* **Smart(ish) Enemies:** They patrol around, actually know when to stop at edges so they don't fall off like idiots, and shoot when you get in their line of sight.
* **Level Editor:** I included a custom level editor (`level_editor_tut.py`) that I used to build the maps. The levels are saved and loaded as `.csv` files.
* **Sounds:** Added some custom/meme sound effects for jumping, shooting, and dying (no more annoying overlapping audio bugs!).
* **Standalone Executable:** I compiled the whole thing into a single `.exe` file, so you can play it without dealing with Python setups.

## How to Play

**Option 1: Just play the game (Windows only)**
If you just want to play, ignore the code. Go to the `dist` folder, find `ShooterGame.exe` (or `main.exe`), and double-click it. You don't need to install Python or anything else.

**Option 2: Run it from the source code**
If you want to mess with the code or make your own levels:
1. Make sure you have Python installed.
2. Open your terminal and install pygame: `pip install pygame`
3. Run the main file: `python main.py`

## Controls
* **Move:** Left / Right Arrows (or A/D)
* **Jump:** Spacebar
* **Shoot:** Mouse Click / Enter *(Change this based on your actual game controls!)*

## Dev Notes / Behind the Scenes
Getting this game to run as a single `.exe` file with PyInstaller was a bit of a nightmare because it kept losing the paths to the `img`, `sound_effects`, and `.csv` folders. If you look at the top of `main.py`, you'll see a little `sys._MEIPASS` trick I used to force the game to find its assets when running as an executable. 

If you want to edit the levels, run `python level_editor_tut.py` and it will save the layout directly to the CSV files which `main.py` reads on startup.

---
Feel free to mess around with the code, change the sprites, or build your own levels using the editor!

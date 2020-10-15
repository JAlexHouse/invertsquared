# invertsquared

This is a python3.x project that is being made for CIS4930: Performant Programming in Python.

PROJECT DESCRIPTION
-    

AESTHETICS:
Color scheme and gameplay layout:
Muted colors, flat design; minimalist

![alt text](https://user-images.githubusercontent.com/55326415/94352158-8c2aa500-002f-11eb-957b-bd67b099dbf2.png)

EXCEPT ...!
- Image to be replicated in top right corner; rounded edges for softer, embedded look
- Game tiles will be 5x5... I Think; rounded edges
- Logo/game name in top left corner; pause/settings button beneath it

SCREENS:
- Home screen: logo in the center (letters are colored, bg is grey); beneath logo: settings/menu, play, share icons;
- Settings screen: game mode (dark/light) (maybe?? or we just stick with the dark theme); audio/vibration settings (if applicable); credits
- Pause screen: home button; settings button; restart level button; select level button;
- Share screen: copy app link for play store; share to Twitter, FB, etc.;
- Level selection screen: 1. choose between Classic, Challenge, Expert (horizontal bars, rounded edges in the center of screen); 2. Select level (level mode will be at top centered; levels will be sorted by difficult ie. lvl 1 is easiest, 20 is hardest; levels display will show the image to replicate); back button in upper left corner;

GAMEPLAY:
- 10/20 levels each mode (maybe 20 for Classic/Challenge, 10 for Expert?); the more the merrier though !!! (if time permits!)
- Hints allowed on all except Expert Mode
3 playing modes: Classic, Challenge, Expert --
- Classic Mode: image to be replicated in upper right corner; playing with no time limits; STRATEGY-BASED gameplay; star ranking by number of moves
- Challenge Mode: image to be replicated in upper right corner; playing with a given amount of time; SPEED-BASED gameplay;
- Expert Mode: image will be shown before you begin the level, but will not remain on screen; MEMORY-BASED gameplay; time limit??? dunno yet


**Run the following commands in the project directory:**

`pip install --user -r requirements.txt`

`python -m pip install --upgrade pip wheel setuptools`

`python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple`

`pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/`

`python -m PyInstaller InvertSquared.spec`

Executable Command
-

`dist\InvertSquared\InvertSquared.exe`

Link to Repository
-

https://github.com/JAlexHouse/invertsquared

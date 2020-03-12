# minereaper
  A program that plays Minesweeper faster than any human by only using the graphical user interface! Minereaper starts by taking a screenshot of the whole screen to locate the game. It then proceeds to play by only using the mouse and taking intermittent screenshots of the game area to update its view of the game. Minereaper can beat Intermediate difficulty quite consistently but since Minesweeper often requires guessing the bot can fail. Since this is purely GUI based bot it can play Minesweeper on any website or running locally assuming they use the original sprites!

![](gif/minereaper.gif)

## Requires
  Requires Pillow, pyautogui and mss (and... well see Warning section)

## Warning
  The code is **highly** screen and OS specific. I made this work on my *13 inch 2016 Macbook pro* which has a (2560 x 1600) display with double pixel density. A lot of the code has to be literally pixel perfect so this probably won't work out of the box on different displays/operating systems and making it compatible with multiple device types just sounds like a chore.

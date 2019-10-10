"""Stick-Bop!

This module runs the game.
"""


import sys
import os

from data.main import main


# for use with PyInstaller
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


if __name__ == '__main__':
    main()

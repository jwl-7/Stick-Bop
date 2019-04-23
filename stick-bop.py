
import sys
import os
from data.main import main

# for use with PyInstaller
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# run main
if __name__ == '__main__':
    main()
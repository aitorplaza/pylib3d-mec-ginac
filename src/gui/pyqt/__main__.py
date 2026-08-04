'''
Entry point for running the IDE as a module:
    python -m src.gui.pyqt
'''
import sys
import os

# Ensure this directory is in sys.path for standalone execution
_this_dir = os.path.dirname(os.path.abspath(__file__))
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from mec_ginac_ide import main

if __name__ == '__main__':
    main()

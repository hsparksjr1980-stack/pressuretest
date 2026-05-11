import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app_files")

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from app_files.app import main

if __name__ == "__main__":
    main()

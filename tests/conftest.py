from pathlib import Path
import sys


SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
SRC_ROOT_STR = str(SRC_ROOT)


if SRC_ROOT_STR not in sys.path:
    sys.path.insert(0, SRC_ROOT_STR)

import sys
import re
from src import mosaic_stitch

if __main__ == "__name__":
    for arg in sys.argv:
        if "marker" in arg and ".txt" in arg:
            arg2 = arg
        elif ".txt" in arg:
            arg1 = arg

    mosaic_stitch.main(arg1, arg2)

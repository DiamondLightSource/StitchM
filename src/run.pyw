import sys
import mosaic_stitch

args = [False, ]
for arg in sys.argv:
    if "marker" in arg and ".txt" in arg:
        args[1] = arg
    elif ".txt" in arg:
        args[0] = arg
mosaic_stitch.main(args)

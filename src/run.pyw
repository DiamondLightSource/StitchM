import sys
import logging

import logger
import mosaic_stitch
from marker_maker import is_marker_file

args = [False, ]
for arg in sys.argv:
    if is_marker_file(arg):
        args[1] = arg
    elif ".txt" in arg:
        args[0] = arg
    else:
        logging.exception(f"arguments {sys.argv} are invalid")
mosaic_stitch.main(args)

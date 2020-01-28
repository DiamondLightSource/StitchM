import sys
import logging

import logger
import mosaic_stitch
from file_checker import *

args = argument_organiser(sys.argv[1:])

if args[0] is not False:
    mosaic_stitch.main(args)

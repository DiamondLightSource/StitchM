import sys
import logging

import logger
import mosaic_stitch
from file_checker import argument_organiser

logger.create_logger("debug")
sys_args = sys.argv
logging.info("Received: %s", sys_args)
args = argument_organiser(sys_args[1:])

if args[0] is not None:
    logging.info(f"Sending files {args} to be stitched")
    mosaic_stitch.main(args)

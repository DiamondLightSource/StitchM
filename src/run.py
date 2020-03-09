import sys
import os
import logging
from configparser import ConfigParser

import logger
import mosaic_stitch
from file_checker import argument_organiser

config = ConfigParser()
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.cfg")) as f:
    config.read_file(f)
logger.create_logger(
    config['LOGGING']['file level'],
    config['LOGGING']['stream level'],
    backup_count=10
    )

sys_args = sys.argv
logging.info("Received: %s", sys_args)
args = argument_organiser(sys_args[1:])

if args[0] is not None:
    logging.info(f"Sending files {args} to be stitched")
    mosaic_stitch.main(args)

import os
import re
import logging

import logger

marker_regex = re.compile(r'(.*)marker(.*).txt$', flags=re.I)


def argument_organiser(arguments):
    args_out = [False, ]
    for arg in arguments:
        if is_marker_file(arg):
            args_out.append(arg)
        elif is_mosaic_file(arg):
            args_out[0] = arg
        else:
            logging.warning(f"argument {arg} is invalid")
    return args_out


def is_marker_file(arg):
    return marker_regex.match(arg)



def is_mosaic_file(arg):
    if ".txt" in arg and os.path.exists(arg):
        with open(arg, 'rb') as csvfile:
            csvfile.seek(0)
            return os.path.exists(csvfile.readline().rstrip())
    return False

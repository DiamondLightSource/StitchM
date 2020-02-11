import os
from numpy import genfromtxt
import re
import logging

marker_regex = re.compile(r'(.*)marker(.*).txt$', flags=re.I)


def argument_organiser(arguments):
    logging.debug("Testing args: %s", arguments)
    args_out = [None, ]
    for arg in arguments:
        if is_marker_file(arg):
            args_out.append(arg)
        elif is_mosaic_file(arg):
            args_out[0] = arg
        else:
            logging.warning(f"argument {arg} is invalid")
    logging.debug("Returning args: %s", args_out)
    return args_out


def is_marker_file(arg):
    return marker_regex.match(os.path.basename(arg))


def is_mosaic_file(arg):
    if ".txt" in arg and os.path.exists(arg) and get_mrc_file(arg)[0] is not None:
        return True
    return False


def get_mrc_file(arg, return_array=False):
    logging.debug("Opening file: %s", arg)
    with open(str(arg), 'rb') as csvfile:
        csvfile.seek(0)
        filepath = os.path.abspath(csvfile.readline().rstrip().decode('utf-8'))
        if return_array:
             location_array = genfromtxt(csvfile, delimiter=",")
    if not os.path.exists(filepath):
        logging.warning(f"Cannot find path %s", filepath)
        if "\\" in filepath:
            #  Windows file paths
            filepath = os.path.join(os.path.dirname(os.path.abspath(arg)), filepath.split("\\")[-1])
        elif "/" in filepath:
            # Unix file paths
            filepath = os.path.join(os.path.dirname(os.path.abspath(arg)), filepath.split("/")[-1])
        else:
            filepath = os.path.join(os.path.dirname(os.path.abspath(arg)), os.path.basename(filepath))
        if not os.path.exists(filepath):
            logging.error(f"Cannot find path %s", filepath, exc_info=True)
            raise IOError(f"Cannot find path %s", filepath)
        logging.info("mrc file with the same name in the current directory will be used")
    if return_array:
        return filepath, location_array
    return filepath, None


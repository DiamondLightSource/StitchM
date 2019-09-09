import os
import re

marker_regex = re.compile(r'(.*)marker(.*).txt$', flags=re.I)


def is_marker_file(arg):
    if marker_regex.match(arg):
        return True
    else:
        return False


def is_mosaic_file(arg):
    if ".txt" in arg:
        with open(arg, 'rb') as csvfile:
            csvfile.seek(0)
        if os.path.exists(csvfile.readline().rstrip()):
            return True
        else:
            return False
    else:
        return False

import sys
from pathlib import Path
import tifffile as tf
import logging

import logger
from unstitched_image import UnstitchedImage
from metadata_maker import MetadataMaker
from stitcher import Stitcher
from file_checker import *


def main(args):
    logging.info(f"Running MosaicStitch with arguments {args}")
    arg0_path = Path(args[0]).resolve()  # Gets absolute path of args[0]

    if arg0_path.is_file() and (arg0_path.suffix == ".txt"):
        tiff_file = str(arg0_path.with_suffix(".ome.tiff"))

        unstitched = UnstitchedImage(arg0_path)
        stitcher = Stitcher(datatype="uint16")
        mosaic = stitcher.make_mosaic(unstitched)
        metadata_creator = MetadataMaker(tiff_file, unstitched, stitcher.get_brightfield_list())

        if len(args) > 1 and is_marker_file(args[1]) and Path(args[1]).is_file():
            tiff_file = tiff_file.replace(".ome.tiff", "_marked.ome.tiff")
            metadata_creator.add_markers(tiff_file, args[1])

        with tf.TiffWriter(tiff_file) as tif:
            tif.save(mosaic, description=metadata_creator.get(), metadata={'axes':'XYZ'})
            tif.close()

    else:
        raise IOError("The first argument must be a text file, not {}".format(args[0]))


if __name__ == "__main__":
    main(sys.argv[1:])

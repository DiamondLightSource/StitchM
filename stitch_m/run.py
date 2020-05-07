import os
import sys
import logging

from .logger import setup_logging, create_logger
from .unstitched_image import UnstitchedImage
from .metadata_maker import MetadataMaker
from .stitcher import Stitcher
from .file_handler import is_mosaic_file, is_marker_file, argument_organiser, get_config, create_user_config, create_Windows_shortcut

def sort_args_then_run():
    try:
        argv = sys.argv[1:]
        # Allows setup options without StitchM script interface:
        create_usr_config = "-cfg" in argv or "--config" in argv
        create_win_shortcut = "-win" in argv or "--windows-shortcut" in argv
        if create_usr_config or create_win_shortcut:
            create_logger("info", "info")
            if create_usr_config:
                create_Windows_shortcut()
            if create_win_shortcut:
                create_user_config()
            logging.getLogger(__name__).handlers.clear()

        config, config_messages = get_config()
        setup_logging(config, config_messages)
        logging.info("StitchM given arguments: %s", argv)
        args = argument_organiser(argv)
        logging.info("Sorted arguments: %s", args)
        if args[0] is not None:
            if len(args) > 2:
                args = args[0:2]
            main_run(config, *args)
        else:
            logging.error("No valid mosaic file")
            if config['OTHER']['wait upon completion'] == 'true':
                input("Press any key to exit")
    except:
        logging.error("Unknown error occurred", exc_info=True)


def main_run(config, mosaic, markers=None):
    """
    PARAMETERS:
        mosaic - Path of .txt file that contains the mosaic information, including the path to the .mrc file
        markers - Path of .txt file that contains a list of marker placements and associated numbers (please make sure this correctly corresponds to the mosaic file)
    
    The output will be saved as the mosaic filename, with the suffix '.ome.tiff' (or '_marked.ome.tiff' if markers are supplied), in same directory as the mosaic file.
    """
    import os
    from pathlib import Path
    from configparser import ConfigParser
    import tifffile as tf
    
    logging.info("Running StitchM with arguments: mosaic=%s, markers=%s", mosaic, markers)
    try:
        if is_mosaic_file(mosaic):
            mosaic_path = Path(mosaic).resolve()  # Gets absolute path of mosaic file
            tiff_file = str(mosaic_path.with_suffix(".ome.tiff"))

            unstitched = UnstitchedImage(mosaic_path)
            stitcher = Stitcher(datatype="uint16")
            mosaic = stitcher.make_mosaic(unstitched, config['PROCESSING']['filter'] == 'true')
            metadata_creator = MetadataMaker(tiff_file, unstitched, stitcher.get_brightfield_list())

            if markers is not None and is_marker_file(markers) and Path(markers).is_file():
                tiff_file = tiff_file.replace(".ome.tiff", "_marked.ome.tiff")
                metadata_creator.add_markers(tiff_file, markers)

            with tf.TiffWriter(tiff_file) as tif:
                tif.save(mosaic, description=metadata_creator.get(), metadata={'axes':'XYZCT'})
                tif.close()
                exit_status = 0
        else:
            raise IOError("Mosaic file path cannot be resolved")
    except:
        exit_status = 1
        if markers is not None:
            logging.error("Invalid arguments: %s, %s", mosaic, markers, exc_info=True)
            raise IOError("Invalid arguments: {}, {}".format(mosaic, markers))
        logging.error("Invalid argument: %s", mosaic, exc_info=True)
        raise IOError("Invalid argument: {}".format(mosaic))

    if config['OTHER']['wait upon completion'] == 'true':
        input("Press any key to exit")

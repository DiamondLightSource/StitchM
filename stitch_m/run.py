import os
import sys
import logging

def sort_args_then_run():
    from .log_handler import LogHandler
    from .file_handler import argument_organiser, get_config, create_user_config, create_Windows_shortcut, boolean_config_handler
    try:
        argv = sys.argv[1:]
        # Allows setup options without StitchM script interface:
        create_usr_config = "-cfg" in argv or "--config" in argv
        create_win_shortcut = "-win" in argv or "--windows-shortcut" in argv
        if create_usr_config or create_win_shortcut:
            with LogHandler("info", "info"):
                if create_usr_config:
                    create_Windows_shortcut()
                if create_win_shortcut:
                    create_user_config()

        config, config_messages = get_config()
        wait_on_fail = boolean_config_handler(config, 'OTHER', 'wait upon failure', default=True)
        with LogHandler(config=config, config_messages=config_messages):
            logging.info("StitchM given arguments: %s", argv)
            args = argument_organiser(argv)
            logging.info("Sorted arguments: %s", args)
            if args[0] is not None:
                if len(args) > 2:
                    args = args[0:2]
                main_run(config, *args)
            else:
                logging.error("No valid mosaic file")
            if wait_on_fail:
                input("Processing failed! Press enter to exit")
    except:
        logging.error("Unknown error occurred", exc_info=True)
        if wait_on_fail:
            input("Processing failed! Press enter to exit")

def _stitch(config, mosaic, markers):
    from pathlib import Path
    from .file_handler import is_mosaic_file, is_marker_file, boolean_config_handler
    from .unstitched_image import UnstitchedImage
    from .metadata_maker import MetadataMaker
    from .stitcher import Stitcher
    try:
        if is_mosaic_file(mosaic):
            mosaic_path = Path(mosaic).resolve()  # Gets absolute path of mosaic file
            tiff_filename = str(mosaic_path.with_suffix(".ome.tiff"))

            unstitched = UnstitchedImage(mosaic_path)
            stitcher = Stitcher(datatype="uint16")
            boolean_config_handler
            mosaic = stitcher.make_mosaic(unstitched, boolean_config_handler(config, 'PROCESSING', 'filter', default=True))
            metadata_creator = MetadataMaker(tiff_filename, unstitched, stitcher.get_brightfield_list())

            if markers is not None and is_marker_file(markers) and Path(markers).is_file():
                tiff_filename = tiff_filename.replace(".ome.tiff", "_marked.ome.tiff")
                metadata_creator.add_markers(tiff_filename, markers)
            return mosaic, metadata_creator.get(), tiff_filename
        else:
            logging.error("Mosaic file path cannot be resolved")
            raise IOError("Mosaic file path cannot be resolved")
    except:
        logging.error("Invalid arguments: %s, %s", mosaic, markers, exc_info=True)
        if boolean_config_handler(config, 'OTHER', 'wait upon failure', default=True):
            input("Processing failed! Press enter to exit")
        raise IOError("Invalid arguments: {}, {}".format(mosaic, markers))
    

def _save(mosaic, metadata, tiff_filename):
    import tifffile as tf
    try:
        logging.info("Saving %s", tiff_filename)
        with tf.TiffWriter(tiff_filename) as tif:
            tif.save(mosaic, description=metadata.to_xml().encode(), metadata={'axes':'XYZCT'})
    except:
        logging.error("Cannot save: %s", tiff_filename, exc_info=True)
        raise IOError("Cannot save: {}".format(tiff_filename))

def main_run(config, mosaic, markers=None):
    """
    PARAMETERS:
        mosaic - Path of .txt file that contains the mosaic information, including the path to the .mrc file
        markers - Path of .txt file that contains a list of marker placements and associated numbers (please make sure this correctly corresponds to the mosaic file)
    
    The output will be saved as the mosaic filename, with the suffix '.ome.tiff' (or '_marked.ome.tiff' if markers are supplied), in same directory as the mosaic file.
    """
    logging.info("Running StitchM with arguments: mosaic=%s, markers=%s", mosaic, markers)
    from .file_handler import boolean_config_handler
    try:
        mosaic, metadata, tiff_file = _stitch(config, mosaic, markers)
        _save(mosaic, metadata, tiff_file)
        if boolean_config_handler(config, 'OTHER', 'wait upon completion', default='false'):
            input("Processing complete. Press enter to exit")
    except:
        logging.error('Error has occurred while stitching or saving mosaic. Please see traceback for more info.', exc_info=True)
        if boolean_config_handler(config, 'OTHER', 'wait upon failure', default='true'):
            input("Processing failed! Press enter to exit")

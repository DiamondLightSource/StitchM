
import os
import sys
import logging
import argparse

def main():
    from .__init__ import __version__
    from .file_handler import get_user_config_path

    description = "Stitch mosaics from Cockpit with (or without) ROIs."
    config_path, _ = get_user_config_path()
    if config_path is not None and config_path.exists():
        description += f" User config can be found at {config_path}."

    parser = argparse.ArgumentParser(prog="StitchM", description=description, add_help=False)
    
    stitch_group = parser.add_argument_group("Stitching arguments")
    stitch_group.add_argument("-m", "--mosaic", metavar="PATH/TO/MOSAIC_FILE.TXT", dest="mosaic", type=str, default="", action='store', help="the mosaic to be stitched (.txt file)")
    stitch_group.add_argument("-a", "--markers", metavar="PATH/TO/MARKER_FILE.TXT", dest="markers", type=str, default="", action='store', help="[OPTIONAL] the markers to be added as ROIs (.txt file)")

    stitch_group.add_argument("-n", "--no-normalisation",
                              metavar="Do not normalise images",
                              dest="normaliseOff", type=bool,
                              default=False, action='store',
                              help="[OPTIONAL]switch to not normalise the output images.")

    setup_subparsers = parser.add_subparsers(title="Setup options", description="enter `StitchM setup -h` for details")
    setup_parser = setup_subparsers.add_parser(name="setup", add_help=False)
    setup_parser.add_argument("-w", "--windows-shortcut", dest="windows_shortcut", action='store_true', help="creates a Windows shortcut on the user's desktop that accepts drag and dropped files (one mosaic at a time, optionally including markers)")
    setup_parser.add_argument("-c", "--config", dest="config", action='store_true', help="creates a user specific config if called")
    setup_info_group = setup_parser.add_argument_group("Setup info")
    setup_info_group.add_argument('-h', '--help', action='help', help="show this help message and exit")

    package_group = parser.add_argument_group("Package info")
    package_group.add_argument('-v', '--version', action='version', version="%(prog)s {}".format(__version__))
    package_group.add_argument('-h', '--help', action='help', help="show this help message and exit")

    args = parser.parse_args()

    # if args has the attribute 'config', the setup subparser has been called and args.win will also exist
    if hasattr(args, 'config'):
        from .log_handler import LogHandler
        with LogHandler("info", "info"):
            if args.windows_shortcut:
                from .file_handler import create_Windows_shortcut
                create_Windows_shortcut()
            if args.config:
                from .file_handler import create_user_config
                create_user_config()
            if not args.windows_shortcut and not args.config:
                setup_parser.print_help()
        return

    # Empty strings are False
    if args.mosaic:
        from .file_handler import get_config
        from .log_handler import LogHandler
        from .run import main_run

        config, config_messages = get_config()
        with LogHandler(config=config, config_messages=config_messages):
            if args.markers:
                logging.info("Sending files %s, %s to be stitched", args.mosaic, args.markers, args.normaliseOff)
                main_run(config, args.mosaic, markers=args.markers, normaliseOff=args.normaliseOff)
            else:
                logging.info("Sending file %s to be stitched", args.mosaic, args.normaliseOff)
                main_run(config, args.mosaic, normaliseOff=args.normaliseOff)
    else:
        parser.print_help()

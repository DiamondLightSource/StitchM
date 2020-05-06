version_info = (1, 0, 0)
__version__ = '.'.join(str(c) for c in version_info)
__author__ = "Thomas Fish"

def stitch(mosaic, markers=None):
    import logging

    from .run import main_run, sort_args_then_run, get_config
    from .logger import setup_logging
    
    config, config_messages = get_config()
    setup_logging(config, config_messages)
    main_run(config, mosaic, markers)

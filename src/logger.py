import logging

logging.basicConfig(filename='mosaicstitch.log',
                    level=logging.DEBUG,
                    format='%formatTime(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)

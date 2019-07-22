from numpy import asarray
from Mrc import bindFile
import logging


class GetMrc():

    def __init__(self, csvfile):
        self.mrc_path = self.get_mrc_location(csvfile)
        self.image = self.extract_image(self.mrc_path)

    @staticmethod
    def get_mrc_location(csvfile):
        csvfile.seek(0)
        return csvfile.readline().rstrip()

    @staticmethod
    def extract_image(mrc_path):
        logging.debug(f"Opening mrc file at {mrc_path}")
        image = bindFile(mrc_path)
        return image

import mrcfile
from numpy import asarray


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
        # permissive allows this mrc file to be opened
        # despite a "bad" header
        with mrcfile.open(mrc_path, permissive=True) as mrc:
            image = asarray(mrc.data, dtype='i')
        return image

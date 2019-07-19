import numpy as np


class TxtExtract():

    def __init__(self, csvfile):
        self.positionlist = self.get_positions(csvfile)
        self.pix2edge = [(self.img_pixels[0]) // 2, (self.img_pixels[1]) // 2]
        self.pix_pos_list = (self.positionlist / self.pixelsize).astype(int)
        self.img_count = self.positionlist.shape[0]
        self.boundaries = self.calculate_boundaries()

    def get_positions(self, csvfile):
        csvfile.seek(0)
        location_array = np.genfromtxt(csvfile, delimiter=",", skip_header=1)
        self.exposure_list = location_array[:, 2]
        self.ave_exposure = np.median(self.exposure_list)
        self.centre = location_array[0, :2]
        self.img_size = location_array[0, 3:5]
        self.img_pixels = location_array[0, 5:7].astype(int)
        self.pixelsize = self.img_size[0] / self.img_pixels[0]  # Assuming square
        return location_array[:, :2] - self.centre[:]

    def calculate_boundaries(self):
        min_coords = (self.pix_pos_list[:, 0].min(), self.pix_pos_list[:, 1].min())
        max_coords = (self.pix_pos_list[:, 0].max(), self.pix_pos_list[:, 1].max())
        image_edges = np.array([[min_coords[0] - self.pix2edge[0],
                                  min_coords[1] - self.pix2edge[1]],
                                 [max_coords[0] + self.pix2edge[0],
                                  max_coords[1] + self.pix2edge[1]]],
                               dtype=int)
        return image_edges

    def get_params(self):
        img_params = {
            "positions"        : self.positionlist,
            "pixel_positions"  : self.pix_pos_list,

            "mosaic_centre"    : self.centre,
            "mosaic_boundaries": self.boundaries,

            "pixels_to_edge"   : self.pix2edge,
            "pixel_size"       : self.pixelsize,
            "image_size"       : self.img_size,
            "image_pixels"     : self.img_pixels,

            "number_of_images"  : self.img_count,
            "exposures"        : self.exposure_list,
            "mean_exposure"    : self.ave_exposure,
            }
        return img_params


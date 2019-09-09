import numpy as np
import logging

import logger


class TxtExtract():

    def __init__(self, csvfile):
        logging.info(f"Importing image values from {csvfile}")
        self._extract_values(csvfile)
        self._calculate_boundaries()

    def _extract_values(self, csvfile):
        csvfile.seek(0)
        location_array = np.genfromtxt(csvfile, delimiter=",", skip_header=1)
        self._get_exposure_data(location_array)
        self._get_image_dimension_data(location_array)
        self._get_position_data(location_array)
        self.img_count = self.positionlist.shape[0]

    def _get_exposure_data(self, location_array):
        self.exposure_list = location_array[:, 2]
        self.exposure_minmax = location_array[:, 7:9]

    def _get_position_data(self, location_array):
        self.centre = location_array[0, :2]
        self.positionlist = location_array[:, :2] - self.centre
        self.pix_pos_list = (self.positionlist / self.pixelsize).astype(int)

    def _get_image_dimension_data(self, location_array):
        self.img_size = location_array[0, 3:5]
        self.img_pixels = location_array[0, 5:7].astype(int)
        self.pixelsize = self.img_size[0] / self.img_pixels[0]  # Assuming square
        self.pix2edge = [(self.img_pixels[0]) // 2, (self.img_pixels[1]) // 2]

    def _calculate_boundaries(self):
        min_coords = (self.pix_pos_list[:, 0].min(), self.pix_pos_list[:, 1].min())
        max_coords = (self.pix_pos_list[:, 0].max(), self.pix_pos_list[:, 1].max())
        image_edges = np.array([[min_coords[0] - self.pix2edge[0],
                                  min_coords[1] - self.pix2edge[1]],
                                 [max_coords[0] + self.pix2edge[0],
                                  max_coords[1] + self.pix2edge[1]]],
                               dtype=int)
        self.boundaries = image_edges

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
            "exposure_black_white"    : self.exposure_minmax,
            }
        return img_params


import numpy as np

import logging

from image_edge_definer import edge_definer


class Stitcher():

    def __init__(self, image, img_params):
        self.image = image
        self.img_count = img_params["number_of_images"]
        self.boundaries = img_params["mosaic_boundaries"]
        self.pix_pos = img_params["pixel_positions"]
        self.exposures = img_params["exposures"]
        self.ave_exposure = img_params["mean_exposure"]
        self.pix2edge = img_params["pixels_to_edge"]

    @staticmethod
    def normalise_exposure(image, exposure, target_exposure):
        uint16max = np.iinfo("uint16").max
        int8max = np.iinfo("uint8").max
        multiplier = (target_exposure / exposure) * (int8max / uint16max)
        return (image * multiplier)

    def make_mosaic(self):
        if self.img_count == self.image.shape[0]:
            # create new large array and load adat from mosaic into it.
            mosaic_size = (self.boundaries[1, 0] - self.boundaries[0, 0],
                         self.boundaries[1, 1] - self.boundaries[0, 1])
            mosaic_array = np.zeros(mosaic_size, dtype="uint8")
            for i in range(self.img_count):
                start, end = edge_definer(
                    self.pix_pos[i, :],
                    self.boundaries,
                    self.pix2edge
                    )
                # Array needs to be transposed for python versus dv.
                # This rotates each image so they line up correctly
                normalised_image = self.normalise_exposure(self.image[i, ::-1, :], self.exposures[i], self.ave_exposure)
                mosaic_array[start[0]:end[0], start[1]:end[1]] = normalised_image.T
            # Rotate back
            return mosaic_array.T.astype("uint8")
        else:
            raise AssertionError("Number of images doesn't match between files")

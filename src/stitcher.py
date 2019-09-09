import numpy as np
import logging

import logger
from edge_definer import image_edge_definer
from builtins import staticmethod
from image_normaliser import normalise_images


class Stitcher():

    def __init__(self, images, img_params):
        # x pixel order is backwards for each image:
        self.images = images[:, ::-1, :]

        self.img_count = img_params["number_of_images"]
        self.boundaries = img_params["mosaic_boundaries"]
        self.pix_pos = img_params["pixel_positions"]
        self.exposures = img_params["exposures"]
        self.exposure_minmax = img_params["exposure_black_white"]
        self.pix2edge = img_params["pixels_to_edge"]

    def find_brightfield_images(self):
        # This returns a list of "good" images i.e. not fluorescent images
        median_max = np.median(self.exposure_minmax[:, 1])
        std_max = np.std(self.exposure_minmax[:, 1])
        good_image_list = []
        for i in range(self.img_count):
            if self.exposure_minmax[i, 1] > median_max - std_max:
                good_image_list.append(i)
            else:
                logging.info(f"Median of image {i} (counted from 0) is not within the minimum threshold")
        return good_image_list

    def make_mosaic(self):
        logging.info("Creating mosaic")
        if self.img_count == self.images.shape[0]:
            good_image_list = self.find_brightfield_images()
            # create new large array and load data into it from mosaic:
            mosaic_size = (self.boundaries[1, 0] - self.boundaries[0, 0],
                         self.boundaries[1, 1] - self.boundaries[0, 1])
            mosaic_array = np.full(mosaic_size, 255, dtype="uint8")

            normalised_images = normalise_images(self.images[:, :, :], self.exposure_minmax, good_image_list)

            for i in range(len(good_image_list)):
                start, end = image_edge_definer(
                    self.pix_pos[good_image_list[i], :],
                    self.boundaries,
                    self.pix2edge
                    )
                # Array needs to be transposed for python versus dv.
                # This rotates each image so they line up correctly
                mosaic_array[start[0]:end[0], start[1]:end[1]] = normalised_images[i, :, :].T
            # Rotate back
            return mosaic_array.T
        else:
            logging.error("Number of images doesn't match between files")
            raise AssertionError("Number of images doesn't match between files")

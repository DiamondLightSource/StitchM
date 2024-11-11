import numpy as np
import logging

from .edge_definer import image_edge_definer
from .image_normaliser import normalise_to_datatype, cast_to_dtype

_logger = logging.getLogger(__package__)


class Stitcher:
    def __init__(self, datatype="uint16"):
        '''Default datatype="uint16"'''
        self.dtype = np.dtype(datatype)
        self.brightfield_list = []

    def make_mosaic(self, unstitched, fl_filter=True, normalise=True):
        _logger.info("Creating mosaic")
        if unstitched.img_count == unstitched.images.shape[0]:
            if fl_filter:
                self.brightfield_list = self._find_brightfield_images(
                    unstitched.img_count, unstitched.exposure_minmax
                )
            else:
                self.brightfield_list = [i for i in range(unstitched.img_count)]
            # create new large array and load data into it from mosaic:
            mosaic_size = (
                unstitched.boundaries[1, 0] - unstitched.boundaries[0, 0],
                unstitched.boundaries[1, 1] - unstitched.boundaries[0, 1],
            )

            # If we are not normalising, fill with zero values rather than max
            fill_value = np.iinfo(self.dtype).max * normalise
            mosaic_array = np.full(mosaic_size, fill_value, dtype=self.dtype)

            images = unstitched.images[
                self.brightfield_list
            ]  # Filter out unwanted images
            unstitched.clear_image_array()
            if normalise:
                # Rescale max/min to fit data type
                images = normalise_to_datatype(images, self.dtype, trim=True)

            # Cast to output data type
            images = cast_to_dtype(images, self.dtype)

            for i in range(len(self.brightfield_list)):
                start, end = image_edge_definer(
                    unstitched.pix_positionlist[self.brightfield_list[i], :],
                    unstitched.boundaries,
                    unstitched.pix2edge,
                )
                # Array needs to be transposed for python versus dv.
                # This rotates each image so they line up correctly
                mosaic_array[start[0] : end[0], start[1] : end[1]] = images[i, :, :].T
            del images
            # Rotate back and flip
            return np.flip(mosaic_array.T, 0)
        else:
            _logger.error("Number of images doesn't match between files")
            raise AssertionError("Number of images doesn't match between files")

    def get_brightfield_list(self):
        return self.brightfield_list

    @staticmethod
    def _find_brightfield_images(img_count, minmax):
        """
        This returns a list of indices of "good" images (i.e. not fluorescent
        images).
        This is based on the the interquartile range. If this is 0 for either
        the min or max exposure values, std will be used instead (to
        allow for some close values beyond the IQR).

        This method is not valid if there are too many fl images to bf images,
        as this will affect the IQR.

        If more than half of the images are filtered out by this metric,
        it is assumed something hasn't worked correctly and a list including
        of all image indices will be returned.
        """

        full_list = range(0, img_count)

        # First & third quartile
        q1, q3 = np.percentile(minmax, (25, 75), axis=0)
        # interquartile range
        iqr = q3 - q1

        mod = np.where(iqr > 0, iqr * 1.5, np.std(minmax, axis=0))

        good_list = np.where(
            np.logical_and(
                minmax[:, 0] >= q1[0] - mod[0], minmax[:, 1] <= q3[1] + mod[1]
            )
        )[0]

        num_good = len(good_list)
        num_fl = img_count - num_good
        if num_fl > 0:
            fl_list = np.setdiff1d(full_list, good_list)
            list_str = ": '%s' (counted from 0)" % ", ".join(map(str, fl_list))
        else:
            list_str = ""
        _logger.info(
            "%i potential fluorescence images identified (and %i brightfield)%s",
            num_fl,
            num_good,
            list_str,
        )
        if num_good < img_count / 2:
            _logger.info(
                "Too many fluorescence images 'identified', so no trimming will be performed to avoid false positives"
            )
            return full_list
        return good_list

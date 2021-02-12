import unittest
import numpy as np
from numpy.testing import assert_array_equal

from stitch_m import image_normaliser


class NormalisationTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        unittest.TestCase.setUp(cls)
        cls.dtype = np.uint16
        cls.image_max = np.iinfo(cls.dtype).max - 1

    def test_normalise_to_datatype(self):
        image = np.arange(6524, 6536).reshape(3, 4)
        images = np.array([image, image])
        image_out = image_normaliser.normalise_to_datatype(images, self.dtype)
        self.assertTrue((image_out.max() == self.image_max), msg=f"image max {image_out.max()} is not {self.image_max}")
        self.assertTrue((image_out.min() == 0), msg=f"image min {image_out.min()} is not 0")

    def test_normalise_simple_minmax_image(self):
        image = np.linspace(524, 5536, 12).reshape(3, 4)
        images = np.array([image, image])
        exp_minmax = np.asarray([[0, 1], [0, 1]])
        good_image_list = [0, 1]

        expected_image = image_normaliser.cast_to_dtype(np.linspace(0, self.image_max, 12).reshape(3, 4), self.dtype)
        expected_images = np.array([expected_image, expected_image])
        
        images_out = image_normaliser.normalise_to_datatype(
            np.asarray(
                image_normaliser.exposure_correct(images, exp_minmax, good_image_list)),
                self.dtype)
        assert_array_equal(image_normaliser.cast_to_dtype(images_out, self.dtype), expected_images)

    def test_normalise_avoiding_bad_image(self):
        image = np.linspace(524, 5536, 12).reshape(3, 4)
        # "bad_image" has a maximum well out of the stdev of the
        # mosaic, so should be cut from "images_out":
        bad_image = np.linspace(0, 100000, 12).reshape(3, 4)
        images = np.array([image, bad_image, image])
        exp_minmax = np.asarray([[0, 1], [0, 1], [0, 1]])
        good_image_list = [0, 2]

        expected_image = image_normaliser.cast_to_dtype( np.linspace(0, self.image_max, 12).reshape(3, 4), self.dtype)
        expected_images = np.array([expected_image, expected_image])

        images_out = image_normaliser.normalise_to_datatype(
            np.asarray(
                image_normaliser.exposure_correct(images, exp_minmax, good_image_list)),
                self.dtype)
        assert_array_equal(image_normaliser.cast_to_dtype(images_out, self.dtype), expected_images)

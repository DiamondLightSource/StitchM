import unittest
import numpy as np

from stitcher import Stitcher


class StitcherTests(unittest.TestCase):

    def test_normalise_max_uint16_to_uint8(self):
        image = np.arange(65524, 65536)
        image.shape = 3, 4
        exposure = 2
        target_exposure = 2
        image_out = Stitcher.normalise_exposure(image, exposure, target_exposure)
        self.assertTrue((image_out.max() == 255), msg=f"{image_out.max()} is not 255")

    def test_normalise_image(self):
        image = np.linspace(65524, 65536, 12).reshape(3, 4)

        uint162uint8 = 255 / 65535
        exposure = 5
        target_exposure = 2
        multiplier = (target_exposure / exposure) * uint162uint8

        expected_image = np.linspace((65524 * multiplier), (65536 * multiplier), 12).reshape(3, 4)

        image_out = Stitcher.normalise_exposure(image, exposure, target_exposure)
        self.assertTrue((image_out.all() == expected_image.all()), msg="Image doesn't match expected")

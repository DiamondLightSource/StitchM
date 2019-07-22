import unittest
import numpy as np
from mock import MagicMock

import image_normaliser


class NormalisationTests(unittest.TestCase):

    def test_rescale_corrected_imgs(self):
        image = np.arange(65524, 65536).reshape(3, 4)
        images = np.array([image, image])
        image_out = image_normaliser._rescale_corrected_imgs(images)
        self.assertTrue((image_out.max() == 255), msg=f"image max {image_out.max()} is not 255")
        self.assertTrue((image_out.min() == 0), msg=f"image min {image_out.min()} is not 0")

    def test_normalise_simple_minmax_image(self):
        image = np.linspace(524, 5536, 12).reshape(3, 4)
        images = np.array([image, image])
        exp_minmax = np.asarray([[0, 1], [0, 1]])
        good_image_list = [0, 1]

        expected_image = np.linspace(0, 255, 12).reshape(3, 4).astype('i')
        expected_images = np.array([expected_image, expected_image])

        images_out = image_normaliser.normalise_images(images, exp_minmax, good_image_list)
        self.assertTrue((images_out == expected_images).all(), msg="Image doesn't match expected")

# Due to current exposure correction method, the response isn't linear
# making it hard to figure out what it should be without fully copying
# its method. I will work on making this test make sense later.
#     def test_normalise_difficult_minmax_image(self):
#         image = np.linspace(524, 5536, 12).reshape(3, 4)
#         images = np.array([image, image])
#         exp_minmax = np.asarray([[0, 25000.0], [0, 50000.0]])
#         good_image_list = [0, 1]
#
#         expected_image = np.linspace(0, 255, 12).reshape(3, 4)
#         expected_images = np.array([expected_image / 2, expected_image]).astype('i')
#
#         images_out = image_normaliser.normalise_images(images, exp_minmax, good_image_list)
#         self.assertTrue((images_out == expected_images).all(), msg="Image doesn't match expected")

    def test_normalise_avoiding_bad_image(self):
        image = np.linspace(524, 5536, 12).reshape(3, 4)
        bad_image = np.linspace(0, 65536, 12).reshape(3, 4)
        images = np.array([image, bad_image, image])
        exp_minmax = np.asarray([[0, 1], [0, 1], [0, 1]])
        good_image_list = [0, 2]

        expected_image = np.linspace(0, 255, 12).reshape(3, 4).astype('i')
        expected_images = np.array([expected_image, expected_image])

        images_out = image_normaliser.normalise_images(images, exp_minmax, good_image_list)
        self.assertTrue((images_out == expected_images).all(), msg="Image doesn't match expected")

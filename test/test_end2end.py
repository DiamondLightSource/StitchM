import unittest
import os
import tifffile as tf
import numpy as np
from PIL import Image

from mosaic_stitch import main as stitch_main

base_path = "/dls/science/groups/das/ExampleData/B24_test_data/MosaicStitch_test_data/files/"
test_files = (base_path + "B15Grid2.txt", base_path + "B8G1-IR_mosaic.txt", base_path + "B8G2-IR_mosaic.txt", base_path + "Fid_T2G3_mosaic.txt")
test_marker_files = (base_path + "B15_location_markers.txt", base_path + "B8G1-IR_markers.txt", base_path + "B8G2-IR_markers.txt", base_path + "Fid_T2G3_markers.txt")
# test_files = (base_path + "Fid_T2G3_mosaic.txt",)  # reduced tuple for quick tests
# test_marker_files = (base_path + "Fid_T2G3_markers.txt",)

expected_outputs = [path.replace(".txt", "_expected_output.tiff") for path in test_files]
expected_marked_outputs = [path.replace(".txt", "_expected_output_marked.tiff") for path in test_files]


class MosaicStitchTests(unittest.TestCase):

    @classmethod
    def tearDownClass(MosaicStitchTests):
        for file in test_files:
            output_path = file.replace('.txt', '.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)
            output_path = file.replace('.txt', '_marked.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)

    def test_end_to_end_simple(self):
        for i in range(len(test_files)):
            test_file = test_files[i]
            stitch_main([test_file, ])
            output_path = test_file.replace('.txt', '.tiff')
            self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
            output_image = tf.imread(output_path)

            expected_file = expected_outputs[i]
            expected_image = tf.imread(expected_file)

            self.assertTrue((output_image == expected_image).all(), msg=f"Not true for {test_file}")

    def test_end2end_with_markers(self):
        for i in range(len(test_files)):
            test_file = test_files[i]
            stitch_main([test_file, test_marker_files[i]])
            output_path = test_file.replace('.txt', '_marked.tiff')
            self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
            output_image = np.asarray(Image.open(output_path))

            expected_file = expected_marked_outputs[i]
            expected_image = np.asarray(Image.open(expected_file))

            self.assertTrue(output_image.all() == expected_image.all(), msg=f"Not true for {test_file}")


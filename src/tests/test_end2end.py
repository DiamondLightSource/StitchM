import unittest
from unittest.mock import patch
from numpy.testing import assert_array_equal

import os
import tifffile as tf
import numpy as np
from pathlib import Path


from stitch_m import file_handler, stitch_and_save

# To quickly update the files:
# - Comment out file removal in tearDownClass
# - Comment out file opening and comparisons
# - Delete old expected_output files
# - Within the base_path dir, run:
#   for f in *.ome.tiff; do mv "$f" `echo ${f} | sed 's/.ome.tiff/_expected_output.ome.tiff/'`; done
# - Uncommented out code commented out above

base_path = Path("/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files")
test_files = (
    base_path / "B15Grid2.txt",
    base_path / "B8G1-IR_mosaic.txt",
    base_path / "B8G2-IR_mosaic.txt",
    base_path / "Fid_T2G3_mosaic.txt",
    base_path / "Yo10_G3_mosaic.txt"
    )

test_marker_files = (
    base_path / "B15_location_markers.txt",
    base_path / "B8G1-IR_markers.txt",
    base_path / "B8G2-IR_markers.txt",
    base_path / "Fid_T2G3_markers.txt",
    base_path / "Yo10_G3_mosaic_MARKERS.txt"
    )

# # Reduced tuple for quick tests:
# test_files = (
#     base_path / "Fid_T2G3_mosaic.txt",
#     )
# test_marker_files = (
#     base_path / "Fid_T2G3_markers.txt",
#     )
test_files = [str(path) for path in test_files]
test_marker_files = [str(path) for path in test_marker_files]

expected_outputs = [
    path.replace(".txt", "_expected_output.ome.tiff")
    for path in test_files]
expected_marked_outputs = [
    path.replace(".txt", "_marked_expected_output.ome.tiff")
    for path in test_files]
test_config = Path(__file__).resolve().with_name("config.cfg")


@unittest.skipUnless(base_path.exists(), "base path cannot be accessed")
class EndToEndTests(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        for f in test_files:
            output_path = f.replace('.txt', '.ome.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)
            output_path = f.replace('.txt', '_marked.ome.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)

    @patch('stitch_m.file_handler')
    def test_end_to_end_simple(self, mocked_file_handler):
        mocked_file_handler.local_config_file.return_value = test_config
        for i in range(len(test_files)):
            test_file = test_files[i]
            stitch_and_save(test_file)
            output_path = test_file.replace('.txt', '.ome.tiff')
            self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
            output_image = tf.imread(output_path)

            expected_file = expected_outputs[i]
            expected_image = tf.imread(expected_file)

            assert_array_equal(output_image, expected_image)

    @patch('stitch_m.file_handler')
    def test_end2end_with_markers(self, mocked_file_handler):
        self.maxDiff = 8000  # Set diff so that all metadata can be read
        mocked_file_handler.local_config_file.return_value = test_config
        for i in range(len(test_files)):
            test_file = test_files[i]
            stitch_and_save(test_file, test_marker_files[i])
            output_path = test_file.replace('.txt', '_marked.ome.tiff')
            self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
            
            with tf.TiffFile(output_path) as tif:
                output_image = tif.asarray()
                output_metadata = tif.ome_metadata

            with tf.TiffFile(expected_marked_outputs[i]) as tif:
                expected_image = tif.asarray()
                expected_metadata = tif.ome_metadata

            assert_array_equal(output_image, expected_image)
            self.assertEqual(
                output_metadata, expected_metadata,
                msg=f"Metadata should match for {output_path} & {expected_marked_outputs[i]}\n")

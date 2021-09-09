import unittest
from unittest.mock import patch
import os
from pathlib import Path
from numpy import genfromtxt
from numpy.testing import assert_array_equal

from stitch_m import file_handler

base_path = Path("/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files/")
test_file = base_path / "Fid_T2G3_mosaic.txt"
test_marker_file = base_path / "Fid_T2G3_markers.txt"
bad_file = base_path / "bad_file.txt"

testargs = [test_file, test_marker_file]
bad_testargs = [bad_file, test_marker_file, test_file]

test_config = Path(__file__).resolve().with_name("config.cfg")


@unittest.skipUnless(base_path.exists(), "base path cannot be accessed")
class FileHandlerTests(unittest.TestCase):

    @patch('stitch_m.file_handler')
    def test_argument_filtering(self, mocked_file_handler):
        mocked_file_handler.local_config_file.return_value = test_config
        if os.path.exists(base_path):
            for arguments in [testargs, testargs[::-1], bad_testargs]:
                arguments_out = file_handler.argument_organiser(arguments)
                self.assertEqual(arguments_out, testargs)
        else:
            print("Cannot run test without access to dls directories")

    @patch("logging.warning")
    @patch("logging.info")
    def test_is_mosaic_file(self, mocked_logging_info, mocked_logging_warning):
        self.assertTrue(
            file_handler.is_mosaic_file(test_file),
            msg=f"{test_file.name} {'exists' if test_file.exists() else 'does not exist'}")
        self.assertFalse(
            file_handler.is_mosaic_file(bad_file),
            msg=f"{bad_file.name} {'exists' if bad_file.exists() else 'does not exist'}")
        mocked_logging_info.assert_not_called()
        mocked_logging_warning.assert_not_called()

    def test_get_mrc_file_opens_file(self):
        with test_file.open('rb') as csvfile:
            mrc_path = Path(csvfile.readline().rstrip().decode('utf-8')).absolute()
            expected_location_array = genfromtxt(csvfile, delimiter=",")

        expected_output_path = test_file.parent / mrc_path.name
        
        output_path, location_array = file_handler.get_mrc_file(test_file, True)

        self.assertEqual(output_path, expected_output_path)
        assert_array_equal(location_array, expected_location_array)

    def test_get_mrc_file_good_file(self):
        with test_file.open('rb') as csvfile:
            mrc_path = Path(csvfile.readline().rstrip().decode('utf-8')).absolute()
        
        expected_output_path = test_file.parent / mrc_path.name

        self.assertTrue(file_handler.get_mrc_file(test_file, False))


    def test_get_mrc_file_bad_file(self):
        self.assertFalse(file_handler.get_mrc_file(bad_file, False))

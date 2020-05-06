import unittest
import os
from stitch_m import file_handler

base_path = "/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files/"
test_file = base_path + "Fid_T2G3_mosaic.txt"
test_marker_file = base_path + "Fid_T2G3_markers.txt"
bad_file = base_path + "bad_file.txt"

testargs = [test_file, test_marker_file]
bad_testargs = [bad_file, test_marker_file, test_file]


class FileCheckerTests(unittest.TestCase):

    def test_argument_filtering(self):
        if os.path.exists(base_path):
            for arguments in [testargs, testargs[::-1], bad_testargs]:
                arguments_out = file_handler.argument_organiser(arguments)
                self.assertEqual(arguments_out, testargs)
        else:
            print("Cannot run test without access to dls directories")

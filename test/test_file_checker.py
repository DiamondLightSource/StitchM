import unittest
from file_checker import *
from nose.tools import assert_true

base_path = "/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files/"
test_file = base_path + "Fid_T2G3_mosaic.txt"
test_marker_file = base_path + "Fid_T2G3_markers.txt"
bad_file = base_path + "bad_file.txt"

testargs = [test_file, test_marker_file]
bad_testargs = [bad_file, test_marker_file, test_file]


class FileCheckerTests(unittest.TestCase):

    def test_argument_filtering(self):
        for arguments in [testargs, testargs[::-1], bad_testargs]:
            arguments_out = argument_organiser(arguments)
            assert_true(arguments_out == testargs)

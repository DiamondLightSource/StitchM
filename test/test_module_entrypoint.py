import sys
import unittest
from unittest.mock import patch, MagicMock, ANY

import stitch_m


class TestEntryPointStitch(unittest.TestCase):
    @patch('stitch_m.run.main_run')
    def test_module_stitch_method(self, stitch_m_run):
        args = ["path_to/mosaic.txt", None]
        stitch_m.stitch(args[0])
        stitch_m_run.assert_called_once_with(ANY, *args)

    @patch('stitch_m.run.main_run')
    def test_module_stitch_method_with_marker_file(self, stitch_m_run):
        args = ["path_to/mosaic.txt", "path_to/markers.txt"]
        test_function = stitch_m.stitch
        stitch_m.stitch(*args)
        stitch_m_run.assert_called_once_with(ANY, *args)

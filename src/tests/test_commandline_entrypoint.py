import os
import sys
import unittest
from unittest.mock import patch, MagicMock, ANY
from subprocess import Popen, PIPE, STDOUT
from time import sleep

from stitch_m.__init__ import __version__ as version

from stitch_m.scripts import commandline


class TestEntryPointCommandline(unittest.TestCase):
    # Before these running tests, the module must be installed in development mode using:
    # `pip install --editable . --user` (from the project folder)
    # it can be uninstalled at the end using:
    # `pip uninstall StitchM`
    # IF TESTING ON WINDOWS: make sure the correct python installation is set as the default in PATH

    @classmethod
    def setUpClass(cls):
        # Set maximum difference string length to None (infinite)
        cls.maxDiff = None
        # Add local intall to path for testing with development install
        if os.name == "posix":
            os.environ["PATH"] += os.pathsep + os.path.join(
                os.path.expanduser("~"), ".local", "bin"
            )

    @patch("argparse.ArgumentParser.print_help")
    def test_commandline_function(self, mocked_printhelp):
        sys.argv = ["StitchM"]
        commandline.main()

        mocked_printhelp.assert_called_once()

    @patch("argparse.ArgumentParser.print_help")
    def test_commandline_function_setup_subpaser(self, mocked_printhelp):
        sys.argv = ["StitchM", "setup"]
        commandline.main()

        mocked_printhelp.assert_called_once()

    def test_commandline_function_setup_config(self):
        with patch(
            "stitch_m.file_handler.create_user_config", MagicMock()
        ) as mocked_config_creator:
            sys.argv = ["StitchM", "setup", "--config"]
            commandline.main()

            mocked_config_creator.assert_called_once()

    def test_commandline_function_setup_windows_shortcut(self):
        with patch(
            "stitch_m.file_handler.create_Windows_shortcut", MagicMock()
        ) as mocked_shortcut_creator:
            sys.argv = ["StitchM", "setup", "-w"]
            commandline.main()

            mocked_shortcut_creator.assert_called_once()

    def test_commandline_function_with_args(
        self,
    ):
        with patch("stitch_m.run.main_run", MagicMock()) as main_run:
            kwargs = {}
            kwargs["mosaic"] = "mosaic_path"
            kwargs["markers"] = "marker_path"
            kwargs["normalise"] = True
            kwargs["fl_filter"] = True

            sys.argv = [
                "StitchM",
                "--mosaic",
                kwargs["mosaic"],
                "--markers",
                kwargs["markers"],
            ]
            commandline.main()

            main_run.assert_called_once_with(ANY, **kwargs)

    def test_commandline_function_with_args_normalise_filter(
        self,
    ):
        with patch("stitch_m.run.main_run", MagicMock()) as main_run:
            kwargs = {}
            kwargs["mosaic"] = "mosaic_path"
            kwargs["markers"] = "marker_path"
            kwargs["normalise"] = False
            kwargs["fl_filter"] = False

            sys.argv = [
                "StitchM",
                "--mosaic",
                kwargs["mosaic"],
                "--markers",
                kwargs["markers"],
                "--unfiltered",
                "--no-normalisation",
            ]
            commandline.main()

            main_run.assert_called_once_with(ANY, **kwargs)

    def test_commandline_method(self):
        args = ["path_to/mosaic"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(
            run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT
        ) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(
            f"Invalid arguments: {args[0]}, None, True",
            stdout,
            msg=f"Actual stdout: {stdout}",
        )

    def test_commandline_method_invalid_path(self):
        args = ["path_to/mosaic.txt"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(
            run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT
        ) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(
            "Mosaic file path cannot be resolved",
            stdout,
            msg=f"Actual stdout: {stdout}",
        )

    def test_commandline_method_with_marker_file(self):
        args = ["path_to/mosaic", "path_to/markers"]
        run_args = [
            "StitchM",
            "--mosaic",
            args[0],
            "--markers",
            args[1],
            "--no-normalisation",
        ]
        with Popen(
            run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT
        ) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(
            f"Invalid arguments: {args[0]}, {args[1]}, False",
            stdout,
            msg=f"Actual stdout: {stdout}",
        )

    def test_commandline_method_version_number(self):
        run_args = ["StitchM", "--version"]
        with Popen(
            run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT
        ) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertEqual(f"StitchM {version}", stdout, msg=f"Actual stdout: {stdout}")

    def test_commandline_method_setup_subparser(self):
        run_args = ["StitchM", "setup"]
        with Popen(
            run_args, universal_newlines=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT
        ) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(
            "StitchM setup [-w] [-c] [-h]", stdout, msg=f"Actual stdout: {stdout}"
        )

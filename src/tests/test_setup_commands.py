import os
import logging
import unittest
import pathlib
from pathlib import Path
from unittest.mock import patch, MagicMock

import stitch_m
from stitch_m.file_handler import (
    create_user_config,
    create_Windows_shortcut,
    _create_lnk_file,
    _get_desktop_path,
    _logger,
)


class TestSetupFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set maximum difference string length to None (infinite)
        cls.maxDiff = None

    # ------------------
    # Test config setup:

    def test_setup_config(self):
        with patch("shutil.copyfile", MagicMock()) as mocked_copyfile:
            local_config_file = (
                Path(stitch_m.__file__).resolve().with_name("config.cfg")
            )
            user_config_location = Path(stitch_m.__file__).parent / "test_config_path"
            with patch(
                "stitch_m.file_handler.get_user_config_path",
                MagicMock(return_value=(user_config_location, [])),
            ):
                create_user_config()
            mocked_copyfile.assert_called_once_with(
                local_config_file, user_config_location
            )

    @patch("stitch_m.file_handler.get_user_config_path")
    @patch.object(_logger, "error")
    def test_setup_config_fail_bad_path(self, mocked_error_log, mocked_get_config):
        mocked_get_config.return_value = (
            Path(os.path.expanduser("~/.fake_dir/oh_no/thisisbad.cfg")),
            [],
        )
        create_user_config()
        mocked_error_log.assert_called_once_with(
            "Unable to create user config file due to directory issues", exc_info=True
        )

    # ------------------
    # Test Windows shortcut setup:

    @patch("os.name")
    @patch.object(_logger, "error")
    def test_setup_win_exits_on_linux(self, mocked_error_log, mocked_os_name):
        mocked_os_name.return_value = "posix"
        create_Windows_shortcut()
        mocked_error_log.assert_called_once_with(
            "This command is only valid on Windows installations."
        )

    @patch.object(pathlib.Path, "exists", MagicMock(return_value=False))
    @patch.object(_logger, "error")
    def test_setup_windows_shortcut_function_called(self, mocked_error):
        with patch(
            "stitch_m.file_handler._create_lnk_file", MagicMock()
        ) as mocked_shortcut_creator:
            create_Windows_shortcut()
            if os.name == "nt":
                home_dir = Path(os.environ["HOMEDRIVE"]) / os.environ["HOMEPATH"]
                try:
                    desktop = _get_desktop_path()
                    self.assertTrue(
                        desktop.relative_to(home_dir), "Invalid desktop found"
                    )
                except Exception:
                    logging.warning("_get_desktop_path failed")
                    desktop = home_dir / "Desktop"

                self.assertTrue(desktop.is_dir(), "Invalid desktop found")
                mocked_shortcut_creator.assert_called_once_with(desktop / "StitchM.lnk")
            else:
                mocked_error.assert_called_once_with(
                    "This command is only valid on Windows installations."
                )

    @unittest.skipUnless(os.name == "nt", "Only run on Windows")
    def test_setup_windows_shortcut_test_created_(self):
        # Only run this test if on Windows
        test_shortcut_path = Path(".") / "test_shortcut.lnk"
        _create_lnk_file(test_shortcut_path)
        link_created = test_shortcut_path.exists()
        if link_created:
            os.remove(test_shortcut_path)
        self.assertTrue(link_created)

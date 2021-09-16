import unittest
from unittest.mock import patch, MagicMock, call
from tempfile import TemporaryDirectory

from pathlib import Path
from io import StringIO

from stitch_m.log_handler import LogHandler
    

class TestLoggerMethods(unittest.TestCase):

    @staticmethod
    def create_logger(log_dir, log_to_file):
        with patch('stitch_m.file_handler.get_user_log_path', MagicMock(return_value=(log_dir))):
            return LogHandler(file_level="info", stream_level="error", log_to_file=log_to_file, backup_count=1)

    def test_logger_without_file(self):
        with TemporaryDirectory(prefix="logs", dir=".") as log_dir:
            log_dir = Path(log_dir)
            log_handler = TestLoggerMethods.create_logger(log_dir, False)
            log_files = list(log_dir.glob("*"))
            log_handler.close()
            self.assertFalse(log_files)           

    @patch('sys.stdout', new_callable=StringIO)
    def test_loggers_created(self, mocked_stdout):
        with TemporaryDirectory(prefix="logs_", dir=Path.cwd()) as log_dir:
            log_dir = Path(log_dir).absolute()
            log_handler = TestLoggerMethods.create_logger(log_dir, True)
            logger = log_handler.get_logger()

            debug_line = "This is debug info"
            info_line = "This is info"
            error_line = "This is an error"
            logger.debug(debug_line)
            logger.info(info_line)
            logger.error(error_line)

            log_handler.close()

            log_files = tuple(log_dir.glob("*"))
            self.assertEqual(len(log_files), 1)
            for log in log_files:
                with log.open("r") as f:
                    lines = f.read()
                    self.assertNotIn(debug_line, lines)
                    self.assertIn(info_line, lines)
                    self.assertIn(error_line, lines)
        stdout = mocked_stdout.getvalue()
        self.assertNotIn(debug_line, stdout)
        self.assertNotIn(info_line, stdout)
        self.assertIn(error_line, stdout)

    def test_file_path_fails(self):
        # Shouldn't throw an error:
        TestLoggerMethods.create_logger(None, True).close()

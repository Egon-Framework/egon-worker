"""Tests for the ``BaseParser``  class"""

from unittest import TestCase

from egon_worker.cli import BaseParser


class ErrorHandling(TestCase):

    def test_error_message_included(self) -> None:
        """Test error messages are included in raised errors"""

        message = 'This is a test'
        parser = BaseParser()
        with self.assertRaisesRegex(SystemExit, message):
            parser.error(message)
